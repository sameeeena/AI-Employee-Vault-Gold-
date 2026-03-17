"""
Enhanced Logging Template for Gold Tier Implementation

This template shows how to implement the Gold Tier logging standards
in any skill or service.
"""

import json
import hashlib
import aiofiles
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


async def enhanced_log_entry(
    log_type: str,
    task_id: str,
    domain: str,
    skill_used: str,
    action_taken: str,
    result: str,
    error: str = None,
    details: dict = None,
    execution_time: float = None
):
    """
    Enhanced logging function with Gold Tier standards

    Args:
        log_type: Type of log (ACTION_LOG, DECISION_LOG, CYCLE_LOG, ERROR_LOG, AUDIT_LOG)
        task_id: Unique identifier for the task
        domain: Domain classification
        skill_used: Name of the skill performing the action
        action_taken: Description of the action performed
        result: Outcome (success, failure, partial_success)
        error: Error message if any
        details: Additional contextual information
        execution_time: Time taken to execute the action in milliseconds
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    correlation_id = hashlib.md5(f"{timestamp}_{task_id}".encode()).hexdigest()[:12]

    log_entry = f"""## {log_type} - {timestamp}
- **Task ID:** {task_id}
- **Domain:** {domain}
- **Skill:** {skill_used}
- **Action:** {action_taken}
- **Result:** {result}
- **Timestamp:** {timestamp}
- **Correlation ID:** {correlation_id}
"""

    if execution_time is not None:
        log_entry += f"- **Duration (ms):** {execution_time:.2f}\n"

    log_entry += "\n### Details\n"

    if details:
        for key, value in details.items():
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, default=str, indent=2)[:1000]  # Limit length
                log_entry += f"- **{key.title()}:** {value_str}\n"
            else:
                log_entry += f"- **{key.title()}:** {str(value)[:500]}\n"
    else:
        log_entry += "- **Info:** No additional details\n"

    if error:
        log_entry += f"""
### Errors
- **Error Type:** {type(error).__name__ if hasattr(error, '__class__') else 'Unknown'}
- **Error Message:** {str(error)[:500]}
"""

    log_entry += "\n---\n"

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Write to appropriate log file based on log_type
    log_filename = f"logs/{log_type.lower().replace('_log', '')}.md"

    try:
        async with aiofiles.open(log_filename, "a", encoding="utf-8") as log_file:
            await log_file.write(log_entry)
    except Exception as e:
        # Fallback logging to console if file logging fails
        print(f"Logging failed: {e}")
        print(log_entry)


# Example implementation in a skill
async def example_skill_with_gold_logging(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Example of how to implement Gold Tier logging in a skill
    """
    start_time = datetime.now()
    task_id = task_data.get("task_id", "unknown")
    domain = task_data.get("domain", "unknown")

    try:
        # Perform the actual skill operation
        result = await perform_skill_operation(task_data)

        execution_time = (datetime.now() - start_time).total_seconds() * 1000

        # Log successful execution
        await enhanced_log_entry(
            log_type="ACTION_LOG",
            task_id=task_id,
            domain=domain,
            skill_used="example_skill",
            action_taken="Processed task data",
            result="success",
            details={
                "input_size": len(json.dumps(task_data)),
                "result_keys": list(result.keys()) if isinstance(result, dict) else type(result).__name__,
                "processed_items": result.get("count", len(result)) if isinstance(result, (list, dict)) else 1
            },
            execution_time=execution_time
        )

        return {
            "success": True,
            "result": result,
            "task_id": task_id
        }

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds() * 1000

        # Log failed execution
        await enhanced_log_entry(
            log_type="ERROR_LOG",
            task_id=task_id,
            domain=domain,
            skill_used="example_skill",
            action_taken="Attempted to process task data",
            result="failure",
            error=str(e),
            details={
                "input_data_preview": str(task_data)[:200],
                "exception_type": type(e).__name__
            },
            execution_time=execution_time
        )

        return {
            "success": False,
            "error": str(e),
            "task_id": task_id
        }


async def perform_skill_operation(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Placeholder for actual skill operation
    """
    # Simulate some processing
    await asyncio.sleep(0.1)  # Simulate async work

    return {
        "processed": True,
        "data": task_data,
        "timestamp": datetime.now().isoformat()
    }


# Example of RALPH Loop specific logging
async def ralph_phase_log(phase_name: str, task_id: str, state: Dict[str, Any]):
    """
    Specialized logging for RALPH loop phases
    """
    await enhanced_log_entry(
        log_type="CYCLE_LOG",
        task_id=task_id,
        domain=state.get("domain", "unknown"),
        skill_used="ralph_loop_skill",
        action_taken=f"RALPH {phase_name.upper()} phase executed",
        result="success",
        details={
            "phase": phase_name,
            "current_step": state.get("current_step", 0),
            "total_steps": len(state.get("sub_tasks", [])),
            "progress_percentage": state.get("progress", 0),
            "iteration_count": state.get("iteration_count", 0)
        }
    )


# Example of decision-specific logging
async def decision_log(task_id: str, decision_data: Dict[str, Any], domain: str):
    """
    Specialized logging for decision-making processes
    """
    await enhanced_log_entry(
        log_type="DECISION_LOG",
        task_id=task_id,
        domain=domain,
        skill_used="domain_router_skill",
        action_taken="Decision made in decision-making process",
        result="success",
        details=decision_data
    )