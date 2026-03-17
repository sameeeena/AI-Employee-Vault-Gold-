"""
Ralph Wiggum Loop - Autonomous Multi-Step Task Completion

An autonomous agent system that iteratively completes complex multi-step tasks
through continuous loops of: Plan → Execute → Validate → Correct → Complete

Named after Ralph Wiggum's persistent approach: "Me fail English? That's unpossible!"

Key Features:
- Autonomous task decomposition
- Iterative execution with validation
- Self-correction on failures
- Progress tracking
- Multi-agent coordination
- Goal-oriented completion

Usage:
    python ralph_loop.py --task "Your complex task here"
    python ralph_loop.py --demo                      # Run demo
    python ralph_loop.py --status                    # Check status
    python ralph_loop.py --monitor                   # Monitor running loops
"""

import asyncio
import json
import os
import sys
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field, asdict
import logging
import aiofiles
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============== Enums & Data Classes ==============

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    WAITING_VALIDATION = "waiting_validation"
    NEEDS_CORRECTION = "needs_correction"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class LoopPhase(Enum):
    """Ralph Loop phases"""
    PLAN = "plan"
    EXECUTE = "execute"
    VALIDATE = "validate"
    CORRECT = "correct"
    COMPLETE = "complete"


@dataclass
class SubTask:
    """Represents a sub-task in the decomposition"""
    task_id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_agent: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "status": self.status.value,
            "priority": self.priority.value
        }


@dataclass
class TaskIteration:
    """Represents one iteration of the Ralph Loop"""
    iteration_number: int
    phase: LoopPhase
    timestamp: str
    action: str
    result: Any
    validation_status: Optional[bool] = None
    correction_needed: bool = False
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "iteration_number": self.iteration_number,
            "phase": self.phase.value,
            "timestamp": self.timestamp,
            "action": self.action,
            "result": self.result,
            "validation_status": self.validation_status,
            "correction_needed": self.correction_needed,
            "notes": self.notes
        }


@dataclass
class RalphTask:
    """Main task object for Ralph Loop"""
    task_id: str
    goal: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    subtasks: List[SubTask] = field(default_factory=list)
    iterations: List[TaskIteration] = field(default_factory=list)
    current_iteration: int = 0
    max_iterations: int = 20
    progress_percentage: float = 0.0
    validation_results: List[Dict] = field(default_factory=list)
    corrections: List[Dict] = field(default_factory=list)
    final_result: Optional[Any] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "status": self.status.value,
            "priority": self.priority.value,
            "subtasks": [st.to_dict() for st in self.subtasks],
            "iterations": [it.to_dict() for it in self.iterations]
        }


# ============== Task Decomposition Engine ==============

class TaskDecompositionEngine:
    """
    Breaks down complex tasks into manageable subtasks.
    """
    
    def __init__(self):
        self.decomposition_strategies = {
            "sequential": self._decompose_sequential,
            "parallel": self._decompose_parallel,
            "hierarchical": self._decompose_hierarchical,
            "dependency_based": self._decompose_dependency_based
        }
    
    async def decompose(self, task: RalphTask, strategy: str = "sequential") -> List[SubTask]:
        """Decompose task into subtasks"""
        decomposer = self.decomposition_strategies.get(strategy, self._decompose_sequential)
        return await decomposer(task)
    
    async def _decompose_sequential(self, task: RalphTask) -> List[SubTask]:
        """Decompose into sequential steps"""
        subtasks = []
        
        # Generic sequential decomposition
        phases = [
            ("analyze", "Analyze requirements and gather information"),
            ("plan", "Create detailed plan and approach"),
            ("prepare", "Prepare resources and dependencies"),
            ("execute", "Execute main task components"),
            ("verify", "Verify results and quality"),
            ("finalize", "Finalize and document completion")
        ]
        
        for i, (phase_name, description) in enumerate(phases):
            subtask = SubTask(
                task_id=f"{task.task_id}_step_{i+1}",
                description=f"{phase_name.capitalize()}: {description}",
                priority=TaskPriority.MEDIUM,
                dependencies=[f"{task.task_id}_step_{i}"] if i > 0 else []
            )
            subtasks.append(subtask)
        
        return subtasks
    
    async def _decompose_parallel(self, task: RalphTask) -> List[SubTask]:
        """Decompose into parallel tasks"""
        subtasks = []
        
        # Identify parallelizable components
        components = [
            ("research", "Research and information gathering"),
            ("development", "Development and implementation"),
            ("testing", "Testing and quality assurance"),
            ("documentation", "Documentation and reporting")
        ]
        
        for i, (comp_name, description) in enumerate(components):
            subtask = SubTask(
                task_id=f"{task.task_id}_parallel_{i+1}",
                description=f"{comp_name.capitalize()}: {description}",
                priority=TaskPriority.MEDIUM,
                dependencies=[]  # No dependencies for parallel tasks
            )
            subtasks.append(subtask)
        
        return subtasks
    
    async def _decompose_hierarchical(self, task: RalphTask) -> List[SubTask]:
        """Decompose into hierarchical tree"""
        # Top-level phases
        phases = [
            ("initiation", "Project initiation"),
            ("planning", "Detailed planning"),
            ("execution", "Task execution"),
            ("monitoring", "Monitoring and control"),
            ("closure", "Project closure")
        ]
        
        subtasks = []
        for i, (phase, description) in enumerate(phases):
            subtask = SubTask(
                task_id=f"{task.task_id}_phase_{i+1}",
                description=f"{phase.capitalize()}: {description}",
                priority=TaskPriority.HIGH if i == 2 else TaskPriority.MEDIUM,
                dependencies=[f"{task.task_id}_phase_{i}"] if i > 0 else []
            )
            subtasks.append(subtask)
        
        return subtasks
    
    async def _decompose_dependency_based(self, task: RalphTask) -> List[SubTask]:
        """Decompose based on dependencies"""
        # Critical path method
        critical_tasks = [
            ("requirements", "Requirements analysis", []),
            ("design", "System design", ["requirements"]),
            ("implementation", "Implementation", ["design"]),
            ("testing", "Testing", ["implementation"]),
            ("deployment", "Deployment", ["testing"])
        ]
        
        subtasks = []
        for i, (name, description, deps) in enumerate(critical_tasks):
            subtask = SubTask(
                task_id=f"{task.task_id}_critical_{i+1}",
                description=f"{name.capitalize()}: {description}",
                priority=TaskPriority.HIGH,
                dependencies=[f"{task.task_id}_critical_{j+1}" for j, _ in enumerate(critical_tasks[:i]) if f"{task.task_id}_critical_{j+1}" in [f"{task.task_id}_critical_{k+1}" for k in range(len(deps))]]
            )
            subtasks.append(subtask)
        
        return subtasks


# ============== Progress Tracker ==============

class ProgressTracker:
    """
    Tracks and validates task progress.
    """
    
    def __init__(self):
        self.validation_rules: List[Dict] = []
        self.progress_history: List[Dict] = []
    
    def calculate_progress(self, task: RalphTask) -> float:
        """Calculate overall task progress"""
        if not task.subtasks:
            return 0.0
        
        completed = sum(1 for st in task.subtasks if st.status == TaskStatus.COMPLETED)
        failed = sum(1 for st in task.subtasks if st.status == TaskStatus.FAILED)
        
        # Weight: completed = 100%, in_progress = 50%, failed = 0%
        total_weight = 0
        earned_weight = 0
        
        for subtask in task.subtasks:
            weight = 1.0 / len(task.subtasks)
            total_weight += weight
            
            if subtask.status == TaskStatus.COMPLETED:
                earned_weight += weight
            elif subtask.status == TaskStatus.IN_PROGRESS:
                earned_weight += weight * 0.5
        
        progress = (earned_weight / total_weight * 100) if total_weight > 0 else 0.0
        task.progress_percentage = progress
        
        return progress
    
    async def validate_subtask(self, subtask: SubTask, result: Any) -> Tuple[bool, str]:
        """Validate subtask completion"""
        # Basic validation rules
        validations = [
            (result is not None, "Result is None"),
            (subtask.status != TaskStatus.FAILED, "Task failed"),
            (subtask.retry_count <= subtask.max_retries, "Max retries exceeded")
        ]
        
        failed_validations = [msg for condition, msg in validations if not condition]
        
        if failed_validations:
            return False, "; ".join(failed_validations)
        
        return True, "Validation passed"
    
    async def validate_task_completion(self, task: RalphTask) -> Tuple[bool, str]:
        """Validate if task is truly complete"""
        # Check all subtasks completed or cancelled
        incomplete = [st for st in task.subtasks if st.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]]
        
        if incomplete:
            return False, f"{len(incomplete)} subtasks incomplete"
        
        # Check progress is 100%
        self.calculate_progress(task)
        if task.progress_percentage < 100.0:
            return False, f"Progress at {task.progress_percentage}%"
        
        # Check no critical errors (HIGH priority failed tasks)
        critical_errors = [st for st in task.subtasks if st.status == TaskStatus.FAILED and st.priority == TaskPriority.HIGH]
        if critical_errors:
            return False, f"{len(critical_errors)} critical subtasks failed"
        
        # All checks passed
        return True, "All validation checks passed"
    
    def record_progress(self, task: RalphTask, phase: LoopPhase, result: Any):
        """Record progress snapshot"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "iteration": task.current_iteration,
            "phase": phase.value,
            "progress": task.progress_percentage,
            "status": task.status.value,
            "completed_subtasks": sum(1 for st in task.subtasks if st.status == TaskStatus.COMPLETED),
            "total_subtasks": len(task.subtasks)
        }
        self.progress_history.append(snapshot)
    
    def get_progress_report(self, task: RalphTask) -> Dict[str, Any]:
        """Generate progress report"""
        return {
            "task_id": task.task_id,
            "goal": task.goal,
            "status": task.status.value,
            "progress_percentage": task.progress_percentage,
            "current_iteration": task.current_iteration,
            "max_iterations": task.max_iterations,
            "subtasks": {
                "total": len(task.subtasks),
                "completed": sum(1 for st in task.subtasks if st.status == TaskStatus.COMPLETED),
                "in_progress": sum(1 for st in task.subtasks if st.status == TaskStatus.IN_PROGRESS),
                "pending": sum(1 for st in task.subtasks if st.status == TaskStatus.PENDING),
                "failed": sum(1 for st in task.subtasks if st.status == TaskStatus.FAILED)
            },
            "iterations": len(task.iterations),
            "corrections": len(task.corrections)
        }


# ============== Self-Correction Engine ==============

class SelfCorrectionEngine:
    """
    Analyzes failures and generates correction strategies.
    """
    
    def __init__(self):
        self.correction_strategies = {
            "retry": self._strategy_retry,
            "alternative_approach": self._strategy_alternative,
            "decompose_further": self._strategy_decompose,
            "seek_assistance": self._strategy_assistance,
            "skip_optional": self._strategy_skip
        }
        self.correction_history: List[Dict] = []
    
    async def analyze_failure(self, task: RalphTask, failed_subtask: SubTask) -> Dict[str, Any]:
        """Analyze failure and recommend correction"""
        analysis = {
            "task_id": task.task_id,
            "subtask_id": failed_subtask.task_id,
            "error": failed_subtask.error,
            "retry_count": failed_subtask.retry_count,
            "max_retries": failed_subtask.max_retries,
            "priority": failed_subtask.priority.value,
            "failure_pattern": self._identify_failure_pattern(failed_subtask),
            "recommended_strategy": await self._recommend_strategy(failed_subtask),
            "alternative_strategies": [],
            "confidence": 0.0
        }
        
        return analysis
    
    def _identify_failure_pattern(self, subtask: SubTask) -> str:
        """Identify pattern in failure"""
        if subtask.retry_count == 0:
            return "first_attempt_failure"
        elif subtask.retry_count < subtask.max_retries:
            return "repeated_failure"
        else:
            return "max_retries_exceeded"
    
    async def _recommend_strategy(self, subtask: SubTask) -> str:
        """Recommend correction strategy based on failure"""
        if subtask.retry_count < subtask.max_retries:
            return "retry"
        
        if subtask.priority == TaskPriority.LOW:
            return "skip_optional"
        
        if "timeout" in (subtask.error or "").lower():
            return "alternative_approach"
        
        if "decompose" in (subtask.error or "").lower():
            return "decompose_further"
        
        return "seek_assistance"
    
    async def apply_correction(self, task: RalphTask, subtask: SubTask, strategy: str) -> bool:
        """Apply correction strategy"""
        strategy_func = self.correction_strategies.get(strategy)
        
        if not strategy_func:
            logger.warning(f"Unknown correction strategy: {strategy}")
            return False
        
        return await strategy_func(task, subtask)
    
    async def _strategy_retry(self, task: RalphTask, subtask: SubTask) -> bool:
        """Retry the subtask"""
        if subtask.retry_count >= subtask.max_retries:
            return False
        
        subtask.retry_count += 1
        subtask.status = TaskStatus.PENDING
        subtask.error = None
        
        correction_record = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task.task_id,
            "subtask_id": subtask.task_id,
            "strategy": "retry",
            "retry_count": subtask.retry_count
        }
        self.correction_history.append(correction_record)
        task.corrections.append(correction_record)
        
        logger.info(f"Applied retry strategy to {subtask.task_id} (attempt {subtask.retry_count}/{subtask.max_retries})")
        return True
    
    async def _strategy_alternative(self, task: RalphTask, subtask: SubTask) -> bool:
        """Try alternative approach"""
        subtask.metadata["alternative_approach"] = True
        subtask.status = TaskStatus.PENDING
        subtask.retry_count += 1
        
        correction_record = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task.task_id,
            "subtask_id": subtask.task_id,
            "strategy": "alternative_approach",
            "description": "Switching to alternative approach"
        }
        self.correction_history.append(correction_record)
        task.corrections.append(correction_record)
        
        logger.info(f"Applied alternative approach to {subtask.task_id}")
        return True
    
    async def _strategy_decompose(self, task: RalphTask, subtask: SubTask) -> bool:
        """Decompose subtask further"""
        # Create smaller subtasks
        new_subtasks = [
            SubTask(
                task_id=f"{subtask.task_id}_part_{i+1}",
                description=f"Part {i+1} of: {subtask.description}",
                priority=subtask.priority,
                dependencies=[f"{subtask.task_id}_part_{i}"] if i > 0 else []
            )
            for i in range(3)
        ]
        
        # Replace original subtask with new ones
        subtask.status = TaskStatus.CANCELLED
        subtask.metadata["decomposed"] = True
        
        task.subtasks.extend(new_subtasks)
        
        correction_record = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task.task_id,
            "subtask_id": subtask.task_id,
            "strategy": "decompose_further",
            "new_subtasks": [st.task_id for st in new_subtasks]
        }
        self.correction_history.append(correction_record)
        task.corrections.append(correction_record)
        
        logger.info(f"Decomposed {subtask.task_id} into {len(new_subtasks)} smaller tasks")
        return True
    
    async def _strategy_assistance(self, task: RalphTask, subtask: SubTask) -> bool:
        """Request human assistance"""
        subtask.metadata["assistance_requested"] = True
        subtask.status = TaskStatus.WAITING_VALIDATION
        
        correction_record = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task.task_id,
            "subtask_id": subtask.task_id,
            "strategy": "seek_assistance",
            "description": "Human assistance required",
            "error": subtask.error
        }
        self.correction_history.append(correction_record)
        task.corrections.append(correction_record)
        
        logger.warning(f"Human assistance requested for {subtask.task_id}: {subtask.error}")
        return True
    
    async def _strategy_skip(self, task: RalphTask, subtask: SubTask) -> bool:
        """Skip optional subtask"""
        if subtask.priority == TaskPriority.HIGH:
            logger.warning(f"Cannot skip high priority task: {subtask.task_id}")
            return False
        
        subtask.status = TaskStatus.CANCELLED
        subtask.metadata["skipped"] = True
        
        correction_record = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task.task_id,
            "subtask_id": subtask.task_id,
            "strategy": "skip_optional",
            "reason": "Low priority task skipped after failures"
        }
        self.correction_history.append(correction_record)
        task.corrections.append(correction_record)
        
        logger.info(f"Skipped optional task: {subtask.task_id}")
        return True


# ============== Ralph Loop Orchestrator ==============

class RalphLoopOrchestrator:
    """
    Main orchestrator for the Ralph Wiggum Loop.
    Coordinates the iterative task completion process.
    """
    
    def __init__(self):
        self.decomposition_engine = TaskDecompositionEngine()
        self.progress_tracker = ProgressTracker()
        self.correction_engine = SelfCorrectionEngine()
        self.active_tasks: Dict[str, RalphTask] = {}
        self.completed_tasks: Dict[str, RalphTask] = {}
        self.logs_dir = Path("logs/ralph_loop")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    async def create_task(self, goal: str, description: str = "", priority: TaskPriority = TaskPriority.MEDIUM) -> RalphTask:
        """Create a new task for Ralph Loop"""
        task_id = f"ralph_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(goal.encode()).hexdigest()[:8]}"
        
        task = RalphTask(
            task_id=task_id,
            goal=goal,
            description=description or goal,
            priority=priority
        )
        
        # Decompose into subtasks
        task.subtasks = await self.decomposition_engine.decompose(task, strategy="sequential")
        
        self.active_tasks[task_id] = task
        
        # Log task creation
        await self._log_task_event(task, "TASK_CREATED", f"Created with {len(task.subtasks)} subtasks")
        
        logger.info(f"Created Ralph task: {task_id} - {goal[:50]}...")
        return task
    
    async def execute_loop(self, task_id: str) -> RalphTask:
        """Execute Ralph Loop for a task"""
        if task_id not in self.active_tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.active_tasks[task_id]
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now().isoformat()
        
        logger.info(f"Starting Ralph Loop for task: {task.task_id}")
        
        while task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            # Check iteration limit
            if task.current_iteration >= task.max_iterations:
                task.status = TaskStatus.FAILED
                task.error_message = "Max iterations exceeded"
                break
            
            task.current_iteration += 1
            
            # Phase 1: PLAN
            await self._plan_phase(task)
            
            # Phase 2: EXECUTE
            await self._execute_phase(task)
            
            # Phase 3: VALIDATE
            validation_result = await self._validate_phase(task)
            
            # Phase 4: CORRECT (if needed)
            if not validation_result[0]:
                await self._correct_phase(task, validation_result[1])
            else:
                # Phase 5: COMPLETE
                await self._complete_phase(task)
        
        # Task finished
        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            task.completed_at = datetime.now().isoformat()
            self.completed_tasks[task_id] = self.active_tasks.pop(task_id)
            await self._save_task_result(task)
        
        return task
    
    async def _plan_phase(self, task: RalphTask):
        """PLAN phase: Plan current iteration"""
        iteration = TaskIteration(
            iteration_number=task.current_iteration,
            phase=LoopPhase.PLAN,
            timestamp=datetime.now().isoformat(),
            action="Planning iteration",
            result={"subtasks_to_process": len([st for st in task.subtasks if st.status == TaskStatus.PENDING])}
        )
        task.iterations.append(iteration)
        
        self.progress_tracker.record_progress(task, LoopPhase.PLAN, iteration.result)
        logger.info(f"Iteration {task.current_iteration}: PLAN phase")
    
    async def _execute_phase(self, task: RalphTask):
        """EXECUTE phase: Execute pending subtasks"""
        pending_subtasks = [st for st in task.subtasks if st.status == TaskStatus.PENDING]
        
        for subtask in pending_subtasks:
            # Check dependencies
            if not self._check_dependencies(subtask, task.subtasks):
                continue
            
            subtask.status = TaskStatus.IN_PROGRESS
            subtask.started_at = datetime.now().isoformat()
            
            # Simulate execution (in real implementation, this would call actual agents/APIs)
            result = await self._execute_subtask(subtask)
            
            subtask.result = result
            subtask.completed_at = datetime.now().isoformat()
            
            if result.get("success", False):
                subtask.status = TaskStatus.COMPLETED
            else:
                subtask.status = TaskStatus.FAILED
                subtask.error = result.get("error", "Unknown error")
        
        iteration = TaskIteration(
            iteration_number=task.current_iteration,
            phase=LoopPhase.EXECUTE,
            timestamp=datetime.now().isoformat(),
            action="Executed subtasks",
            result={"executed": len(pending_subtasks)}
        )
        task.iterations.append(iteration)
        
        self.progress_tracker.record_progress(task, LoopPhase.EXECUTE, iteration.result)
        logger.info(f"Iteration {task.current_iteration}: EXECUTE phase - {len(pending_subtasks)} subtasks")
    
    async def _execute_subtask(self, subtask: SubTask) -> Dict[str, Any]:
        """Execute individual subtask"""
        # Simulate execution - in real implementation, this would:
        # - Call appropriate MCP server
        # - Execute specific function
        # - Use AI agent for complex tasks
        
        await asyncio.sleep(0.1)  # Simulate work
        
        # Simulate success (90% success rate for demo)
        import random
        success = random.random() > 0.1
        
        return {
            "success": success,
            "subtask_id": subtask.task_id,
            "message": "Executed successfully" if success else "Execution failed",
            "error": None if success else f"Simulated failure for {subtask.description}"
        }
    
    def _check_dependencies(self, subtask: SubTask, all_subtasks: List[SubTask]) -> bool:
        """Check if all dependencies are completed"""
        for dep_id in subtask.dependencies:
            dep_subtask = next((st for st in all_subtasks if st.task_id == dep_id), None)
            if not dep_subtask or dep_subtask.status != TaskStatus.COMPLETED:
                return False
        return True
    
    async def _validate_phase(self, task: RalphTask) -> Tuple[bool, str]:
        """VALIDATE phase: Validate progress"""
        is_complete, message = await self.progress_tracker.validate_task_completion(task)
        
        iteration = TaskIteration(
            iteration_number=task.current_iteration,
            phase=LoopPhase.VALIDATE,
            timestamp=datetime.now().isoformat(),
            action="Validated progress",
            result={"complete": is_complete, "message": message},
            validation_status=is_complete
        )
        task.iterations.append(iteration)
        task.validation_results.append({"iteration": task.current_iteration, "passed": is_complete, "message": message})
        
        self.progress_tracker.record_progress(task, LoopPhase.VALIDATE, iteration.result)
        logger.info(f"Iteration {task.current_iteration}: VALIDATE phase - {'PASSED' if is_complete else 'FAILED'}")
        
        if is_complete:
            task.status = TaskStatus.COMPLETED
            task.final_result = self._compile_final_result(task)
        
        return is_complete, message
    
    async def _correct_phase(self, task: RalphTask, validation_message: str):
        """CORRECT phase: Apply corrections"""
        failed_subtasks = [st for st in task.subtasks if st.status == TaskStatus.FAILED]
        
        if not failed_subtasks:
            return
        
        # Analyze and correct first failed subtask
        subtask = failed_subtasks[0]
        analysis = await self.correction_engine.analyze_failure(task, subtask)
        
        # Apply recommended strategy
        strategy = analysis["recommended_strategy"]
        applied = await self.correction_engine.apply_correction(task, subtask, strategy)
        
        iteration = TaskIteration(
            iteration_number=task.current_iteration,
            phase=LoopPhase.CORRECT,
            timestamp=datetime.now().isoformat(),
            action=f"Applied correction: {strategy}",
            result=analysis,
            correction_needed=True
        )
        task.iterations.append(iteration)
        
        self.progress_tracker.record_progress(task, LoopPhase.CORRECT, iteration.result)
        logger.info(f"Iteration {task.current_iteration}: CORRECT phase - Applied {strategy}")
    
    async def _complete_phase(self, task: RalphTask):
        """COMPLETE phase: Finalize task"""
        task.status = TaskStatus.COMPLETED
        task.progress_percentage = 100.0
        
        iteration = TaskIteration(
            iteration_number=task.current_iteration,
            phase=LoopPhase.COMPLETE,
            timestamp=datetime.now().isoformat(),
            action="Task completed",
            result={"goal": task.goal}
        )
        task.iterations.append(iteration)
        
        logger.info(f"Task {task.task_id} COMPLETED in {task.current_iteration} iterations")
    
    def _compile_final_result(self, task: RalphTask) -> Dict[str, Any]:
        """Compile final result from all subtasks"""
        return {
            "task_id": task.task_id,
            "goal": task.goal,
            "status": "completed",
            "iterations": task.current_iteration,
            "subtasks_completed": len([st for st in task.subtasks if st.status == TaskStatus.COMPLETED]),
            "total_subtasks": len(task.subtasks),
            "corrections_applied": len(task.corrections),
            "results": {st.task_id: st.result for st in task.subtasks if st.result}
        }
    
    async def _log_task_event(self, task: RalphTask, event_type: str, message: str):
        """Log task event"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": task.task_id,
            "event_type": event_type,
            "message": message
        }
        
        log_file = self.logs_dir / f"task_{task.task_id}.jsonl"
        async with aiofiles.open(log_file, 'a', encoding='utf-8') as f:
            await f.write(json.dumps(log_entry) + "\n")
    
    async def _save_task_result(self, task: RalphTask):
        """Save task result to file"""
        result_file = self.logs_dir / f"result_{task.task_id}.json"
        async with aiofiles.open(result_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(task.to_dict(), indent=2))
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status"""
        task = self.active_tasks.get(task_id) or self.completed_tasks.get(task_id)
        if task:
            return self.progress_tracker.get_progress_report(task)
        return None
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks"""
        all_tasks = []
        for task in list(self.active_tasks.values()) + list(self.completed_tasks.values()):
            all_tasks.append(self.progress_tracker.get_progress_report(task))
        return all_tasks


# ============== Global Instance ==============

ralph_orchestrator = RalphLoopOrchestrator()


# ============== Main Entry Points ==============

async def run_demo():
    """Run Ralph Loop demo"""
    print("=" * 60)
    print(" RALPH WIGGUM LOOP - AUTONOMOUS TASK COMPLETION")
    print("=" * 60)
    print()
    
    # Create demo task
    print("📝 Creating demo task...")
    task = await ralph_orchestrator.create_task(
        goal="Complete multi-step business analysis",
        description="Analyze business metrics, generate reports, and create recommendations",
        priority=TaskPriority.HIGH
    )
    
    print(f"   Task ID: {task.task_id}")
    print(f"   Goal: {task.goal}")
    print(f"   Subtasks: {len(task.subtasks)}")
    print()
    
    # Show subtasks
    print("📋 Subtasks:")
    for i, subtask in enumerate(task.subtasks, 1):
        print(f"   {i}. {subtask.description[:60]}...")
    print()
    
    # Execute loop
    print("🔄 Starting Ralph Loop execution...")
    print("-" * 60)
    
    completed_task = await ralph_orchestrator.execute_loop(task.task_id)
    
    print("-" * 60)
    print()
    
    # Show results
    print("📊 RESULTS:")
    print(f"   Status: {completed_task.status.value}")
    print(f"   Iterations: {completed_task.current_iteration}")
    print(f"   Progress: {completed_task.progress_percentage:.1f}%")
    print(f"   Subtasks Completed: {sum(1 for st in completed_task.subtasks if st.status == TaskStatus.COMPLETED)}/{len(completed_task.subtasks)}")
    print(f"   Corrections Applied: {len(completed_task.corrections)}")
    print()
    
    if completed_task.final_result:
        print("✅ FINAL RESULT:")
        print(f"   {json.dumps(completed_task.final_result, indent=2)[:500]}...")
    
    print()
    print("=" * 60)
    print(" DEMO COMPLETE!")
    print("=" * 60)
    
    return completed_task


async def execute_task(goal: str, description: str = "", priority: str = "medium"):
    """Execute a specific task through Ralph Loop"""
    priority_map = {
        "low": TaskPriority.LOW,
        "medium": TaskPriority.MEDIUM,
        "high": TaskPriority.HIGH,
        "critical": TaskPriority.CRITICAL
    }
    
    task = await ralph_orchestrator.create_task(
        goal=goal,
        description=description or goal,
        priority=priority_map.get(priority.lower(), TaskPriority.MEDIUM)
    )
    
    print(f"Created task: {task.task_id}")
    print(f"Goal: {task.goal}")
    print(f"Subtasks: {len(task.subtasks)}")
    print()
    print("Executing Ralph Loop...")
    
    completed_task = await ralph_orchestrator.execute_loop(task.task_id)
    
    print()
    print(f"Task {completed_task.status.value}")
    print(f"Iterations: {completed_task.current_iteration}")
    print(f"Progress: {completed_task.progress_percentage:.1f}%")
    
    return completed_task


async def show_status():
    """Show Ralph Loop status"""
    print("=" * 60)
    print(" RALPH WIGGUM LOOP - STATUS")
    print("=" * 60)
    
    all_tasks = ralph_orchestrator.get_all_tasks()
    
    if not all_tasks:
        print("\nNo tasks found. Create a task with: python ralph_loop.py --task \"Your goal\"")
    else:
        print(f"\nTotal Tasks: {len(all_tasks)}")
        print()
        
        for task in all_tasks:
            status_icon = "✅" if task["status"] == "completed" else "🔄" if task["status"] == "in_progress" else "⏳"
            print(f"{status_icon} Task: {task['task_id']}")
            print(f"   Goal: {task['goal']}")
            print(f"   Status: {task['status']}")
            print(f"   Progress: {task['progress_percentage']:.1f}%")
            print(f"   Iterations: {task['current_iteration']}/{task['max_iterations']}")
            print()
    
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ralph Wiggum Loop - Autonomous Task Completion")
    parser.add_argument("--task", type=str, help="Task goal to execute")
    parser.add_argument("--description", type=str, help="Task description")
    parser.add_argument("--priority", type=str, default="medium", choices=["low", "medium", "high", "critical"], help="Task priority")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--monitor", action="store_true", help="Monitor running loops")
    
    args = parser.parse_args()
    
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    if args.demo:
        asyncio.run(run_demo())
    elif args.task:
        asyncio.run(execute_task(args.task, args.description, args.priority))
    elif args.monitor:
        print("Monitoring mode - watching for new tasks...")
        print("Press Ctrl+C to stop")
        try:
            while True:
                asyncio.run(show_status())
                asyncio.sleep(5)
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
    else:
        asyncio.run(show_status())
