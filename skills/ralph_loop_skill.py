"""
RALPH Loop Skill

Implements the Observe → Think → Plan → Act → Reflect → Adjust → Repeat cycle
for autonomous task execution with domain routing integration.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid
import aiofiles
from pathlib import Path

from domain_router_skill import domain_router_skill


class RalphState:
    """Manages the state of the RALPH loop"""

    def __init__(self, state_file: str = "state/ralph_state.json"):
        self.state_file = state_file
        self.state_dir = Path(state_file).parent
        self.state_dir.mkdir(parents=True, exist_ok=True)

    async def load_state(self) -> Dict[str, Any]:
        """Load the current state from file"""
        try:
            if os.path.exists(self.state_file):
                async with aiofiles.open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.loads(await f.read())
            else:
                return self.get_default_state()
        except Exception as e:
            print(f"Error loading state: {e}")
            return self.get_default_state()

    async def save_state(self, state: Dict[str, Any]):
        """Save the current state to file"""
        try:
            async with aiofiles.open(self.state_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(state, indent=2, default=str))
        except Exception as e:
            print(f"Error saving state: {e}")

    def get_default_state(self) -> Dict[str, Any]:
        """Get default state structure"""
        return {
            "current_task": "",
            "sub_tasks": [],
            "current_step": 0,
            "iteration_count": 0,
            "max_iterations": 50,  # Safe iteration limit
            "progress": {},
            "failed_steps": [],
            "adaptation_history": [],
            "last_action_result": None,
            "domain": "",
            "recommended_skill": ""
        }


class RalphLoopSkill:
    """Implements the complete RALPH loop cycle"""

    def __init__(self):
        self.state_manager = RalphState()
        self.max_iterations = 50

    async def observe(self, task_description: str) -> Dict[str, Any]:
        """Observe the environment and current task"""
        state = await self.state_manager.load_state()

        observation = {
            "timestamp": datetime.now().isoformat(),
            "task_description": task_description,
            "current_state": state.copy(),
            "available_tools": [
                "domain_router_skill",
                "accounting_mcp_server",
                "social_mcp_server",
                "weekly_business_audit_skill"
            ]
        }

        # Route task to appropriate domain
        domain_input = {
            "task_id": f"observe_{uuid.uuid4().hex[:8]}",
            "content": task_description,
            "metadata": {"phase": "observe"},
            "sender": "ralph_loop"
        }

        domain_result = domain_router_skill(domain_input)
        domain_data = json.loads(domain_result)

        observation["domain_classification"] = domain_data

        # Update state with domain info
        state["domain"] = domain_data["domain"]
        state["recommended_skill"] = domain_data["recommended_skill"]
        await self.state_manager.save_state(state)

        return observation

    async def think(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Think about the task and plan approach"""
        state = await self.state_manager.load_state()

        thinking = {
            "timestamp": datetime.now().isoformat(),
            "observation": observation,
            "analysis": {
                "task_complexity": "high" if len(observation["task_description"]) > 100 else "medium" if len(observation["task_description"]) > 50 else "low",
                "estimated_subtasks": max(1, len(observation["task_description"].split()) // 10),
                "domain": observation["domain_classification"]["domain"],
                "confidence": observation["domain_classification"]["confidence_score"]
            }
        }

        return thinking

    async def plan(self, thinking: Dict[str, Any], original_task: str) -> Dict[str, Any]:
        """Create a plan with sub-tasks"""
        state = await self.state_manager.load_state()

        # Break complex task into sub-tasks
        sub_tasks = self.break_into_subtasks(original_task, thinking["analysis"]["estimated_subtasks"])

        plan = {
            "timestamp": datetime.now().isoformat(),
            "original_task": original_task,
            "sub_tasks": sub_tasks,
            "total_steps": len(sub_tasks),
            "current_step": 0,
            "domain": thinking["analysis"]["domain"]
        }

        # Update state with plan
        state["current_task"] = original_task
        state["sub_tasks"] = sub_tasks
        state["current_step"] = 0
        state["progress"] = {f"step_{i}": "pending" for i in range(len(sub_tasks))}
        await self.state_manager.save_state(state)

        return plan

    def break_into_subtasks(self, task: str, estimated_count: int) -> List[Dict[str, Any]]:
        """Break a complex task into smaller sub-tasks"""
        # Simple breakdown based on task content
        sub_tasks = []

        # Split by common task indicators
        parts = []
        if "and" in task.lower():
            parts = task.split(" and ")
        elif "," in task:
            parts = task.split(", ")
        else:
            # Break into chunks if it's a long task
            words = task.split()
            chunk_size = max(1, len(words) // estimated_count)
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i+chunk_size])
                parts.append(chunk)

        for i, part in enumerate(parts):
            sub_tasks.append({
                "id": f"subtask_{i+1}",
                "description": part.strip(),
                "depends_on": [f"subtask_{i}"] if i > 0 else [],
                "domain": self.estimate_domain(part),
                "estimated_duration": "short"
            })

        return sub_tasks

    def estimate_domain(self, task_part: str) -> str:
        """Estimate the domain for a task part"""
        task_lower = task_part.lower()

        if any(word in task_lower for word in ["finance", "money", "account", "tax", "expense", "revenue", "profit", "invoice", "payment"]):
            return "Accounting"
        elif any(word in task_lower for word in ["social", "facebook", "twitter", "instagram", "post", "share", "like", "follow"]):
            return "Social Media"
        elif any(word in task_lower for word in ["business", "company", "meeting", "project", "client", "work"]):
            return "Business"
        else:
            return "Personal"

    async def act(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the current sub-task"""
        state = await self.state_manager.load_state()

        if state["current_step"] >= len(state["sub_tasks"]):
            # All sub-tasks completed
            result = {
                "status": "completed",
                "message": "All sub-tasks completed successfully",
                "completed_tasks": state["sub_tasks"]
            }
            return result

        current_subtask = state["sub_tasks"][state["current_step"]]

        # Execute based on domain
        try:
            if current_subtask["domain"] == "Accounting":
                result = await self.execute_accounting_task(current_subtask)
            elif current_subtask["domain"] == "Social Media":
                result = await self.execute_social_task(current_subtask)
            elif current_subtask["domain"] == "Business":
                result = await self.execute_business_task(current_subtask)
            else:  # Personal
                result = await self.execute_personal_task(current_subtask)

            # Update progress
            state["progress"][f"step_{state['current_step']}"] = "completed"
            state["last_action_result"] = result
            await self.state_manager.save_state(state)

            action_result = {
                "status": "success",
                "subtask_id": current_subtask["id"],
                "result": result,
                "next_step": state["current_step"] + 1
            }

        except Exception as e:
            # Mark as failed, possibly retry
            state["progress"][f"step_{state['current_step']}"] = "failed"
            state["failed_steps"].append({
                "step": state["current_step"],
                "error": str(e),
                "retry_count": state["progress"].get(f"retry_{state['current_step']}", 0)
            })

            if state["progress"].get(f"retry_{state['current_step']}", 0) < 1:
                # First failure, mark for retry
                state["progress"][f"retry_{state['current_step']}"] = 1
                action_result = {
                    "status": "retry",
                    "subtask_id": current_subtask["id"],
                    "error": str(e),
                    "retry_attempt": 1
                }
            else:
                # Second failure, need to adapt plan
                action_result = {
                    "status": "failed",
                    "subtask_id": current_subtask["id"],
                    "error": str(e),
                    "requires_adaptation": True
                }

            state["last_action_result"] = action_result
            await self.state_manager.save_state(state)

        return action_result

    async def execute_accounting_task(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an accounting-related sub-task"""
        # This would integrate with accounting_mcp_server
        # For now, simulating the call
        return {
            "executed_task": subtask["description"],
            "domain": "Accounting",
            "simulated_result": "Accounting operation completed"
        }

    async def execute_social_task(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a social media-related sub-task"""
        # This would integrate with social_mcp_server
        # For now, simulating the call
        return {
            "executed_task": subtask["description"],
            "domain": "Social Media",
            "simulated_result": "Social media operation completed"
        }

    async def execute_business_task(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a business-related sub-task"""
        return {
            "executed_task": subtask["description"],
            "domain": "Business",
            "simulated_result": "Business operation completed"
        }

    async def execute_personal_task(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a personal-related sub-task"""
        return {
            "executed_task": subtask["description"],
            "domain": "Personal",
            "simulated_result": "Personal task completed"
        }

    async def reflect(self, action_result: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on the action results"""
        state = await self.state_manager.load_state()

        reflection = {
            "timestamp": datetime.now().isoformat(),
            "action_result": action_result,
            "current_iteration": state["iteration_count"],
            "overall_progress": self.calculate_progress(state),
            "success_rate": self.calculate_success_rate(state),
            "needs_adjustment": action_result.get("requires_adaptation", False) or action_result.get("status") == "failed"
        }

        return reflection

    def calculate_progress(self, state: Dict[str, Any]) -> float:
        """Calculate overall progress percentage"""
        total_steps = len(state["sub_tasks"])
        if total_steps == 0:
            return 0.0

        completed = sum(1 for status in state["progress"].values() if status == "completed")
        return round((completed / total_steps) * 100, 2)

    def calculate_success_rate(self, state: Dict[str, Any]) -> float:
        """Calculate success rate of completed steps"""
        completed_steps = [k for k, v in state["progress"].items() if v == "completed" and not k.startswith("retry_")]
        failed_steps = [k for k, v in state["progress"].items() if v == "failed" and not k.startswith("retry_")]

        total_attempted = len(completed_steps) + len(failed_steps)
        if total_attempted == 0:
            return 100.0

        return round((len(completed_steps) / total_attempted) * 100, 2)

    async def adjust(self, reflection: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust the plan based on reflection"""
        adjustment = {
            "timestamp": datetime.now().isoformat(),
            "reflection": reflection,
            "adjustments_made": [],
            "new_plan": state["sub_tasks"].copy()
        }

        if reflection["needs_adjustment"]:
            # Log the adaptation
            adaptation_record = {
                "timestamp": datetime.now().isoformat(),
                "reason": "Failed step requiring plan adjustment",
                "original_plan": state["sub_tasks"].copy(),
                "failed_step": state["current_step"]
            }

            state["adaptation_history"].append(adaptation_record)

            # Modify the plan - skip failed step or modify approach
            if state["current_step"] < len(state["sub_tasks"]):
                # Mark current step as skipped and move to next
                adjustment["adjustments_made"].append(f"Skipping step {state['current_step']} due to repeated failure")

                # Move to next step
                state["current_step"] += 1

        # Update state with adjustments
        await self.state_manager.save_state(state)

        return adjustment

    async def log_cycle(self, cycle_data: Dict[str, Any]):
        """Log the entire cycle to decision_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"""
## RALPH Loop Cycle - {timestamp}
- **Iteration:** {cycle_data.get('iteration', 0)}
- **Phase:** {cycle_data.get('phase', 'unknown')}
- **Task:** {cycle_data.get('task', '')[:100]}...
- **Status:** {cycle_data.get('status', 'running')}
- **Progress:** {cycle_data.get('progress', 0)}%
- **Current Step:** {cycle_data.get('current_step', 0)}
- **Domain:** {cycle_data.get('domain', 'unknown')}

"""

        async with aiofiles.open("decision_log.md", "a", encoding="utf-8") as log_file:
            await log_file.write(log_entry)

    async def run_complete_cycle(self, task_description: str) -> Dict[str, Any]:
        """Run one complete cycle of Observe → Think → Plan → Act → Reflect → Adjust"""
        state = await self.state_manager.load_state()

        # Increment iteration count
        state["iteration_count"] += 1
        await self.state_manager.save_state(state)

        if state["iteration_count"] > state["max_iterations"]:
            return {"status": "stopped", "reason": "Max iterations reached", "final_state": state}

        # Observe
        observation = await self.observe(task_description)
        await self.log_cycle({
            "iteration": state["iteration_count"],
            "phase": "observe",
            "task": task_description,
            "status": "completed",
            "progress": self.calculate_progress(state),
            "current_step": state["current_step"],
            "domain": state["domain"]
        })

        # Think
        thinking = await self.think(observation)
        await self.log_cycle({
            "iteration": state["iteration_count"],
            "phase": "think",
            "task": task_description,
            "status": "completed",
            "progress": self.calculate_progress(state),
            "current_step": state["current_step"],
            "domain": state["domain"]
        })

        # Plan (only on first iteration or when needed)
        if state["sub_tasks"] == []:
            plan = await self.plan(thinking, task_description)
            await self.log_cycle({
                "iteration": state["iteration_count"],
                "phase": "plan",
                "task": task_description,
                "status": "completed",
                "progress": self.calculate_progress(state),
                "current_step": state["current_step"],
                "domain": state["domain"]
            })
        else:
            plan = {
                "original_task": state["current_task"],
                "sub_tasks": state["sub_tasks"],
                "current_step": state["current_step"]
            }

        # Act
        action_result = await self.act(plan)
        await self.log_cycle({
            "iteration": state["iteration_count"],
            "phase": "act",
            "task": task_description,
            "status": action_result["status"],
            "progress": self.calculate_progress(state),
            "current_step": state["current_step"],
            "domain": state["domain"]
        })

        # Update current step if successful
        if action_result["status"] == "success":
            state = await self.state_manager.load_state()
            state["current_step"] += 1
            await self.state_manager.save_state(state)
        elif action_result["status"] == "retry":
            # Stay on same step for retry
            pass
        elif action_result["status"] == "failed" and action_result.get("requires_adaptation"):
            # Adjust plan due to failure
            reflection = await self.reflect(action_result)
            state = await self.state_manager.load_state()
            await self.adjust(reflection, state)

        # Reflect
        reflection = await self.reflect(action_result)
        await self.log_cycle({
            "iteration": state["iteration_count"],
            "phase": "reflect",
            "task": task_description,
            "status": "completed",
            "progress": self.calculate_progress(state),
            "current_step": state["current_step"],
            "domain": state["domain"]
        })

        # Check if all tasks are completed
        state = await self.state_manager.load_state()
        if state["current_step"] >= len(state["sub_tasks"]):
            return {
                "status": "completed",
                "message": "All sub-tasks completed",
                "final_state": state,
                "results": state["last_action_result"]
            }

        return {
            "status": "continue",
            "current_step": state["current_step"],
            "progress": self.calculate_progress(state),
            "total_steps": len(state["sub_tasks"]),
            "state": state
        }


async def ralph_loop_skill(task_description: str) -> str:
    """
    Main entry point for the RALPH loop skill.

    Args:
        task_description: The complex task to be broken down and executed

    Returns:
        JSON string with the result of the operation
    """
    ralph = RalphLoopSkill()

    # Run cycles until completion or limit reached
    result = None
    while True:
        result = await ralph.run_complete_cycle(task_description)

        if result["status"] in ["completed", "stopped"]:
            break
        elif result["status"] == "continue":
            # Continue to next cycle
            continue
        else:
            # Some other status, check if we should continue
            state = await ralph.state_manager.load_state()
            if state["iteration_count"] > state["max_iterations"]:
                result = {"status": "stopped", "reason": "Max iterations reached"}
                break

    return json.dumps(result, indent=2, default=str)


# Example usage
if __name__ == "__main__":
    # Example of how to run the skill
    sample_task = "Process monthly accounting entries and create social media campaign for new product launch"

    async def run_example():
        result = await ralph_loop_skill(sample_task)
        print("RALPH Loop Result:")
        print(result)

    asyncio.run(run_example())