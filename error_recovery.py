"""
Error Recovery & Graceful Degradation System

Comprehensive error handling, recovery, and graceful degradation for all systems:
- Automatic retry with exponential backoff
- Circuit breaker pattern
- Graceful degradation when services fail
- Error logging and analysis
- Auto-recovery mechanisms
- Fallback strategies

Usage:
    python error_recovery.py              # Run recovery system
    python error_recovery.py --monitor    # Start monitoring
    python error_recovery.py --test       # Test error handling
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable, Awaitable
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field
import logging
import hashlib
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

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, stop calling
    HALF_OPEN = "half_open"  # Testing if service recovered


class RecoveryStrategy(Enum):
    """Available recovery strategies"""
    RETRY = "retry"
    FALLBACK = "fallback"
    BYPASS = "bypass"
    QUEUE = "queue"
    DEGRADED = "degraded"


@dataclass
class ErrorEvent:
    """Represents an error event"""
    timestamp: str
    service: str
    error_type: str
    error_message: str
    severity: ErrorSeverity
    stack_trace: Optional[str] = None
    recovery_attempted: bool = False
    recovery_successful: bool = False
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "service": self.service,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "severity": self.severity.value,
            "stack_trace": self.stack_trace,
            "recovery_attempted": self.recovery_attempted,
            "recovery_successful": self.recovery_successful,
            "retry_count": self.retry_count
        }


@dataclass
class CircuitBreaker:
    """Circuit breaker for a service"""
    service: str
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout_seconds: int = 60
    half_open_max_calls: int = 3
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "service": self.service,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "last_success_time": self.last_success_time.isoformat() if self.last_success_time else None,
            "failure_threshold": self.failure_threshold,
            "success_threshold": self.success_threshold,
            "timeout_seconds": self.timeout_seconds
        }


@dataclass
class ServiceHealth:
    """Health status of a service"""
    service: str
    is_healthy: bool = True
    last_check: Optional[datetime] = None
    response_time_ms: float = 0.0
    error_rate: float = 0.0
    consecutive_failures: int = 0
    degradation_level: int = 0  # 0 = full, 1 = degraded, 2 = minimal, 3 = offline
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "service": self.service,
            "is_healthy": self.is_healthy,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "response_time_ms": self.response_time_ms,
            "error_rate": self.error_rate,
            "consecutive_failures": self.consecutive_failures,
            "degradation_level": self.degradation_level
        }


# ============== Retry with Exponential Backoff ==============

class RetryWithBackoff:
    """
    Retry mechanism with exponential backoff and jitter.
    
    Usage:
        @RetryWithBackoff(max_retries=3, base_delay=1.0, max_delay=60.0)
        async def my_function():
            ...
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        exceptions: tuple = (Exception,)
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.exceptions = exceptions
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator to add retry logic to a function"""
        
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(self.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except self.exceptions as e:
                    last_exception = e
                    
                    if attempt == self.max_retries:
                        logger.error(f"{func.__name__} failed after {self.max_retries} retries")
                        raise
                    
                    # Calculate delay with exponential backoff
                    delay = min(
                        self.base_delay * (self.exponential_base ** attempt),
                        self.max_delay
                    )
                    
                    # Add jitter to prevent thundering herd
                    if self.jitter:
                        import random
                        delay *= (0.5 + random.random() * 0.5)
                    
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt + 1}/{self.max_retries + 1}). "
                        f"Retrying in {delay:.2f}s"
                    )
                    
                    await asyncio.sleep(delay)
            
            raise last_exception
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper


# ============== Circuit Breaker ==============

class CircuitBreakerManager:
    """
    Manages circuit breakers for all services.
    
    Circuit Breaker Pattern:
    - CLOSED: Normal operation, requests flow through
    - OPEN: Service failing, requests blocked
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(self):
        self.circuits: Dict[str, CircuitBreaker] = {}
        self.default_failure_threshold = 5
        self.default_success_threshold = 3
        self.default_timeout = 60
    
    def get_circuit(self, service: str) -> CircuitBreaker:
        """Get or create circuit breaker for a service"""
        if service not in self.circuits:
            self.circuits[service] = CircuitBreaker(
                service=service,
                failure_threshold=self.default_failure_threshold,
                success_threshold=self.default_success_threshold,
                timeout_seconds=self.default_timeout
            )
        return self.circuits[service]
    
    def can_execute(self, service: str) -> bool:
        """Check if request can be executed"""
        circuit = self.get_circuit(service)
        
        if circuit.state == CircuitState.CLOSED:
            return True
        
        if circuit.state == CircuitState.OPEN:
            # Check if timeout has passed
            if circuit.last_failure_time:
                elapsed = (datetime.now() - circuit.last_failure_time).total_seconds()
                if elapsed >= circuit.timeout_seconds:
                    circuit.state = CircuitState.HALF_OPEN
                    circuit.failure_count = 0
                    logger.info(f"Circuit for {service} moved to HALF_OPEN")
                    return True
            return False
        
        if circuit.state == CircuitState.HALF_OPEN:
            # Allow limited calls in half-open state
            return circuit.success_count < circuit.half_open_max_calls
        
        return False
    
    async def record_success(self, service: str):
        """Record successful execution"""
        circuit = self.get_circuit(service)
        circuit.success_count += 1
        circuit.last_success_time = datetime.now()
        
        if circuit.state == CircuitState.HALF_OPEN:
            if circuit.success_count >= circuit.success_threshold:
                circuit.state = CircuitState.CLOSED
                circuit.failure_count = 0
                circuit.success_count = 0
                logger.info(f"Circuit for {service} moved to CLOSED")
        
        elif circuit.state == CircuitState.CLOSED:
            # Reset failure count on success
            circuit.failure_count = 0
    
    async def record_failure(self, service: str):
        """Record failed execution"""
        circuit = self.get_circuit(service)
        circuit.failure_count += 1
        circuit.last_failure_time = datetime.now()
        circuit.success_count = 0
        
        if circuit.state == CircuitState.HALF_OPEN:
            circuit.state = CircuitState.OPEN
            logger.warning(f"Circuit for {service} moved to OPEN (failed in half-open)")
        
        elif circuit.state == CircuitState.CLOSED:
            if circuit.failure_count >= circuit.failure_threshold:
                circuit.state = CircuitState.OPEN
                logger.warning(f"Circuit for {service} moved to OPEN (threshold reached)")
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all circuit breakers"""
        return {
            service: circuit.to_dict()
            for service, circuit in self.circuits.items()
        }


# ============== Graceful Degradation ==============

class GracefulDegradation:
    """
    Implements graceful degradation strategies when services fail.
    
    Degradation Levels:
    0 - Full functionality
    1 - Degraded (some features disabled)
    2 - Minimal (core features only)
    3 - Offline (service unavailable)
    """
    
    def __init__(self):
        self.service_degradation: Dict[str, int] = {}
        self.fallback_strategies: Dict[str, Callable] = {}
        self.feature_flags: Dict[str, bool] = {}
    
    def set_degradation_level(self, service: str, level: int):
        """Set degradation level for a service"""
        if level < 0 or level > 3:
            raise ValueError("Degradation level must be 0-3")
        
        self.service_degradation[service] = level
        
        # Update feature flags based on degradation
        self._update_feature_flags(service, level)
        
        logger.info(f"Service {service} degradation level set to {level}")
    
    def _update_feature_flags(self, service: str, level: int):
        """Update feature flags based on degradation level"""
        if service == "Accounting":
            self.feature_flags["accounting_full_reports"] = level == 0
            self.feature_flags["accounting_basic"] = level <= 1
            self.feature_flags["accounting_read_only"] = level <= 2
        
        elif service == "Social Media":
            self.feature_flags["social_auto_post"] = level == 0
            self.feature_flags["social_manual_post"] = level <= 1
            self.feature_flags["social_read_only"] = level <= 2
        
        elif service == "Business":
            self.feature_flags["business_full"] = level == 0
            self.feature_flags["business_basic"] = level <= 1
            self.feature_flags["business_read_only"] = level <= 2
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        return self.feature_flags.get(feature, True)
    
    def register_fallback(self, service: str, fallback: Callable):
        """Register fallback function for a service"""
        self.fallback_strategies[service] = fallback
    
    async def execute_with_fallback(
        self,
        service: str,
        primary: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Execute primary function, fallback on failure"""
        degradation_level = self.service_degradation.get(service, 0)
        
        # If service is offline, use fallback immediately
        if degradation_level >= 3:
            logger.info(f"Service {service} is offline, using fallback")
            return await self._execute_fallback(service, *args, **kwargs)
        
        try:
            # Try primary function
            return await primary(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Primary execution failed for {service}, using fallback: {e}")
            return await self._execute_fallback(service, *args, **kwargs)
    
    async def _execute_fallback(self, service: str, *args, **kwargs) -> Any:
        """Execute fallback function"""
        if service in self.fallback_strategies:
            return await self.fallback_strategies[service](*args, **kwargs)
        
        # Default fallback - return empty/safe response
        logger.warning(f"No fallback registered for {service}, returning default")
        return self._get_default_response(service)
    
    def _get_default_response(self, service: str) -> Any:
        """Get default response for a service"""
        defaults = {
            "Accounting": {"revenue": 0, "expenses": 0, "profit": 0},
            "Social Media": {"posts": 0, "engagement": 0},
            "Business": {"meetings": 0, "deals": 0, "pipeline_value": 0},
            "Personal": {"appointments": [], "tasks": []}
        }
        return defaults.get(service, {})


# ============== Error Recovery Manager ==============

class ErrorRecoveryManager:
    """
    Central manager for error recovery and graceful degradation.
    """
    
    def __init__(self):
        self.circuit_breaker = CircuitBreakerManager()
        self.degradation = GracefulDegradation()
        self.error_log: List[ErrorEvent] = []
        self.max_error_log_size = 1000
        self.recovery_strategies: Dict[str, RecoveryStrategy] = {}
        self.service_health: Dict[str, ServiceHealth] = {}
        
        # Ensure logs directory exists
        self.logs_dir = Path("logs/error_recovery")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Load error log
        self._load_error_log()
    
    def _load_error_log(self):
        """Load error log from file"""
        log_file = self.logs_dir / "error_log.json"
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    errors = json.load(f)
                    self.error_log = [ErrorEvent(**e) for e in errors[-100:]]
            except Exception as e:
                logger.error(f"Failed to load error log: {e}")
    
    def _save_error_log(self):
        """Save error log to file"""
        log_file = self.logs_dir / "error_log.json"
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump([e.to_dict() for e in self.error_log[-self.max_error_log_size:]], f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save error log: {e}")
    
    async def execute_with_recovery(
        self,
        service: str,
        operation: Callable,
        *args,
        fallback: Optional[Callable] = None,
        **kwargs
    ) -> Any:
        """
        Execute operation with full error recovery support.
        
        Args:
            service: Service name
            operation: Async function to execute
            fallback: Optional fallback function
            *args, **kwargs: Arguments for operation
        
        Returns:
            Operation result or fallback result
        """
        # Check circuit breaker
        if not self.circuit_breaker.can_execute(service):
            logger.warning(f"Circuit breaker OPEN for {service}, using fallback")
            if fallback:
                return await fallback(*args, **kwargs)
            return self.degradation._get_default_response(service)
        
        try:
            # Execute operation
            start_time = time.time()
            result = await operation(*args, **kwargs)
            elapsed_ms = (time.time() - start_time) * 1000
            
            # Record success
            await self.circuit_breaker.record_success(service)
            self._update_service_health(service, True, elapsed_ms)
            
            return result
        
        except Exception as e:
            # Record failure
            await self.circuit_breaker.record_failure(service)
            self._update_service_health(service, False, 0)
            
            # Log error
            error_event = self._create_error_event(service, e)
            self.error_log.append(error_event)
            self._save_error_log()
            
            # Attempt recovery
            recovery_result = await self._attempt_recovery(service, e, operation, *args, **kwargs)
            if recovery_result is not None:
                return recovery_result
            
            # Use fallback if available
            if fallback:
                logger.info(f"Using fallback for {service}")
                try:
                    return await fallback(*args, **kwargs)
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed for {service}: {fallback_error}")
            
            # Return default response
            logger.error(f"All recovery attempts failed for {service}")
            return self.degradation._get_default_response(service)
    
    def _create_error_event(self, service: str, error: Exception) -> ErrorEvent:
        """Create error event from exception"""
        import traceback
        
        # Determine severity based on error type
        severity = ErrorSeverity.MEDIUM
        if isinstance(error, (httpx.ConnectError, httpx.TimeoutException)):
            severity = ErrorSeverity.HIGH
        elif isinstance(error, (httpx.HTTPStatusError, httpx.HTTPError)):
            severity = ErrorSeverity.MEDIUM
        elif isinstance(error, (KeyError, ValueError, TypeError)):
            severity = ErrorSeverity.LOW
        
        return ErrorEvent(
            timestamp=datetime.now().isoformat(),
            service=service,
            error_type=type(error).__name__,
            error_message=str(error),
            severity=severity,
            stack_trace=traceback.format_exc(),
            recovery_attempted=False
        )
    
    async def _attempt_recovery(
        self,
        service: str,
        error: Exception,
        operation: Callable,
        *args,
        **kwargs
    ) -> Optional[Any]:
        """Attempt to recover from error"""
        strategy = self.recovery_strategies.get(service, RecoveryStrategy.RETRY)
        
        if strategy == RecoveryStrategy.RETRY:
            # Retry with exponential backoff
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    await asyncio.sleep(2 ** retry_count)
                    return await operation(*args, **kwargs)
                except Exception:
                    retry_count += 1
            
            return None
        
        elif strategy == RecoveryStrategy.BYPASS:
            # Return cached/default response
            return self.degradation._get_default_response(service)
        
        return None
    
    def _update_service_health(self, service: str, success: bool, response_time_ms: float):
        """Update service health metrics"""
        if service not in self.service_health:
            self.service_health[service] = ServiceHealth(service=service)
        
        health = self.service_health[service]
        health.last_check = datetime.now()
        
        if success:
            health.consecutive_failures = 0
            health.response_time_ms = response_time_ms
            health.is_healthy = True
        else:
            health.consecutive_failures += 1
            if health.consecutive_failures >= 5:
                health.is_healthy = False
                # Set degradation level based on failures
                degradation_level = min(health.consecutive_failures // 5, 3)
                self.degradation.set_degradation_level(service, degradation_level)
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors"""
        if not self.error_log:
            return {"total_errors": 0, "errors": []}
        
        # Count by severity
        by_severity = {}
        for error in self.error_log:
            severity = error.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        # Count by service
        by_service = {}
        for error in self.error_log:
            service = error.service
            by_service[service] = by_service.get(service, 0) + 1
        
        # Recent errors (last 10)
        recent = [e.to_dict() for e in self.error_log[-10:]]
        
        return {
            "total_errors": len(self.error_log),
            "by_severity": by_severity,
            "by_service": by_service,
            "recent_errors": recent,
            "time_range": {
                "oldest": self.error_log[0].timestamp if self.error_log else None,
                "newest": self.error_log[-1].timestamp if self.error_log else None
            }
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health"""
        return {
            "timestamp": datetime.now().isoformat(),
            "circuit_breakers": self.circuit_breaker.get_status(),
            "service_health": {
                service: health.to_dict()
                for service, health in self.service_health.items()
            },
            "degradation_levels": self.degradation.service_degradation,
            "feature_flags": self.degradation.feature_flags,
            "error_summary": self.get_error_summary()
        }


# ============== Health Monitor ==============

class HealthMonitor:
    """
    Monitors health of all services and triggers recovery when needed.
    """
    
    def __init__(self, recovery_manager: ErrorRecoveryManager):
        self.recovery_manager = recovery_manager
        self.mcp_servers = {
            "Accounting": "http://localhost:8001",
            "Social Media": "http://localhost:8002",
            "Personal": "http://localhost:8003",
            "Business": "http://localhost:8004"
        }
        self.check_interval = 30  # seconds
        self.running = False
    
    async def start_monitoring(self):
        """Start continuous health monitoring"""
        self.running = True
        logger.info("Starting health monitoring...")
        
        while self.running:
            try:
                await self._check_all_services()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                logger.info("Health monitoring stopped")
                break
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(self.check_interval)
    
    async def stop_monitoring(self):
        """Stop health monitoring"""
        self.running = False
        logger.info("Stopping health monitoring...")
    
    async def _check_all_services(self):
        """Check health of all MCP servers"""
        for service, url in self.mcp_servers.items():
            await self._check_service_health(service, url)
    
    async def _check_service_health(self, service: str, url: str):
        """Check health of a single service"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
                start_time = time.time()
                response = await client.get(f"{url}/health")
                elapsed_ms = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "healthy":
                        await self.recovery_manager.circuit_breaker.record_success(service)
                        self.recovery_manager._update_service_health(service, True, elapsed_ms)
                        logger.debug(f"✅ {service} is healthy ({elapsed_ms:.0f}ms)")
                    else:
                        await self._handle_unhealthy_service(service)
                else:
                    await self._handle_unhealthy_service(service)
        
        except Exception as e:
            await self.recovery_manager.circuit_breaker.record_failure(service)
            self.recovery_manager._update_service_health(service, False, 0)
            logger.warning(f"❌ {service} health check failed: {e}")
    
    async def _handle_unhealthy_service(self, service: str):
        """Handle unhealthy service"""
        logger.warning(f"Service {service} is unhealthy")
        
        # Increase degradation level
        current_level = self.recovery_manager.degradation.service_degradation.get(service, 0)
        new_level = min(current_level + 1, 3)
        self.recovery_manager.degradation.set_degradation_level(service, new_level)
        
        # Log error
        error_event = ErrorEvent(
            timestamp=datetime.now().isoformat(),
            service=service,
            error_type="HealthCheckFailed",
            error_message=f"Service {service} failed health check",
            severity=ErrorSeverity.HIGH if new_level >= 2 else ErrorSeverity.MEDIUM
        )
        self.recovery_manager.error_log.append(error_event)


# ============== Main Entry Points ==============

async def test_error_handling():
    """Test error handling and recovery"""
    print("=" * 60)
    print(" ERROR RECOVERY & GRACEFUL DEGRADATION - TEST")
    print("=" * 60)
    
    recovery_manager = ErrorRecoveryManager()
    
    # Test 1: Circuit Breaker
    print("\n[TEST 1] Circuit Breaker Pattern")
    print("-" * 60)
    
    async def failing_operation():
        raise Exception("Simulated failure")
    
    for i in range(7):
        result = await recovery_manager.execute_with_recovery(
            "TestService",
            failing_operation
        )
        circuit = recovery_manager.circuit_breaker.get_circuit("TestService")
        print(f"  Attempt {i+1}: State={circuit.state.value}, Failures={circuit.failure_count}")
    
    # Test 2: Graceful Degradation
    print("\n[TEST 2] Graceful Degradation")
    print("-" * 60)
    
    recovery_manager.degradation.set_degradation_level("Accounting", 1)
    print(f"  Accounting degradation level: {recovery_manager.degradation.service_degradation.get('Accounting')}")
    print(f"  accounting_full_reports enabled: {recovery_manager.degradation.is_feature_enabled('accounting_full_reports')}")
    print(f"  accounting_read_only enabled: {recovery_manager.degradation.is_feature_enabled('accounting_read_only')}")
    
    # Test 3: Retry with Backoff
    print("\n[TEST 3] Retry with Exponential Backoff")
    print("-" * 60)
    
    attempt_count = 0
    
    @RetryWithBackoff(max_retries=3, base_delay=0.1, max_delay=1.0)
    async def eventually_succeeds():
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise Exception("Not yet")
        return "Success!"
    
    try:
        result = await eventually_succeeds()
        print(f"  Result: {result} (after {attempt_count} attempts)")
    except Exception as e:
        print(f"  Failed: {e}")
    
    # Test 4: System Health
    print("\n[TEST 4] System Health Status")
    print("-" * 60)
    
    health = recovery_manager.get_system_health()
    print(f"  Circuit Breakers: {len(health['circuit_breakers'])}")
    print(f"  Total Errors: {health['error_summary']['total_errors']}")
    
    print("\n" + "=" * 60)
    print(" TEST COMPLETE")
    print("=" * 60)
    
    return True


async def start_monitoring():
    """Start health monitoring"""
    recovery_manager = ErrorRecoveryManager()
    monitor = HealthMonitor(recovery_manager)
    
    print("=" * 60)
    print(" HEALTH MONITORING STARTED")
    print("=" * 60)
    print(f"Checking {len(monitor.mcp_servers)} services every {monitor.check_interval} seconds")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        await monitor.start_monitoring()
    except KeyboardInterrupt:
        await monitor.stop_monitoring()


async def show_status():
    """Show current error recovery status"""
    recovery_manager = ErrorRecoveryManager()
    
    print("=" * 60)
    print(" ERROR RECOVERY & GRACEFUL DEGRADATION STATUS")
    print("=" * 60)
    
    health = recovery_manager.get_system_health()
    
    print(f"\nTimestamp: {health['timestamp']}")
    
    # Circuit Breakers
    print("\n📊 Circuit Breakers:")
    for service, circuit in health['circuit_breakers'].items():
        state = circuit['state']
        icon = "✅" if state == "closed" else "⚠️" if state == "half_open" else "❌"
        print(f"  {icon} {service}: {state}")
    
    # Service Health
    print("\n🏥 Service Health:")
    for service, health_info in health['service_health'].items():
        status = "✅ Healthy" if health_info['is_healthy'] else "❌ Unhealthy"
        print(f"  {status} - {service}")
    
    # Degradation Levels
    print("\n📉 Degradation Levels:")
    if not health['degradation_levels']:
        print("  All services at full functionality")
    else:
        for service, level in health['degradation_levels'].items():
            level_text = ["Full", "Degraded", "Minimal", "Offline"][level]
            print(f"  {service}: {level_text} (Level {level})")
    
    # Error Summary
    print("\n📋 Error Summary:")
    error_summary = health['error_summary']
    print(f"  Total Errors: {error_summary['total_errors']}")
    if error_summary['by_severity']:
        print(f"  By Severity: {error_summary['by_severity']}")
    if error_summary['by_service']:
        print(f"  By Service: {error_summary['by_service']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Error Recovery & Graceful Degradation System")
    parser.add_argument("--test", action="store_true", help="Test error handling")
    parser.add_argument("--monitor", action="store_true", help="Start health monitoring")
    parser.add_argument("--status", action="store_true", help="Show current status")
    
    args = parser.parse_args()
    
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    if args.test:
        asyncio.run(test_error_handling())
    elif args.monitor:
        asyncio.run(start_monitoring())
    elif args.status:
        asyncio.run(show_status())
    else:
        # Default: show status
        asyncio.run(show_status())
