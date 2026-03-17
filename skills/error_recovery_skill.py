"""
Error Recovery Skill

Handles MCP server failures by detecting errors, retrying operations,
logging errors appropriately, and ensuring the orchestrator continues running.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, Callable
import httpx
import aiofiles
from pathlib import Path


async def error_recovery_skill(
    operation_func: Callable,
    *args,
    **kwargs
) -> Dict[str, Any]:
    """
    Execute an operation with error recovery capabilities.

    Args:
        operation_func: The function to execute (typically an MCP call)
        *args: Arguments for the operation function
        **kwargs: Keyword arguments for the operation function

    Returns:
        Dict with operation result and status information
    """
    max_retries = 1
    retry_count = 0
    last_error = None

    # Extract operation name from function if available
    operation_name = getattr(operation_func, '__name__', 'unknown_operation')

    while retry_count <= max_retries:
        try:
            # Execute the operation
            result = await operation_func(*args, **kwargs)

            # Check if result indicates success
            if isinstance(result, dict):
                if result.get('success', False):
                    return {
                        "status": "success",
                        "result": result,
                        "attempts": retry_count + 1,
                        "operation": operation_name
                    }
                else:
                    # Even if marked as failure, continue to error handling
                    pass

            # If we get here with a successful result (non-dict or success=True)
            return {
                "status": "success",
                "result": result,
                "attempts": retry_count + 1,
                "operation": operation_name
            }

        except httpx.HTTPStatusError as e:
            last_error = f"HTTP error: {e.response.status_code} - {e.response.text}"
            error_details = {
                "error_type": "HTTPStatusError",
                "status_code": e.response.status_code,
                "response_text": e.response.text,
                "operation": operation_name
            }
        except httpx.RequestError as e:
            last_error = f"Request error: {str(e)}"
            error_details = {
                "error_type": "RequestError",
                "error_message": str(e),
                "operation": operation_name
            }
        except Exception as e:
            last_error = f"Unexpected error: {str(e)}"
            error_details = {
                "error_type": "UnexpectedError",
                "error_message": str(e),
                "operation": operation_name
            }

        # If this was the last attempt, log the error and continue
        if retry_count >= max_retries:
            await log_error(error_details, last_error)
            await update_dashboard_error_count()

            return {
                "status": "failed_after_retry",
                "error": last_error,
                "error_details": error_details,
                "attempts": retry_count + 1,
                "operation": operation_name,
                "result": None
            }

        # Otherwise, increment retry count and try again
        retry_count += 1
        await asyncio.sleep(1)  # Brief delay before retry

    # This shouldn't be reached, but just in case
    return {
        "status": "failed",
        "error": last_error,
        "attempts": retry_count,
        "operation": operation_name,
        "result": None
    }


async def log_error(error_details: Dict[str, Any], error_message: str):
    """Log the error to error_log.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create error logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_entry = f"""
## Error Log - {timestamp}
- **Operation:** {error_details.get('operation', 'unknown')}
- **Error Type:** {error_details.get('error_type', 'unknown')}
- **Error Message:** {error_message}
- **Status Code:** {error_details.get('status_code', 'N/A')}
- **Additional Details:** {json.dumps({k: v for k, v in error_details.items() if k not in ['operation', 'error_type', 'status_code']}, indent=2)}

---

"""

    async with aiofiles.open("logs/error_log.md", "a", encoding="utf-8") as log_file:
        await log_file.write(log_entry)


async def update_dashboard_error_count():
    """Update the dashboard error count"""
    try:
        # Read existing dashboard data or create new one
        dashboard_file = Path("dashboard.json")

        if dashboard_file.exists():
            async with aiofiles.open(dashboard_file, 'r', encoding='utf-8') as f:
                dashboard_data = json.loads(await f.read())
        else:
            dashboard_data = {
                "total_errors": 0,
                "recent_errors": [],
                "last_updated": None
            }

        # Increment error count
        dashboard_data["total_errors"] = dashboard_data.get("total_errors", 0) + 1

        # Add to recent errors (keep last 10)
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "MCP_Failure"
        }

        recent_errors = dashboard_data.get("recent_errors", [])
        recent_errors.insert(0, error_entry)
        dashboard_data["recent_errors"] = recent_errors[:10]  # Keep only last 10

        dashboard_data["last_updated"] = datetime.now().isoformat()

        # Write back to file
        async with aiofiles.open(dashboard_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(dashboard_data, indent=2))

    except Exception as e:
        # If dashboard update fails, log but don't crash
        print(f"Warning: Could not update dashboard error count: {e}")


def mark_task_as_partially_completed(task_id: str, completed_steps: list, failed_steps: list):
    """
    Mark a task as partially completed due to errors

    Args:
        task_id: The ID of the task
        completed_steps: List of steps that were completed successfully
        failed_steps: List of steps that failed
    """
    try:
        # Create tasks directory if it doesn't exist
        tasks_dir = Path("tasks")
        tasks_dir.mkdir(exist_ok=True)

        task_status_file = tasks_dir / f"{task_id}_status.json"

        status_data = {
            "task_id": task_id,
            "status": "partially_completed",
            "completed_steps": completed_steps,
            "failed_steps": failed_steps,
            "completion_percentage": len(completed_steps) / (len(completed_steps) + len(failed_steps)) * 100 if (len(completed_steps) + len(failed_steps)) > 0 else 0,
            "timestamp": datetime.now().isoformat()
        }

        with open(task_status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2)

    except Exception as e:
        # If task status update fails, log but don't crash
        print(f"Warning: Could not update task status: {e}")


async def execute_with_recovery(
    mcp_endpoint: str,
    payload: Dict[str, Any],
    mcp_base_url: str = None
) -> Dict[str, Any]:
    """
    Execute an MCP operation with built-in recovery

    Args:
        mcp_endpoint: The endpoint to call (e.g., '/create_invoice')
        payload: The request payload
        mcp_base_url: Base URL for the MCP server

    Returns:
        Structured response with status and results
    """
    if mcp_base_url is None:
        # Try to get from environment or default
        mcp_base_url = os.getenv("DEFAULT_MCP_BASE_URL", "http://localhost:8000")

    async def mcp_call():
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{mcp_base_url}{mcp_endpoint}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()
            result = response.json()

            # Standardize response format if needed
            if not isinstance(result, dict):
                result = {"success": True, "data": result}
            elif "success" not in result:
                result["success"] = True

            return result

    return await error_recovery_skill(mcp_call)


# Example wrapper functions for common MCP operations

async def recoverable_create_invoice(invoice_data: Dict[str, Any], mcp_base_url: str = None) -> Dict[str, Any]:
    """Wrapper for creating invoices with error recovery"""
    return await execute_with_recovery("/create_invoice", invoice_data, mcp_base_url)


async def recoverable_post_social_message(message_data: Dict[str, Any], mcp_base_url: str = None) -> Dict[str, Any]:
    """Wrapper for posting social messages with error recovery"""
    return await execute_with_recovery("/post_message", message_data, mcp_base_url)


async def recoverable_fetch_metrics(metrics_data: Dict[str, Any], mcp_base_url: str = None) -> Dict[str, Any]:
    """Wrapper for fetching metrics with error recovery"""
    endpoint = "/fetch_engagement_metrics" if "post_id" in metrics_data else "/fetch_profit_loss"
    return await execute_with_recovery(endpoint, metrics_data, mcp_base_url)


# Example usage function
async def example_usage():
    """Example of how to use the error recovery skill"""

    # Example: Recoverable invoice creation
    invoice_data = {
        "partner_id": 1,
        "product_ids": [1, 2],
        "quantities": [1, 2],
        "prices": [100.0, 50.0],
        "reference": "INV-001"
    }

    result = await recoverable_create_invoice(invoice_data)

    if result["status"] == "success":
        print(f"Invoice created successfully: {result['result']}")
    else:
        print(f"Invoice creation failed: {result['error']}")
        print(f"Attempted {result['attempts']} times")

        # Mark as partially completed if applicable
        if "invoice_id" in result.get("result", {}):
            mark_task_as_partially_completed(
                task_id="invoice_task_123",
                completed_steps=["validation", "creation"],
                failed_steps=["posting"]
            )

    return result


if __name__ == "__main__":
    # Example execution
    result = asyncio.run(example_usage())
    print(json.dumps(result, indent=2))