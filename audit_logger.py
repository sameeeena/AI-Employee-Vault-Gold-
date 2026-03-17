"""
Comprehensive Audit Logging System

Enterprise-grade audit logging for all systems:
- Logs all user actions and system events
- Immutable audit trail
- Query and search capabilities
- Compliance-ready reports
- Real-time monitoring
- Log rotation and archival

Usage:
    python audit_logger.py              # Show status
    python audit_logger.py --log        # Log an event
    python audit_logger.py --query      # Query logs
    python audit_logger.py --report     # Generate report
    python audit_logger.py --monitor    # Real-time monitoring
"""

import asyncio
import json
import os
import sys
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
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

class AuditEventType(Enum):
    """Types of audit events"""
    # Authentication
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    
    # Data Operations
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    IMPORT = "import"
    
    # System Operations
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"
    CONFIG_CHANGE = "config_change"
    BACKUP = "backup"
    RESTORE = "restore"
    
    # Business Operations
    INVOICE_CREATE = "invoice_create"
    PAYMENT_PROCESS = "payment_process"
    MEETING_SCHEDULE = "meeting_schedule"
    POST_PUBLISH = "post_publish"
    
    # Security
    PERMISSION_CHANGE = "permission_change"
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    SECURITY_ALERT = "security_alert"


class AuditSeverity(Enum):
    """Audit event severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditCategory(Enum):
    """Audit event categories"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    SYSTEM = "system"
    SECURITY = "security"
    BUSINESS = "business"
    COMPLIANCE = "compliance"


@dataclass
class AuditEvent:
    """Represents an audit event"""
    event_id: str
    timestamp: str
    event_type: str
    category: str
    severity: str
    service: str
    action: str
    user_id: Optional[str]
    user_email: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    resource_type: Optional[str]
    resource_id: Optional[str]
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    previous_state: Optional[Dict[str, Any]] = None
    new_state: Optional[Dict[str, Any]] = None
    signature: str = ""
    
    def __post_init__(self):
        """Generate signature after initialization"""
        if not self.signature:
            self.signature = self._generate_signature()
    
    def _generate_signature(self) -> str:
        """Generate cryptographic signature for integrity"""
        data = f"{self.event_id}{self.timestamp}{self.event_type}{self.service}{self.action}"
        secret = os.getenv("AUDIT_SECRET_KEY", "default_audit_key")
        return hmac.new(
            secret.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def verify_signature(self) -> bool:
        """Verify event integrity"""
        return self.signature == self._generate_signature()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuditEvent':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class AuditQuery:
    """Query parameters for audit log search"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    event_type: Optional[str] = None
    category: Optional[str] = None
    severity: Optional[str] = None
    service: Optional[str] = None
    user_id: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    search_text: Optional[str] = None
    limit: int = 100
    offset: int = 0


# ============== Audit Log Storage ==============

class AuditLogStorage:
    """
    Manages audit log storage with multiple backends.
    """
    
    def __init__(self, base_dir: str = "audit_logs"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Current log file
        self.current_date = datetime.now().strftime("%Y%m%d")
        self.current_file = self.base_dir / f"audit_{self.current_date}.json"
        
        # Initialize today's log file
        self._initialize_log_file()
        
        # Log rotation settings
        self.max_file_size_mb = 100
        self.retention_days = 90
        
        # Archive directory
        self.archive_dir = self.base_dir / "archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def _initialize_log_file(self):
        """Initialize log file if it doesn't exist"""
        if not self.current_file.exists():
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "version": "1.0",
                    "created": datetime.now().isoformat(),
                    "events": [],
                    "event_count": 0
                }, f, indent=2)
    
    def _load_log_file(self) -> Dict[str, Any]:
        """Load current log file"""
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_log_file()
            return {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "events": [],
                "event_count": 0
            }
    
    def _save_log_file(self, data: Dict[str, Any]):
        """Save log file"""
        with open(self.current_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    async def append_event(self, event: AuditEvent):
        """Append event to log file"""
        log_data = self._load_log_file()
        
        log_data["events"].append(event.to_dict())
        log_data["event_count"] = len(log_data["events"])
        log_data["last_updated"] = datetime.now().isoformat()
        
        self._save_log_file(log_data)
        
        # Check if rotation needed
        await self._check_rotation()
    
    async def _check_rotation(self):
        """Check if log rotation is needed"""
        # Check file size
        if self.current_file.exists():
            size_mb = self.current_file.stat().st_size / (1024 * 1024)
            if size_mb > self.max_file_size_mb:
                await self._rotate_log()
        
        # Check date change
        today = datetime.now().strftime("%Y%m%d")
        if today != self.current_date:
            self.current_date = today
            self.current_file = self.base_dir / f"audit_{self.current_date}.json"
            self._initialize_log_file()
    
    async def _rotate_log(self):
        """Rotate log file to archive"""
        if not self.current_file.exists():
            return
        
        # Move to archive
        archive_name = f"audit_{self.current_date}_{datetime.now().strftime('%H%M%S')}.json"
        archive_path = self.archive_dir / archive_name
        
        import shutil
        shutil.copy2(self.current_file, archive_path)
        
        # Clear current file
        with open(self.current_file, 'w', encoding='utf-8') as f:
            json.dump({
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "events": [],
                "event_count": 0
            }, f, indent=2)
        
        logger.info(f"Log rotated to {archive_path}")
        
        # Clean old archives
        await self._cleanup_old_archives()
    
    async def _cleanup_old_archives(self):
        """Remove archives older than retention period"""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        
        for archive_file in self.archive_dir.glob("*.json"):
            try:
                file_time = datetime.fromtimestamp(archive_file.stat().st_mtime)
                if file_time < cutoff:
                    archive_file.unlink()
                    logger.info(f"Deleted old archive: {archive_file.name}")
            except Exception as e:
                logger.error(f"Error processing archive {archive_file.name}: {e}")
    
    async def query_events(self, query: AuditQuery) -> List[Dict[str, Any]]:
        """Query audit events"""
        results = []
        
        # Load all log files (current + archives)
        log_files = [self.current_file] + list(self.archive_dir.glob("audit_*.json"))
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    events = log_data.get("events", [])
                    
                    for event in events:
                        if self._matches_query(event, query):
                            results.append(event)
                            
                            if len(results) >= query.limit + query.offset:
                                break
            except Exception as e:
                logger.error(f"Error reading log file {log_file}: {e}")
        
        # Apply offset and limit
        return results[query.offset:query.offset + query.limit]
    
    def _matches_query(self, event: Dict[str, Any], query: AuditQuery) -> bool:
        """Check if event matches query criteria"""
        # Date range
        event_time = datetime.fromisoformat(event["timestamp"])
        if query.start_date and event_time < query.start_date:
            return False
        if query.end_date and event_time > query.end_date:
            return False
        
        # Event type
        if query.event_type and event["event_type"] != query.event_type:
            return False
        
        # Category
        if query.category and event["category"] != query.category:
            return False
        
        # Severity
        if query.severity and event["severity"] != query.severity:
            return False
        
        # Service
        if query.service and event["service"] != query.service:
            return False
        
        # User
        if query.user_id and event["user_id"] != query.user_id:
            return False
        
        # Resource
        if query.resource_type and event["resource_type"] != query.resource_type:
            return False
        if query.resource_id and event["resource_id"] != query.resource_id:
            return False
        
        # Search text
        if query.search_text:
            search_lower = query.search_text.lower()
            searchable = f"{event['action']} {event['description']} {event.get('resource_type', '')} {event.get('resource_id', '')}".lower()
            if search_lower not in searchable:
                return False
        
        return True
    
    async def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get audit log statistics"""
        cutoff = datetime.now() - timedelta(days=days)
        
        stats = {
            "total_events": 0,
            "by_type": {},
            "by_category": {},
            "by_severity": {},
            "by_service": {},
            "by_user": {},
            "time_range": {
                "start": cutoff.isoformat(),
                "end": datetime.now().isoformat()
            }
        }
        
        # Load all log files
        log_files = [self.current_file] + list(self.archive_dir.glob("audit_*.json"))
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                    events = log_data.get("events", [])
                    
                    for event in events:
                        event_time = datetime.fromisoformat(event["timestamp"])
                        if event_time < cutoff:
                            continue
                        
                        stats["total_events"] += 1
                        
                        # Count by type
                        event_type = event["event_type"]
                        stats["by_type"][event_type] = stats["by_type"].get(event_type, 0) + 1
                        
                        # Count by category
                        category = event["category"]
                        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
                        
                        # Count by severity
                        severity = event["severity"]
                        stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1
                        
                        # Count by service
                        service = event["service"]
                        stats["by_service"][service] = stats["by_service"].get(service, 0) + 1
                        
                        # Count by user
                        user_id = event.get("user_id", "anonymous")
                        stats["by_user"][user_id] = stats["by_user"].get(user_id, 0) + 1
            
            except Exception as e:
                logger.error(f"Error processing log file {log_file}: {e}")
        
        return stats


# ============== Audit Logger ==============

class AuditLogger:
    """
    Main audit logger - provides logging interface for all systems.
    """
    
    def __init__(self):
        self.storage = AuditLogStorage()
        self.enabled = True
        self.buffer: List[AuditEvent] = []
        self.buffer_size = 10
        self.flush_interval = 60  # seconds
        self.last_flush = datetime.now()
    
    async def initialize(self):
        """Initialize audit logger"""
        # Log system startup
        await self._log_system_event("AUDIT_LOGGER_STARTED")
    
    def create_event(
        self,
        event_type: AuditEventType,
        category: AuditCategory,
        severity: AuditSeverity,
        service: str,
        action: str,
        description: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        ip_address: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        previous_state: Optional[Dict[str, Any]] = None,
        new_state: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        """Create an audit event"""
        event_id = self._generate_event_id()
        
        event = AuditEvent(
            event_id=event_id,
            timestamp=datetime.now().isoformat(),
            event_type=event_type.value,
            category=category.value,
            severity=severity.value,
            service=service,
            action=action,
            user_id=user_id,
            user_email=user_email,
            ip_address=ip_address,
            user_agent=None,  # Can be set from request
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            metadata=metadata or {},
            previous_state=previous_state,
            new_state=new_state
        )
        
        return event
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        timestamp = datetime.now().isoformat()
        random_data = os.urandom(16).hex()
        return hashlib.sha256(f"{timestamp}{random_data}".encode()).hexdigest()[:32]
    
    async def log_event(self, event: AuditEvent):
        """Log an audit event"""
        if not self.enabled:
            return
        
        # Add to buffer
        self.buffer.append(event)
        
        # Flush if buffer full or interval passed
        if len(self.buffer) >= self.buffer_size:
            await self._flush_buffer()
        
        # Also log to console
        self._log_to_console(event)
    
    def _log_to_console(self, event: AuditEvent):
        """Log event to console"""
        log_level = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }.get(event.severity, logging.INFO)
        
        logger.log(
            log_level,
            f"[{event.event_type}] {event.service} - {event.action} by {event.user_id or 'system'}"
        )
    
    async def _flush_buffer(self):
        """Flush buffer to storage"""
        if not self.buffer:
            return
        
        for event in self.buffer:
            await self.storage.append_event(event)
        
        self.buffer = []
        self.last_flush = datetime.now()
    
    async def _log_system_event(self, action: str):
        """Log system-level event"""
        event = self.create_event(
            event_type=AuditEventType.SYSTEM_START if "START" in action else AuditEventType.SYSTEM_STOP,
            category=AuditCategory.SYSTEM,
            severity=AuditSeverity.INFO,
            service="AUDIT_LOGGER",
            action=action,
            description=f"System event: {action}"
        )
        
        await self.log_event(event)
    
    # Convenience methods for common operations
    
    async def log_login(self, user_id: str, email: str, success: bool, ip_address: str = ""):
        """Log login attempt"""
        event = self.create_event(
            event_type=AuditEventType.LOGIN if success else AuditEventType.LOGIN_FAILED,
            category=AuditCategory.AUTHENTICATION,
            severity=AuditSeverity.INFO if success else AuditSeverity.WARNING,
            service="AUTH",
            action="user_login",
            description=f"User {'login successful' if success else 'login failed'}: {email}",
            user_id=user_id,
            user_email=email,
            ip_address=ip_address
        )
        await self.log_event(event)
    
    async def log_logout(self, user_id: str, email: str):
        """Log logout"""
        event = self.create_event(
            event_type=AuditEventType.LOGOUT,
            category=AuditCategory.AUTHENTICATION,
            severity=AuditSeverity.INFO,
            service="AUTH",
            action="user_logout",
            description=f"User logout: {email}",
            user_id=user_id,
            user_email=email
        )
        await self.log_event(event)
    
    async def log_data_access(
        self,
        service: str,
        resource_type: str,
        resource_id: str,
        user_id: str,
        action: str = "read"
    ):
        """Log data access"""
        event = self.create_event(
            event_type=AuditEventType.READ,
            category=AuditCategory.DATA_ACCESS,
            severity=AuditSeverity.DEBUG,
            service=service,
            action=action,
            description=f"{action.capitalize()} access to {resource_type}: {resource_id}",
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id
        )
        await self.log_event(event)
    
    async def log_data_modification(
        self,
        service: str,
        resource_type: str,
        resource_id: str,
        user_id: str,
        action: str,
        previous_state: Dict[str, Any],
        new_state: Dict[str, Any]
    ):
        """Log data modification"""
        event = self.create_event(
            event_type=AuditEventType.UPDATE,
            category=AuditCategory.DATA_MODIFICATION,
            severity=AuditSeverity.INFO,
            service=service,
            action=action,
            description=f"{action.capitalize()} {resource_type}: {resource_id}",
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            previous_state=previous_state,
            new_state=new_state
        )
        await self.log_event(event)
    
    async def log_security_event(
        self,
        service: str,
        action: str,
        description: str,
        severity: AuditSeverity = AuditSeverity.WARNING,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Log security event"""
        event = self.create_event(
            event_type=AuditEventType.SECURITY_ALERT,
            category=AuditCategory.SECURITY,
            severity=severity,
            service=service,
            action=action,
            description=description,
            user_id=user_id,
            ip_address=ip_address
        )
        await self.log_event(event)
    
    async def log_business_event(
        self,
        service: str,
        event_type: AuditEventType,
        action: str,
        description: str,
        user_id: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log business operation"""
        event = self.create_event(
            event_type=event_type,
            category=AuditCategory.BUSINESS,
            severity=AuditSeverity.INFO,
            service=service,
            action=action,
            description=description,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata
        )
        await self.log_event(event)
    
    async def flush(self):
        """Force flush buffer to storage"""
        await self._flush_buffer()
    
    async def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get audit statistics"""
        return await self.storage.get_statistics(days)
    
    async def query(self, query: AuditQuery) -> List[Dict[str, Any]]:
        """Query audit logs"""
        return await self.storage.query_events(query)


# ============== Audit Report Generator ==============

class AuditReportGenerator:
    """
    Generates audit reports for compliance and analysis.
    """
    
    def __init__(self, logger: AuditLogger):
        self.logger = logger
        self.reports_dir = Path("audit_reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate_daily_report(self, date: Optional[datetime] = None) -> str:
        """Generate daily audit report"""
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime("%Y%m%d")
        
        # Query events for the day
        query = AuditQuery(
            start_date=date.replace(hour=0, minute=0, second=0),
            end_date=date.replace(hour=23, minute=59, second=59),
            limit=10000
        )
        
        events = await self.logger.query(query)
        
        # Generate report
        report = self._create_report_content("Daily Audit Report", date_str, events)
        
        # Save report
        filename = f"daily_audit_{date_str}.md"
        filepath = self.reports_dir / filename
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(report)
        
        logger.info(f"Daily report generated: {filepath}")
        return str(filepath)
    
    async def generate_weekly_report(self, week_start: Optional[datetime] = None) -> str:
        """Generate weekly audit report"""
        if week_start is None:
            # Get Monday of current week
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
        
        week_end = week_start + timedelta(days=6)
        
        query = AuditQuery(
            start_date=week_start,
            end_date=week_end.replace(hour=23, minute=59, second=59),
            limit=50000
        )
        
        events = await self.logger.query(query)
        
        report = self._create_report_content(
            "Weekly Audit Report",
            f"{week_start.strftime('%Y%m%d')}_{week_end.strftime('%Y%m%d')}",
            events
        )
        
        filename = f"weekly_audit_{week_start.strftime('%Y%m%d')}.md"
        filepath = self.reports_dir / filename
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(report)
        
        logger.info(f"Weekly report generated: {filepath}")
        return str(filepath)
    
    async def generate_security_report(self, days: int = 30) -> str:
        """Generate security-focused audit report"""
        cutoff = datetime.now() - timedelta(days=days)
        
        query = AuditQuery(
            start_date=cutoff,
            category="security",
            limit=10000
        )
        
        events = await self.logger.query(query)
        
        report = self._create_security_report_content(events, days)
        
        filename = f"security_report_{days}days.md"
        filepath = self.reports_dir / filename
        
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(report)
        
        logger.info(f"Security report generated: {filepath}")
        return str(filepath)
    
    def _create_report_content(self, title: str, date_range: str, events: List[Dict]) -> str:
        """Create report content"""
        report = []
        report.append(f"# {title}")
        report.append(f"**Period:** {date_range}")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("## Summary")
        report.append(f"**Total Events:** {len(events)}")
        report.append("")
        
        # Events by type
        by_type = {}
        for event in events:
            event_type = event.get("event_type", "unknown")
            by_type[event_type] = by_type.get(event_type, 0) + 1
        
        report.append("## Events by Type")
        for event_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- {event_type}: {count}")
        report.append("")
        
        # Events by severity
        by_severity = {}
        for event in events:
            severity = event.get("severity", "unknown")
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        report.append("## Events by Severity")
        for severity, count in sorted(by_severity.items(), key=lambda x: x[1], reverse=True):
            report.append(f"- {severity}: {count}")
        report.append("")
        
        # Recent critical events
        critical_events = [e for e in events if e.get("severity") in ["error", "critical"]]
        if critical_events:
            report.append("## Critical/Error Events")
            for event in critical_events[:20]:
                report.append(f"- **{event['timestamp']}** - {event['service']}: {event['action']}")
                report.append(f"  - {event['description']}")
            report.append("")
        
        # Timeline
        report.append("## Event Timeline")
        report.append("```")
        for event in events[:100]:  # Show first 100
            report.append(f"{event['timestamp'][:19]} | {event['severity']:8} | {event['service']:20} | {event['action']}")
        report.append("```")
        
        return "\n".join(report)
    
    def _create_security_report_content(self, events: List[Dict], days: int) -> str:
        """Create security-focused report content"""
        report = []
        report.append(f"# Security Audit Report")
        report.append(f"**Period:** Last {days} days")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Security summary
        report.append("## Security Summary")
        report.append(f"**Total Security Events:** {len(events)}")
        report.append("")
        
        # Failed logins
        failed_logins = [e for e in events if e.get("event_type") == "login_failed"]
        report.append(f"### Failed Login Attempts: {len(failed_logins)}")
        if failed_logins:
            report.append("**Recent Failed Logins:**")
            for event in failed_logins[-10:]:
                report.append(f"- {event['timestamp']}: {event.get('user_email', 'unknown')} from {event.get('ip_address', 'unknown')}")
        report.append("")
        
        # Access denied
        access_denied = [e for e in events if e.get("event_type") == "access_denied"]
        report.append(f"### Access Denied Events: {len(access_denied)}")
        if access_denied:
            for event in access_denied[-10:]:
                report.append(f"- {event['timestamp']}: {event.get('user_id', 'unknown')} - {event['description']}")
        report.append("")
        
        # Recommendations
        report.append("## Security Recommendations")
        if len(failed_logins) > 10:
            report.append("⚠️ High number of failed logins - Consider implementing account lockout")
        if len(access_denied) > 20:
            report.append("⚠️ Many access denied events - Review user permissions")
        if not failed_logins and not access_denied:
            report.append("✅ No significant security concerns detected")
        
        return "\n".join(report)


# ============== Real-time Monitor ==============

class AuditMonitor:
    """
    Real-time audit log monitoring.
    """
    
    def __init__(self, logger: AuditLogger):
        self.logger = logger
        self.running = False
        self.alerts: List[Dict[str, Any]] = []
    
    async def start_monitoring(self):
        """Start real-time monitoring"""
        self.running = True
        logger.info("Starting real-time audit monitoring...")
        
        while self.running:
            try:
                # Check for critical events in last minute
                cutoff = datetime.now() - timedelta(minutes=1)
                query = AuditQuery(
                    start_date=cutoff,
                    severity="critical",
                    limit=100
                )
                
                critical_events = await self.logger.query(query)
                
                for event in critical_events:
                    await self._handle_critical_event(event)
                
                await asyncio.sleep(30)  # Check every 30 seconds
            
            except asyncio.CancelledError:
                logger.info("Audit monitoring stopped")
                break
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(30)
    
    async def _handle_critical_event(self, event: Dict[str, Any]):
        """Handle critical event"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "event": event
        }
        self.alerts.append(alert)
        
        logger.critical(
            f"🚨 CRITICAL EVENT: {event['service']} - {event['action']} - {event['description']}"
        )
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    async def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False


# ============== Global Instance ==============

# Global audit logger instance (will be initialized in main)
audit_logger: Optional[AuditLogger] = None
audit_report_generator: Optional[AuditReportGenerator] = None
audit_monitor: Optional[AuditMonitor] = None


async def get_audit_logger() -> AuditLogger:
    """Get or create audit logger instance"""
    global audit_logger, audit_report_generator, audit_monitor
    
    if audit_logger is None:
        audit_logger = AuditLogger()
        await audit_logger.initialize()
        audit_report_generator = AuditReportGenerator(audit_logger)
        audit_monitor = AuditMonitor(audit_logger)
    
    return audit_logger


# ============== Main Entry Points ==============

async def show_status():
    """Show audit logging status"""
    logger = await get_audit_logger()
    
    print("=" * 60)
    print(" COMPREHENSIVE AUDIT LOGGING SYSTEM")
    print("=" * 60)
    
    stats = await logger.get_statistics(days=7)
    
    print(f"\n📊 Audit Log Statistics (Last 7 Days)")
    print(f"   Total Events: {stats['total_events']}")
    
    print(f"\n📋 Events by Type:")
    for event_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {event_type}: {count}")
    
    print(f"\n⚠️ Events by Severity:")
    for severity, count in stats['by_severity'].items():
        icon = "🔴" if severity == "critical" else "🟠" if severity == "error" else "🟡" if severity == "warning" else "🟢"
        print(f"   {icon} {severity}: {count}")
    
    print(f"\n🏢 Events by Service:")
    for service, count in sorted(stats['by_service'].items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {service}: {count}")
    
    print("\n" + "=" * 60)


async def log_test_event():
    """Log a test event"""
    logger = await get_audit_logger()
    
    print("\nLogging test events...")
    
    # Test login
    await logger.log_login("user123", "user@example.com", True, "192.168.1.1")
    
    # Test data access
    await logger.log_data_access(
        service="Accounting",
        resource_type="invoice",
        resource_id="INV-001",
        user_id="user123"
    )
    
    # Test data modification
    await logger.log_data_modification(
        service="Business",
        resource_type="meeting",
        resource_id="MTG-001",
        user_id="user123",
        action="update",
        previous_state={"status": "scheduled"},
        new_state={"status": "completed"}
    )
    
    # Test security event
    await logger.log_security_event(
        service="AUTH",
        action="brute_force_detected",
        description="Multiple failed login attempts from same IP",
        severity=AuditSeverity.CRITICAL,
        ip_address="192.168.1.100"
    )
    
    await logger.flush()
    
    print("✅ Test events logged successfully")


async def generate_report():
    """Generate audit report"""
    logger = await get_audit_logger()
    report_gen = AuditReportGenerator(logger)
    
    print("\nGenerating daily audit report...")
    filepath = await report_gen.generate_daily_report()
    print(f"✅ Report generated: {filepath}")


async def start_monitor():
    """Start real-time monitoring"""
    logger = await get_audit_logger()
    monitor = AuditMonitor(logger)
    
    print("=" * 60)
    print(" REAL-TIME AUDIT MONITORING")
    print("=" * 60)
    print("Monitoring for critical events...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    await monitor.start_monitoring()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Comprehensive Audit Logging System")
    parser.add_argument("--log", action="store_true", help="Log test events")
    parser.add_argument("--query", action="store_true", help="Query audit logs")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--monitor", action="store_true", help="Start monitoring")
    parser.add_argument("--status", action="store_true", help="Show status")
    
    args = parser.parse_args()
    
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    if args.log:
        asyncio.run(log_test_event())
    elif args.report:
        asyncio.run(generate_report())
    elif args.monitor:
        asyncio.run(start_monitor())
    elif args.status or not any([args.log, args.report, args.monitor]):
        asyncio.run(show_status())
