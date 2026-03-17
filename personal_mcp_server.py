"""
Personal MCP Server

FastAPI service that handles personal domain operations including:
- Personal appointments and calendar management
- Reminders and notifications
- Family task coordination
- Health and fitness tracking
- Travel planning
- Personal finance tracking (non-business)
- Personal communications

Supports cross-domain integration with Business domain for work-life balance.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager
import hashlib
import aiofiles

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for startup/shutdown events"""
    logger.info("Initializing Personal MCP Server...")
    logger.info("Personal MCP Server ready")
    yield
    logger.info("Shutting down Personal MCP Server...")


app = FastAPI(
    title="Personal MCP Server",
    version="1.0.0",
    lifespan=lifespan,
    description="Personal domain operations with cross-domain integration"
)


# ============== Request/Response Models ==============

class JSONRPCResponse(BaseModel):
    """Standard response model"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: str


class CreateAppointmentRequest(BaseModel):
    """Request model for creating appointments"""
    title: str
    description: str
    dates: Optional[list[str]] = None
    location: Optional[str] = None
    reminder_minutes: Optional[int] = 15


class CreateReminderRequest(BaseModel):
    """Request model for creating reminders"""
    title: str
    description: str
    reminder_date: Optional[str] = None
    priority: Optional[str] = "medium"


class CreateTravelPlanRequest(BaseModel):
    """Request model for travel planning"""
    description: str
    dates: Optional[list[str]] = None
    destinations: Optional[list[str]] = None
    budget: Optional[str] = None


class TrackPersonalExpenseRequest(BaseModel):
    """Request model for tracking personal expenses"""
    description: str
    amount: Optional[str] = None
    date: Optional[str] = None
    category: Optional[str] = "general"


class SendPersonalMessageRequest(BaseModel):
    """Request model for sending personal communications"""
    content: str
    recipients: Optional[list[str]] = None
    method: Optional[str] = "email"


class FlagPersonalImpactRequest(BaseModel):
    """Request model for cross-domain personal impact flagging"""
    task_id: str
    content: str
    source_domain: str


# ============== Personal Data Manager ==============

class PersonalDataManager:
    """Manages personal data storage and retrieval"""
    
    def __init__(self):
        self.data_file = "state/personal_data.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists"""
        os.makedirs("state", exist_ok=True)
        if not os.path.exists(self.data_file):
            self._write_data({
                "appointments": [],
                "reminders": [],
                "travel_plans": [],
                "expenses": [],
                "cross_domain_flags": []
            })
    
    def _read_data(self) -> Dict[str, Any]:
        """Read data from file"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "appointments": [],
                "reminders": [],
                "travel_plans": [],
                "expenses": [],
                "cross_domain_flags": []
            }
    
    def _write_data(self, data: Dict[str, Any]):
        """Write data to file"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    
    def add_appointment(self, appointment: Dict[str, Any]) -> str:
        """Add a new appointment"""
        data = self._read_data()
        appointment["id"] = f"appt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(appointment['title'].encode()).hexdigest()[:8]}"
        appointment["created_at"] = datetime.now().isoformat()
        appointment["status"] = "scheduled"
        data["appointments"].append(appointment)
        self._write_data(data)
        return appointment["id"]
    
    def add_reminder(self, reminder: Dict[str, Any]) -> str:
        """Add a new reminder"""
        data = self._read_data()
        reminder["id"] = f"rem_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(reminder['title'].encode()).hexdigest()[:8]}"
        reminder["created_at"] = datetime.now().isoformat()
        reminder["status"] = "pending"
        data["reminders"].append(reminder)
        self._write_data(data)
        return reminder["id"]
    
    def add_travel_plan(self, travel_plan: Dict[str, Any]) -> str:
        """Add a new travel plan"""
        data = self._read_data()
        travel_plan["id"] = f"travel_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(travel_plan['description'][:20].encode()).hexdigest()[:8]}"
        travel_plan["created_at"] = datetime.now().isoformat()
        travel_plan["status"] = "planning"
        data["travel_plans"].append(travel_plan)
        self._write_data(data)
        return travel_plan["id"]
    
    def add_expense(self, expense: Dict[str, Any]) -> str:
        """Add a new personal expense"""
        data = self._read_data()
        expense["id"] = f"exp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(expense['description'].encode()).hexdigest()[:8]}"
        expense["created_at"] = datetime.now().isoformat()
        expense["domain"] = "personal"
        data["expenses"].append(expense)
        self._write_data(data)
        return expense["id"]
    
    def add_cross_domain_flag(self, flag: Dict[str, Any]) -> str:
        """Add a cross-domain flag (from Business domain)"""
        data = self._read_data()
        flag["id"] = f"cross_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(flag['task_id'].encode()).hexdigest()[:8]}"
        flag["created_at"] = datetime.now().isoformat()
        flag["status"] = "flagged"
        data["cross_domain_flags"].append(flag)
        self._write_data(data)
        return flag["id"]
    
    def get_appointments(self, limit: int = 10) -> list:
        """Get recent appointments"""
        data = self._read_data()
        return data["appointments"][-limit:]
    
    def get_reminders(self, limit: int = 10) -> list:
        """Get pending reminders"""
        data = self._read_data()
        return [r for r in data["reminders"] if r.get("status") == "pending"][-limit:]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get personal data summary"""
        data = self._read_data()
        return {
            "total_appointments": len(data["appointments"]),
            "pending_reminders": len([r for r in data["reminders"] if r.get("status") == "pending"]),
            "travel_plans": len(data["travel_plans"]),
            "tracked_expenses": len(data["expenses"]),
            "cross_domain_flags": len(data["cross_domain_flags"])
        }


# ============== Request Logger ==============

class PersonalRequestLogger:
    """Logs all requests to personal_log.md"""
    
    def __init__(self):
        self.log_file = "logs/personal_log.md"
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Ensure log file exists"""
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("# Personal MCP Server Log\n\n")
    
    async def log_request(self, action: str, request_data: Dict[str, Any], 
                         response: JSONRPCResponse):
        """Log a request and response"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
## {action} - {timestamp}
- **Status:** {"✅ Success" if response.success else "❌ Error"}
- **Request:** {json.dumps(request_data, indent=2)[:200]}...
- **Response:** {json.dumps(response.data if response.success else response.error, indent=2)[:200]}...

---
"""
        
        async with aiofiles.open(self.log_file, "a", encoding="utf-8") as f:
            await f.write(log_entry)


# ============== Global Instances ==============

data_manager = PersonalDataManager()
request_logger = PersonalRequestLogger()


# ============== API Endpoints ==============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Personal MCP Server",
        "timestamp": datetime.now().isoformat(),
        "summary": data_manager.get_summary()
    }


@app.post("/api/create_appointment", response_model=JSONRPCResponse)
async def create_appointment(request: CreateAppointmentRequest):
    """Create a new personal appointment"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.title}".encode()).hexdigest()[:12]
    
    try:
        appointment_data = {
            "title": request.title,
            "description": request.description,
            "dates": request.dates,
            "location": request.location,
            "reminder_minutes": request.reminder_minutes
        }
        
        appointment_id = data_manager.add_appointment(appointment_data)
        
        response = JSONRPCResponse(
            success=True,
            data={
                "appointment_id": appointment_id,
                "title": request.title,
                "message": "Appointment created successfully"
            },
            request_id=request_id
        )
        
        await request_logger.log_request("create_appointment", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("create_appointment", request.dict(), response)
        return response


@app.post("/api/create_reminder", response_model=JSONRPCResponse)
async def create_reminder(request: CreateReminderRequest):
    """Create a new personal reminder"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.title}".encode()).hexdigest()[:12]
    
    try:
        reminder_data = {
            "title": request.title,
            "description": request.description,
            "reminder_date": request.reminder_date,
            "priority": request.priority
        }
        
        reminder_id = data_manager.add_reminder(reminder_data)
        
        response = JSONRPCResponse(
            success=True,
            data={
                "reminder_id": reminder_id,
                "title": request.title,
                "message": "Reminder created successfully"
            },
            request_id=request_id
        )
        
        await request_logger.log_request("create_reminder", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("create_reminder", request.dict(), response)
        return response


@app.post("/api/create_travel_plan", response_model=JSONRPCResponse)
async def create_travel_plan(request: CreateTravelPlanRequest):
    """Create a new travel plan"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.description[:50]}".encode()).hexdigest()[:12]
    
    try:
        travel_plan_data = {
            "description": request.description,
            "dates": request.dates,
            "destinations": request.destinations,
            "budget": request.budget
        }
        
        travel_id = data_manager.add_travel_plan(travel_plan_data)
        
        response = JSONRPCResponse(
            success=True,
            data={
                "travel_id": travel_id,
                "message": "Travel plan created successfully",
                "next_steps": [
                    "Research flights and accommodations",
                    "Check passport/visa requirements",
                    "Create packing list",
                    "Set up travel notifications"
                ]
            },
            request_id=request_id
        )
        
        await request_logger.log_request("create_travel_plan", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("create_travel_plan", request.dict(), response)
        return response


@app.post("/api/track_personal_expense", response_model=JSONRPCResponse)
async def track_personal_expense(request: TrackPersonalExpenseRequest):
    """Track a personal expense"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.description}".encode()).hexdigest()[:12]
    
    try:
        expense_data = {
            "description": request.description,
            "amount": request.amount,
            "date": request.date or datetime.now().strftime("%Y-%m-%d"),
            "category": request.category
        }
        
        expense_id = data_manager.add_expense(expense_data)
        
        response = JSONRPCResponse(
            success=True,
            data={
                "expense_id": expense_id,
                "message": "Personal expense tracked successfully"
            },
            request_id=request_id
        )
        
        await request_logger.log_request("track_personal_expense", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("track_personal_expense", request.dict(), response)
        return response


@app.post("/api/send_personal_message", response_model=JSONRPCResponse)
async def send_personal_message(request: SendPersonalMessageRequest):
    """Send a personal message (email/SMS)"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.content[:50]}".encode()).hexdigest()[:12]
    
    try:
        # In a real implementation, this would integrate with email/SMS services
        message_data = {
            "content": request.content,
            "recipients": request.recipients,
            "method": request.method,
            "sent_at": datetime.now().isoformat()
        }
        
        response = JSONRPCResponse(
            success=True,
            data={
                "message": f"Personal message prepared for sending via {request.method}",
                "recipients_count": len(request.recipients) if request.recipients else 0,
                "note": "Message queued (requires email/SMS service integration)"
            },
            request_id=request_id
        )
        
        await request_logger.log_request("send_personal_message", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("send_personal_message", request.dict(), response)
        return response


@app.post("/api/flag_personal_impact", response_model=JSONRPCResponse)
async def flag_personal_impact(request: FlagPersonalImpactRequest):
    """
    Flag a task from another domain (Business) that has personal impact.
    This is a CROSS-DOMAIN INTEGRATION endpoint.
    """
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.task_id}".encode()).hexdigest()[:12]
    
    try:
        cross_domain_data = {
            "task_id": request.task_id,
            "content": request.content,
            "source_domain": request.source_domain,
            "impact_type": "work_life_balance",
            "requires_attention": True
        }
        
        flag_id = data_manager.add_cross_domain_flag(cross_domain_data)
        
        # Analyze for work-life balance concerns
        content_lower = request.content.lower()
        concerns = []
        
        if any(word in content_lower for word in ["weekend", "evening", "night", "late"]):
            concerns.append("⚠️ Task may intrude on personal time")
        
        if any(word in content_lower for word in ["urgent", "asap", "immediate", "emergency"]):
            concerns.append("⚠️ High-pressure task detected - consider stress management")
        
        if any(word in content_lower for word in ["vacation", "time off", "leave", "holiday"]):
            concerns.append("ℹ️ Task relates to time off - ensure proper handover")
        
        response = JSONRPCResponse(
            success=True,
            data={
                "flag_id": flag_id,
                "message": "Personal impact flagged successfully",
                "source_domain": request.source_domain,
                "concerns": concerns,
                "recommendations": [
                    "Review work-life balance",
                    "Consider delegating if overloaded",
                    "Schedule personal time for recovery"
                ] if concerns else ["No immediate work-life balance concerns detected"]
            },
            request_id=request_id
        )
        
        await request_logger.log_request("flag_personal_impact", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("flag_personal_impact", request.dict(), response)
        return response


@app.get("/api/get_personal_summary", response_model=JSONRPCResponse)
async def get_personal_summary():
    """Get summary of personal domain data"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}summary".encode()).hexdigest()[:12]
    
    try:
        summary = data_manager.get_summary()
        summary["recent_appointments"] = data_manager.get_appointments(5)
        summary["pending_reminders"] = data_manager.get_reminders(5)
        
        response = JSONRPCResponse(
            success=True,
            data=summary,
            request_id=request_id
        )
        
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        return response


@app.get("/api/get_cross_domain_flags", response_model=JSONRPCResponse)
async def get_cross_domain_flags():
    """Get all cross-domain flags (from Business domain)"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}cross_domain".encode()).hexdigest()[:12]
    
    try:
        data = data_manager._read_data()
        
        response = JSONRPCResponse(
            success=True,
            data={
                "total_flags": len(data["cross_domain_flags"]),
                "flags": data["cross_domain_flags"][-20:]  # Last 20 flags
            },
            request_id=request_id
        )
        
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        return response


# ============== Main Entry Point ==============

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8003,
        log_level="info"
    )
