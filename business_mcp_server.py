"""
Business MCP Server

FastAPI service that handles business domain operations including:
- Meeting scheduling and management
- Client relationship management (CRM)
- Project tracking
- Sales pipeline management
- Contract management
- Team coordination
- Business communications

Supports cross-domain integration with Personal, Accounting, and Social Media domains.
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
    logger.info("Initializing Business MCP Server...")
    logger.info("Business MCP Server ready")
    yield
    logger.info("Shutting down Business MCP Server...")


app = FastAPI(
    title="Business MCP Server",
    version="1.0.0",
    lifespan=lifespan,
    description="Business domain operations with cross-domain integration"
)


# ============== Request/Response Models ==============

class JSONRPCResponse(BaseModel):
    """Standard response model"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: str


class ScheduleMeetingRequest(BaseModel):
    """Request model for scheduling meetings"""
    title: str
    description: str
    dates: Optional[list[str]] = None
    participants: Optional[list[str]] = None
    emails: Optional[list[str]] = None
    location: Optional[str] = None
    meeting_type: Optional[str] = "in_person"


class UpdateCRMRequest(BaseModel):
    """Request model for CRM updates"""
    activity_type: str
    description: str
    companies: Optional[list[str]] = None
    contacts: Optional[list[str]] = None
    value: Optional[str] = None


class UpdateSalesPipelineRequest(BaseModel):
    """Request model for sales pipeline updates"""
    activity_type: str
    description: str
    deal_value: Optional[str] = None
    companies: Optional[list[str]] = None
    stage: Optional[str] = "prospecting"


class FlagFinancialTaskRequest(BaseModel):
    """Request model for cross-domain financial task flagging"""
    task_id: str
    content: str
    source_domain: str


class FlagMarketingTaskRequest(BaseModel):
    """Request model for cross-domain marketing task flagging"""
    task_id: str
    content: str
    source_domain: str


# ============== Business Data Manager ==============

class BusinessDataManager:
    """Manages business data storage and retrieval"""
    
    def __init__(self):
        self.data_file = "state/business_data.json"
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure data file exists"""
        os.makedirs("state", exist_ok=True)
        if not os.path.exists(self.data_file):
            self._write_data({
                "meetings": [],
                "crm_activities": [],
                "sales_pipeline": [],
                "projects": [],
                "contracts": [],
                "cross_domain_flags": {
                    "accounting": [],
                    "personal": [],
                    "social_media": []
                }
            })
    
    def _read_data(self) -> Dict[str, Any]:
        """Read data from file"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "meetings": [],
                "crm_activities": [],
                "sales_pipeline": [],
                "projects": [],
                "contracts": [],
                "cross_domain_flags": {
                    "accounting": [],
                    "personal": [],
                    "social_media": []
                }
            }
    
    def _write_data(self, data: Dict[str, Any]):
        """Write data to file"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    
    def add_meeting(self, meeting: Dict[str, Any]) -> str:
        """Add a new meeting"""
        data = self._read_data()
        meeting["id"] = f"meeting_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(meeting['title'].encode()).hexdigest()[:8]}"
        meeting["created_at"] = datetime.now().isoformat()
        meeting["status"] = "scheduled"
        data["meetings"].append(meeting)
        self._write_data(data)
        return meeting["id"]
    
    def add_crm_activity(self, activity: Dict[str, Any]) -> str:
        """Add a new CRM activity"""
        data = self._read_data()
        activity["id"] = f"crm_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(activity['description'].encode()).hexdigest()[:8]}"
        activity["created_at"] = datetime.now().isoformat()
        activity["status"] = "logged"
        data["crm_activities"].append(activity)
        self._write_data(data)
        return activity["id"]
    
    def add_sales_activity(self, activity: Dict[str, Any]) -> str:
        """Add a new sales pipeline activity"""
        data = self._read_data()
        activity["id"] = f"sales_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(activity['description'].encode()).hexdigest()[:8]}"
        activity["created_at"] = datetime.now().isoformat()
        activity["status"] = "active"
        data["sales_pipeline"].append(activity)
        self._write_data(data)
        return activity["id"]
    
    def add_cross_domain_flag(self, target_domain: str, flag: Dict[str, Any]) -> str:
        """Add a cross-domain flag to another domain"""
        data = self._read_data()
        
        if target_domain not in data["cross_domain_flags"]:
            data["cross_domain_flags"][target_domain] = []
        
        flag["id"] = f"cross_{target_domain}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(flag['task_id'].encode()).hexdigest()[:8]}"
        flag["created_at"] = datetime.now().isoformat()
        flag["status"] = "flagged"
        data["cross_domain_flags"][target_domain].append(flag)
        self._write_data(data)
        return flag["id"]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get business data summary"""
        data = self._read_data()
        return {
            "total_meetings": len(data["meetings"]),
            "scheduled_meetings": len([m for m in data["meetings"] if m.get("status") == "scheduled"]),
            "crm_activities": len(data["crm_activities"]),
            "sales_activities": len(data["sales_pipeline"]),
            "active_deals": len([s for s in data["sales_pipeline"] if s.get("status") == "active"]),
            "cross_domain_flags": {
                domain: len(flags) 
                for domain, flags in data["cross_domain_flags"].items()
            }
        }
    
    def get_sales_pipeline_summary(self) -> Dict[str, Any]:
        """Get sales pipeline summary"""
        data = self._read_data()
        
        total_value = 0
        by_stage = {}
        
        for activity in data["sales_pipeline"]:
            stage = activity.get("stage", "unknown")
            if stage not in by_stage:
                by_stage[stage] = {"count": 0, "value": 0}
            
            by_stage[stage]["count"] += 1
            
            if "deal_value" in activity and activity["deal_value"]:
                try:
                    value = float(activity["deal_value"].replace("$", "").replace(",", ""))
                    by_stage[stage]["value"] += value
                    total_value += value
                except (ValueError, AttributeError):
                    pass
        
        return {
            "total_pipeline_value": total_value,
            "by_stage": by_stage,
            "total_deals": len(data["sales_pipeline"])
        }


# ============== Request Logger ==============

class BusinessRequestLogger:
    """Logs all requests to business_log.md"""
    
    def __init__(self):
        self.log_file = "logs/business_log.md"
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Ensure log file exists"""
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                f.write("# Business MCP Server Log\n\n")
    
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

data_manager = BusinessDataManager()
request_logger = BusinessRequestLogger()


# ============== API Endpoints ==============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Business MCP Server",
        "timestamp": datetime.now().isoformat(),
        "summary": data_manager.get_summary()
    }


@app.post("/api/schedule_meeting", response_model=JSONRPCResponse)
async def schedule_meeting(request: ScheduleMeetingRequest):
    """Schedule a new business meeting"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.title}".encode()).hexdigest()[:12]
    
    try:
        meeting_data = {
            "title": request.title,
            "description": request.description,
            "dates": request.dates,
            "participants": request.participants,
            "emails": request.emails,
            "location": request.location,
            "meeting_type": request.meeting_type
        }
        
        meeting_id = data_manager.add_meeting(meeting_data)
        
        response = JSONRPCResponse(
            success=True,
            data={
                "meeting_id": meeting_id,
                "title": request.title,
                "message": "Meeting scheduled successfully",
                "next_steps": [
                    "Send calendar invites to participants",
                    "Prepare meeting agenda",
                    "Book meeting room if in-person",
                    "Set up video conference link if virtual"
                ]
            },
            request_id=request_id
        )
        
        await request_logger.log_request("schedule_meeting", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("schedule_meeting", request.dict(), response)
        return response


@app.post("/api/update_crm", response_model=JSONRPCResponse)
async def update_crm(request: UpdateCRMRequest):
    """Update CRM with client activity"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.description[:50]}".encode()).hexdigest()[:12]
    
    try:
        crm_data = {
            "activity_type": request.activity_type,
            "description": request.description,
            "companies": request.companies,
            "contacts": request.contacts,
            "value": request.value
        }
        
        activity_id = data_manager.add_crm_activity(crm_data)
        
        response = JSONRPCResponse(
            success=True,
            data={
                "activity_id": activity_id,
                "message": "CRM updated successfully",
                "companies_tracked": request.companies if request.companies else [],
                "contacts_tracked": request.contacts if request.contacts else []
            },
            request_id=request_id
        )
        
        await request_logger.log_request("update_crm", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("update_crm", request.dict(), response)
        return response


@app.post("/api/update_sales_pipeline", response_model=JSONRPCResponse)
async def update_sales_pipeline(request: UpdateSalesPipelineRequest):
    """Update sales pipeline with new activity"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.description[:50]}".encode()).hexdigest()[:12]
    
    try:
        sales_data = {
            "activity_type": request.activity_type,
            "description": request.description,
            "deal_value": request.deal_value,
            "companies": request.companies,
            "stage": request.stage
        }
        
        activity_id = data_manager.add_sales_activity(sales_data)
        
        # Get updated pipeline summary
        pipeline_summary = data_manager.get_sales_pipeline_summary()
        
        response = JSONRPCResponse(
            success=True,
            data={
                "activity_id": activity_id,
                "message": "Sales pipeline updated successfully",
                "pipeline_summary": {
                    "total_value": pipeline_summary["total_pipeline_value"],
                    "total_deals": pipeline_summary["total_deals"]
                }
            },
            request_id=request_id
        )
        
        await request_logger.log_request("update_sales_pipeline", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("update_sales_pipeline", request.dict(), response)
        return response


@app.post("/api/flag_financial_task", response_model=JSONRPCResponse)
async def flag_financial_task(request: FlagFinancialTaskRequest):
    """
    Flag a task from Business domain that has accounting/financial implications.
    This is a CROSS-DOMAIN INTEGRATION endpoint (Business → Accounting).
    """
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.task_id}".encode()).hexdigest()[:12]
    
    try:
        # Store the flag in Business MCP for tracking
        cross_domain_data = {
            "task_id": request.task_id,
            "content": request.content,
            "source_domain": request.source_domain,
            "target_domain": "Accounting",
            "impact_type": "financial"
        }
        
        flag_id = data_manager.add_cross_domain_flag("accounting", cross_domain_data)
        
        # Analyze for financial implications
        content_lower = request.content.lower()
        financial_indicators = []
        
        if any(word in content_lower for word in ["expense", "cost", "payment"]):
            financial_indicators.append("💰 Expense/Payment detected")
        
        if any(word in content_lower for word in ["invoice", "billing", "revenue"]):
            financial_indicators.append("💵 Invoice/Revenue detected")
        
        if any(word in content_lower for word in ["contract", "deal", "agreement"]):
            financial_indicators.append("📋 Contract with financial terms")
        
        response = JSONRPCResponse(
            success=True,
            data={
                "flag_id": flag_id,
                "message": "Financial task flagged for Accounting domain",
                "target_domain": "Accounting",
                "financial_indicators": financial_indicators,
                "recommendations": [
                    "Ensure proper expense categorization",
                    "Track for tax purposes",
                    "Update budget forecasts"
                ] if financial_indicators else ["No immediate financial concerns detected"]
            },
            request_id=request_id
        )
        
        await request_logger.log_request("flag_financial_task", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("flag_financial_task", request.dict(), response)
        return response


@app.post("/api/flag_marketing_task", response_model=JSONRPCResponse)
async def flag_marketing_task(request: FlagMarketingTaskRequest):
    """
    Flag a task from Business domain that has social media/marketing implications.
    This is a CROSS-DOMAIN INTEGRATION endpoint (Business → Social Media).
    """
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.task_id}".encode()).hexdigest()[:12]
    
    try:
        # Store the flag in Business MCP for tracking
        cross_domain_data = {
            "task_id": request.task_id,
            "content": request.content,
            "source_domain": request.source_domain,
            "target_domain": "Social Media",
            "impact_type": "marketing"
        }
        
        flag_id = data_manager.add_cross_domain_flag("social_media", cross_domain_data)
        
        # Analyze for marketing implications
        content_lower = request.content.lower()
        marketing_indicators = []
        
        if any(word in content_lower for word in ["campaign", "promotion", "launch"]):
            marketing_indicators.append("📢 Campaign/Promotion detected")
        
        if any(word in content_lower for word in ["brand", "awareness", "visibility"]):
            marketing_indicators.append("🎯 Brand awareness initiative")
        
        if any(word in content_lower for word in ["social media", "facebook", "instagram", "linkedin"]):
            marketing_indicators.append("📱 Social media component identified")
        
        response = JSONRPCResponse(
            success=True,
            data={
                "flag_id": flag_id,
                "message": "Marketing task flagged for Social Media domain",
                "target_domain": "Social Media",
                "marketing_indicators": marketing_indicators,
                "recommendations": [
                    "Coordinate with social media team",
                    "Prepare content calendar",
                    "Set up tracking metrics"
                ] if marketing_indicators else ["No immediate marketing concerns detected"]
            },
            request_id=request_id
        )
        
        await request_logger.log_request("flag_marketing_task", request.dict(), response)
        return response
        
    except Exception as e:
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        await request_logger.log_request("flag_marketing_task", request.dict(), response)
        return response


@app.get("/api/get_business_summary", response_model=JSONRPCResponse)
async def get_business_summary():
    """Get summary of business domain data"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}summary".encode()).hexdigest()[:12]
    
    try:
        summary = data_manager.get_summary()
        summary["pipeline_details"] = data_manager.get_sales_pipeline_summary()
        
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
    """Get all cross-domain flags (to other domains)"""
    request_id = hashlib.md5(f"{datetime.now().isoformat()}cross_domain".encode()).hexdigest()[:12]
    
    try:
        data = data_manager._read_data()
        
        response = JSONRPCResponse(
            success=True,
            data={
                "total_flags": sum(len(flags) for flags in data["cross_domain_flags"].values()),
                "flags_by_domain": {
                    domain: flags[-10:]  # Last 10 per domain
                    for domain, flags in data["cross_domain_flags"].items()
                }
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
        port=8004,
        log_level="info"
    )
