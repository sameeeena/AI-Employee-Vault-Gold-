"""
Cross-Domain Orchestrator

Manages integration and data flow between domains:
- Personal ↔ Business (work-life balance, expense classification)
- Business ↔ Accounting (financial task routing)
- Business ↔ Social Media (marketing coordination)
- Personal ↔ Accounting (personal finance tracking)

Provides unified task routing with cross-domain awareness.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
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


class CrossDomainOrchestrator:
    """
    Orchestrates tasks across multiple domains with intelligent routing
    and cross-domain integration.
    """
    
    def __init__(self):
        # MCP Server URLs
        self.mcp_urls = {
            "Personal": os.getenv("PERSONAL_MCP_URL", "http://localhost:8003"),
            "Business": os.getenv("BUSINESS_MCP_URL", "http://localhost:8004"),
            "Accounting": os.getenv("ACCOUNTING_MCP_URL", "http://localhost:8001"),
            "Social Media": os.getenv("SOCIAL_MCP_URL", "http://localhost:8002")
        }
        
        # Skill mappings
        self.skill_mapping = {
            "Personal": "personal_assistant_skill",
            "Business": "business_analyst_skill",
            "Accounting": "accounting_assistant_skill",
            "Social Media": "social_media_manager_skill"
        }
        
        # Cross-domain integration rules
        self.integration_rules = self._load_integration_rules()
        
        # HTTP client timeout
        self.timeout = httpx.Timeout(30.0)
        
        logger.info("Cross-Domain Orchestrator initialized")
    
    def _load_integration_rules(self) -> Dict[str, Any]:
        """Load cross-domain integration rules"""
        return {
            "Personal": {
                "can_trigger": ["Accounting"],
                "can_receive_from": ["Business"],
                "integration_endpoints": {
                    "Accounting": "track_personal_expense"
                }
            },
            "Business": {
                "can_trigger": ["Accounting", "Personal", "Social Media"],
                "can_receive_from": [],
                "integration_endpoints": {
                    "Accounting": "flag_financial_task",
                    "Personal": "flag_personal_impact",
                    "Social Media": "flag_marketing_task"
                }
            },
            "Accounting": {
                "can_trigger": [],
                "can_receive_from": ["Personal", "Business"],
                "integration_endpoints": {}
            },
            "Social Media": {
                "can_trigger": [],
                "can_receive_from": ["Business"],
                "integration_endpoints": {}
            }
        }
    
    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task with cross-domain awareness.
        
        Args:
            task_data: Dictionary containing:
                - task_id: Unique task identifier
                - content: Task content
                - primary_domain: Initially classified domain
                - metadata: Additional metadata
                - sender: Task sender
                
        Returns:
            Dictionary with processing results including cross-domain actions
        """
        task_id = task_data.get("task_id", "")
        content = task_data.get("content", "")
        primary_domain = task_data.get("primary_domain", "Business")
        
        logger.info(f"Processing task {task_id} in domain {primary_domain}")
        
        result = {
            "task_id": task_id,
            "primary_domain": primary_domain,
            "status": "processing",
            "domain_result": None,
            "cross_domain_actions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Step 1: Process in primary domain
            domain_result = self._process_in_domain(task_data, primary_domain)
            result["domain_result"] = domain_result
            
            # Step 2: Check for cross-domain implications
            cross_domain_actions = self._check_cross_domain_implications(
                task_data, primary_domain, domain_result
            )
            result["cross_domain_actions"] = cross_domain_actions
            
            # Step 3: Execute cross-domain integrations
            for action in cross_domain_actions:
                self._execute_cross_domain_action(action, task_data)
            
            result["status"] = "completed"
            logger.info(f"Task {task_id} completed with {len(cross_domain_actions)} cross-domain actions")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            logger.error(f"Error processing task {task_id}: {str(e)}")
        
        return result
    
    def _process_in_domain(self, task_data: Dict[str, Any], domain: str) -> Dict[str, Any]:
        """Process task within a specific domain"""
        # In a full implementation, this would call the appropriate skill
        # For now, we'll call the MCP server health endpoint to verify connectivity
        
        mcp_url = self.mcp_urls.get(domain)
        
        if not mcp_url:
            return {
                "status": "error",
                "message": f"Unknown domain: {domain}"
            }
        
        try:
            # Call the domain's MCP server
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{mcp_url}/health")
                response.raise_for_status()
                health_data = response.json()
                
                return {
                    "status": "success",
                    "domain": domain,
                    "server_status": health_data.get("status", "unknown"),
                    "message": f"Task processed in {domain} domain"
                }
                
        except httpx.ConnectError:
            return {
                "status": "warning",
                "domain": domain,
                "server_status": "unavailable",
                "message": f"{domain} MCP Server not available - task queued"
            }
        except Exception as e:
            return {
                "status": "error",
                "domain": domain,
                "message": f"Error processing in {domain}: {str(e)}"
            }
    
    def _check_cross_domain_implications(self, task_data: Dict[str, Any], 
                                         primary_domain: str,
                                         domain_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check if task has implications for other domains.
        
        Returns list of cross-domain actions to execute.
        """
        cross_domain_actions = []
        content = task_data.get("content", "").lower()
        
        # Get integration rules for primary domain
        rules = self.integration_rules.get(primary_domain, {})
        can_trigger = rules.get("can_trigger", [])
        
        # Check for Business domain cross-domain triggers
        if primary_domain == "Business":
            # Check for Accounting implications
            accounting_keywords = ["expense", "budget", "invoice", "payment", "revenue", 
                                  "cost", "financial", "tax", "billing"]
            if any(keyword in content for keyword in accounting_keywords):
                if "Accounting" in can_trigger:
                    cross_domain_actions.append({
                        "target_domain": "Accounting",
                        "action_type": "flag_financial_task",
                        "reason": "Financial keywords detected in business task",
                        "priority": "high"
                    })
            
            # Check for Personal implications (work-life balance)
            personal_keywords = ["weekend", "evening", "late", "urgent", "asap",
                               "vacation", "time off", "holiday", "work-life"]
            if any(keyword in content for keyword in personal_keywords):
                if "Personal" in can_trigger:
                    cross_domain_actions.append({
                        "target_domain": "Personal",
                        "action_type": "flag_personal_impact",
                        "reason": "Work-life balance keywords detected",
                        "priority": "medium"
                    })
            
            # Check for Social Media implications
            social_keywords = ["social media", "post", "campaign", "marketing",
                             "facebook", "instagram", "linkedin", "twitter", "brand"]
            if any(keyword in content for keyword in social_keywords):
                if "Social Media" in can_trigger:
                    cross_domain_actions.append({
                        "target_domain": "Social Media",
                        "action_type": "flag_marketing_task",
                        "reason": "Marketing/social media keywords detected",
                        "priority": "medium"
                    })
        
        # Check for Personal domain cross-domain triggers
        if primary_domain == "Personal":
            # Check if personal expense might be business-related
            expense_keywords = ["expense", "purchase", "bought", "paid for", "receipt"]
            business_indicators = ["work", "office", "client", "business", "company"]
            
            if any(keyword in content for keyword in expense_keywords):
                if any(indicator in content for indicator in business_indicators):
                    # This might be a business expense
                    cross_domain_actions.append({
                        "target_domain": "Accounting",
                        "action_type": "flag_potential_business_expense",
                        "reason": "Personal expense with business indicators",
                        "priority": "high",
                        "recommendation": "Review for potential business expense categorization"
                    })
        
        return cross_domain_actions
    
    def _execute_cross_domain_action(self, action: Dict[str, Any], 
                                     task_data: Dict[str, Any]):
        """Execute a cross-domain action"""
        target_domain = action.get("target_domain")
        action_type = action.get("action_type")
        
        logger.info(f"Executing cross-domain action: {action_type} → {target_domain}")
        
        try:
            mcp_url = self.mcp_urls.get(target_domain)
            if not mcp_url:
                logger.warning(f"Unknown target domain: {target_domain}")
                return
            
            # Prepare the cross-domain payload
            payload = {
                "task_id": task_data.get("task_id"),
                "content": task_data.get("content"),
                "source_domain": task_data.get("primary_domain"),
                "action_type": action_type,
                "reason": action.get("reason")
            }
            
            # Execute based on action type
            if action_type == "flag_financial_task":
                self._call_mcp_endpoint(f"{mcp_url}/api/flag_financial_task", payload)
            
            elif action_type == "flag_personal_impact":
                self._call_mcp_endpoint(f"{mcp_url}/api/flag_personal_impact", payload)
            
            elif action_type == "flag_marketing_task":
                self._call_mcp_endpoint(f"{mcp_url}/api/flag_marketing_task", payload)
            
            elif action_type == "track_personal_expense":
                self._call_mcp_endpoint(f"{mcp_url}/api/track_personal_expense", payload)
            
            elif action_type == "flag_potential_business_expense":
                # Flag to accounting server
                accounting_url = self.mcp_urls.get("Accounting")
                if accounting_url:
                    self._call_mcp_endpoint(f"{accounting_url}/api/flag_review_expense", payload)
            
            logger.info(f"Cross-domain action {action_type} executed successfully")
            
        except Exception as e:
            logger.error(f"Error executing cross-domain action {action_type}: {str(e)}")
    
    def _call_mcp_endpoint(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP server endpoint"""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            logger.warning(f"MCP Server unavailable: {url}")
            return {"status": "unavailable", "message": "Server not reachable"}
        except Exception as e:
            logger.error(f"Error calling MCP endpoint {url}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_cross_domain_status(self) -> Dict[str, Any]:
        """Get status of all cross-domain integrations"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "domains": {},
            "integration_health": {}
        }
        
        # Check each domain's MCP server
        for domain, url in self.mcp_urls.items():
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.get(f"{url}/health")
                    response.raise_for_status()
                    health_data = response.json()
                    
                    status["domains"][domain] = {
                        "status": "healthy",
                        "details": health_data
                    }
            except Exception as e:
                status["domains"][domain] = {
                    "status": "unavailable",
                    "error": str(e)
                }
        
        # Check integration health
        for source_domain, rules in self.integration_rules.items():
            can_trigger = rules.get("can_trigger", [])
            status["integration_health"][source_domain] = {
                "can_trigger": can_trigger,
                "integration_count": len(can_trigger)
            }
        
        return status
    
    def get_integration_report(self) -> str:
        """Generate a markdown report of cross-domain integration status"""
        status = self.get_cross_domain_status()
        
        report = f"""# Cross-Domain Integration Report

**Generated:** {status['timestamp']}

## Domain Health Status

| Domain | Status | Details |
|--------|--------|---------|
"""
        
        for domain, details in status["domains"].items():
            status_icon = "✅" if details["status"] == "healthy" else "❌"
            report += f"| {status_icon} {domain} | {details['status']} | {details.get('error', 'Operational')} |\n"
        
        report += "\n## Integration Rules\n\n"
        report += "| Source Domain | Can Trigger | Integration Count |\n"
        report += "|---------------|-------------|-------------------|\n"
        
        for domain, health in status["integration_health"].items():
            triggers = ", ".join(health["can_trigger"]) if health["can_trigger"] else "None"
            report += f"| {domain} | {triggers} | {health['integration_count']} |\n"
        
        report += "\n## Cross-Domain Flow Diagram\n\n"
        report += """```
┌──────────────┐
│   Business   │────────────┐
│   Domain     │            │
└──────────────┘            │
        │                   │
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│  Personal    │    │  Accounting  │
│   Domain     │    │    Domain    │
└──────────────┘    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │Social Media  │
                    │   Domain     │
                    └──────────────┘
```
"""
        
        return report


# Convenience function for direct usage
def cross_domain_orchestrator(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Direct function call interface"""
    orchestrator = CrossDomainOrchestrator()
    return orchestrator.process_task(task_data)


# Example usage when run directly
if __name__ == "__main__":
    orchestrator = CrossDomainOrchestrator()
    
    # Example tasks demonstrating cross-domain integration
    examples = [
        {
            "task_id": "cross_001",
            "content": "Client dinner meeting this evening at 7 PM - expense will be $150",
            "primary_domain": "Business",
            "metadata": {"priority": "high"},
            "sender": "sales_team"
        },
        {
            "task_id": "cross_002",
            "content": "Urgent project deadline - need to work this weekend",
            "primary_domain": "Business",
            "metadata": {},
            "sender": "project_manager"
        },
        {
            "task_id": "cross_003",
            "content": "New marketing campaign launch on Facebook and Instagram next week",
            "primary_domain": "Business",
            "metadata": {"priority": "high"},
            "sender": "marketing_team"
        },
        {
            "task_id": "cross_004",
            "content": "Bought office supplies for work - $45.50 receipt attached",
            "primary_domain": "Personal",
            "metadata": {},
            "sender": "employee"
        }
    ]
    
    print("=" * 70)
    print("CROSS-DOMAIN ORCHESTRATOR - EXAMPLE EXECUTIONS")
    print("=" * 70)
    
    for example in examples:
        print(f"\n{'='*70}")
        print(f"Task: {example['content']}")
        print(f"Domain: {example['primary_domain']}")
        print('='*70)
        
        result = orchestrator.process_task(example)
        print(json.dumps(result, indent=2, default=str))
    
    # Generate integration report
    print("\n" + "=" * 70)
    print("INTEGRATION STATUS REPORT")
    print("=" * 70)
    print(orchestrator.get_integration_report())
