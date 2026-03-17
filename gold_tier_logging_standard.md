# Gold Tier Logging Standards

## Overview
The Gold tier logging system provides comprehensive, structured logging for all system activities with enhanced traceability and audit capabilities.

## Standard Log Entry Format
Every action must include these mandatory fields:

```markdown
## [LOG_TYPE] - [TIMESTAMP]
- **Task ID:** [task_id]
- **Domain:** [domain]
- **Skill:** [skill_used]
- **Action:** [action_taken]
- **Result:** [success|failure|partial_success]
- **Timestamp:** [YYYY-MM-DD HH:MM:SS.mmm]
- **Correlation ID:** [unique_correlation_id]

### Details
- **Input:** [input_parameters]
- **Output:** [output_result]
- **Duration:** [execution_time_ms]
- **User Context:** [user_context_if_available]

### Errors (if any)
- **Error Type:** [error_type]
- **Error Message:** [error_message]
- **Stack Trace:** [stack_trace_if_applicable]

---
```

## Log Types
- `ACTION_LOG` - For standard skill executions
- `DECISION_LOG` - For domain routing and decision-making
- `CYCLE_LOG` - For RALPH loop cycle phases
- `ERROR_LOG` - For error events and recovery
- `AUDIT_LOG` - For business audits and reports

## Enhanced Skill Logging Template
```python
async def enhanced_log_entry(
    log_type: str,
    task_id: str,
    domain: str,
    skill_used: str,
    action_taken: str,
    result: str,
    error: str = None,
    details: dict = None
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    correlation_id = hashlib.md5(f"{timestamp}_{task_id}".encode()).hexdigest()[:12]

    log_entry = f"""
## {log_type} - {timestamp}
- **Task ID:** {task_id}
- **Domain:** {domain}
- **Skill:** {skill_used}
- **Action:** {action_taken}
- **Result:** {result}
- **Timestamp:** {timestamp}
- **Correlation ID:** {correlation_id}

### Details
"""

    if details:
        for key, value in details.items():
            log_entry += f"- **{key.title()}:** {json.dumps(value, default=str)[:500]}\n"

    if error:
        log_entry += f"""
### Errors
- **Error:** {error}
"""

    log_entry += "\n---\n"

    # Write to appropriate log file based on log_type
    log_filename = f"logs/{log_type.lower().replace('_log', '')}.md"
    async with aiofiles.open(log_filename, "a", encoding="utf-8") as log_file:
        await log_file.write(log_entry)
```

## Updated Skill Implementations
Each skill must now use the enhanced logging with mandatory fields:

### For Domain Router Skill:
- Log type: DECISION_LOG
- Domain: Based on classification result
- Action: "Domain classification performed"
- Result: Classification outcome

### For MCP Servers:
- Log type: ACTION_LOG
- Domain: Pre-determined for server
- Action: Specific API operation
- Result: API call outcome

### For RALPH Loop:
- Each phase gets CYCLE_LOG
- Decision steps logged separately as DECISION_LOG
- Sub-task executions as ACTION_LOG

### For Error Recovery:
- Log type: ERROR_LOG
- Action: "Error recovery attempted"
- Result: Recovery outcome
- Include original error details

## Correlation Tracking
All related logs share correlation IDs to enable traceability across the system lifecycle of a task.