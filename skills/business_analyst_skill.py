"""
Business Analyst Skill

Handles business domain tasks including:
- Business meetings and presentations
- Client relationship management
- Project planning and tracking
- Strategy development
- Team coordination
- Business communications
- Revenue and profit analysis
- Contract and proposal management

Integrates with Business MCP Server for external actions.
Supports cross-domain integration with Personal and Accounting domains.
"""
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import httpx
import os

class BusinessAnalystSkill:
    """Skill for handling business domain tasks"""
    
    def __init__(self):
        self.mcp_server_url = os.getenv("BUSINESS_MCP_URL", "http://localhost:8004")
        self.accounting_mcp_url = os.getenv("ACCOUNTING_MCP_URL", "http://localhost:8001")
        self.timeout = httpx.Timeout(30.0)
        
    def __call__(self, input_data: Dict[str, Any]) -> str:
        """
        Main entry point for the business analyst skill.
        
        Args:
            input_data: Dictionary containing:
                - task_id: Unique identifier for the task
                - content: The task content
                - metadata: Additional metadata
                - sender: Information about sender
                
        Returns:
            JSON string with execution results
        """
        task_id = input_data.get("task_id", "")
        content = input_data.get("content", "")
        metadata = input_data.get("metadata", {})
        sender = input_data.get("sender", "")
        
        # Analyze the business task type
        task_analysis = self._analyze_business_task(content, metadata)
        
        # Execute appropriate action
        result = self._execute_business_action(task_id, content, task_analysis, metadata, sender)
        
        # Log the execution
        self._log_execution(task_id, content, result)
        
        return json.dumps(result, indent=2, default=str)
    
    def _analyze_business_task(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze business task to determine specific category and required actions.
        
        Categories:
        - meeting: Business meetings, presentations, conferences
        - client: Client relationships, customer service
        - project: Project planning, execution, tracking
        - strategy: Business strategy, planning, analysis
        - team: Team management, HR, employee matters
        - sales: Sales, marketing, revenue generation
        - contract: Contracts, proposals, negotiations
        - operations: Daily operations, processes, workflows
        """
        content_lower = content.lower()
        
        category_scores = {
            "meeting": 0,
            "client": 0,
            "project": 0,
            "strategy": 0,
            "team": 0,
            "sales": 0,
            "contract": 0,
            "operations": 0
        }
        
        # Meeting keywords
        meeting_keywords = ["meeting", "presentation", "conference", "seminar", "workshop",
                           "board meeting", "standup", "briefing", "webinar", "call with"]
        for keyword in meeting_keywords:
            if keyword in content_lower:
                category_scores["meeting"] += 2
        
        # Client keywords
        client_keywords = ["client", "customer", "customer service", "support ticket",
                          "client feedback", "customer complaint", "account management",
                          "client meeting", "customer onboarding"]
        for keyword in client_keywords:
            if keyword in content_lower:
                category_scores["client"] += 2
        
        # Project keywords
        project_keywords = ["project", "milestone", "deliverable", "deadline", "sprint",
                           "agile", "scrum", "kanban", "task management", "timeline",
                           "gantt", "roadmap", "backlog"]
        for keyword in project_keywords:
            if keyword in content_lower:
                category_scores["project"] += 2
        
        # Strategy keywords
        strategy_keywords = ["strategy", "strategic", "business plan", "roadmap",
                            "competitive analysis", "market analysis", "swot", "kpi",
                            "objective", "goal setting", "vision", "mission"]
        for keyword in strategy_keywords:
            if keyword in content_lower:
                category_scores["strategy"] += 2
        
        # Team keywords
        team_keywords = ["team", "employee", "staff", "hr", "human resources", "hiring",
                        "recruitment", "onboarding", "training", "performance review",
                        "team building", "management", "supervisor", "report to"]
        for keyword in team_keywords:
            if keyword in content_lower:
                category_scores["team"] += 2
        
        # Sales keywords
        sales_keywords = ["sales", "revenue", "marketing", "lead", "prospect", "pipeline",
                         "conversion", "quota", "target", "campaign", "promotion",
                         "business development", "partnership", "deal", "closing"]
        for keyword in sales_keywords:
            if keyword in content_lower:
                category_scores["sales"] += 2
        
        # Contract keywords
        contract_keywords = ["contract", "agreement", "proposal", "negotiation", "terms",
                            "legal", "ndc", "sla", "service agreement", "vendor contract",
                            "partnership agreement", "amendment", "sign off"]
        for keyword in contract_keywords:
            if keyword in content_lower:
                category_scores["contract"] += 2
        
        # Operations keywords
        operations_keywords = ["operations", "process", "workflow", "efficiency",
                              "optimization", "automation", "standard operating procedure",
                              "sop", "quality assurance", "compliance", "audit", "reporting"]
        for keyword in operations_keywords:
            if keyword in content_lower:
                category_scores["operations"] += 2
        
        # Determine primary category
        primary_category = max(category_scores, key=category_scores.get)
        confidence = category_scores[primary_category] / max(sum(category_scores.values()), 1)
        
        # Extract entities
        entities = self._extract_business_entities(content, primary_category)
        
        # Check for cross-domain implications
        cross_domain_analysis = self._analyze_cross_domain(content, primary_category)
        
        return {
            "primary_category": primary_category,
            "confidence": round(confidence, 2),
            "category_scores": category_scores,
            "entities": entities,
            "cross_domain": cross_domain_analysis,
            "requires_external_action": self._requires_external_action(primary_category),
            "suggested_priority": self._suggest_priority(primary_category, metadata)
        }
    
    def _extract_business_entities(self, content: str, category: str) -> Dict[str, Any]:
        """Extract relevant business entities"""
        entities = {}
        content_lower = content.lower()
        
        # Extract dates/times
        date_patterns = [
            r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
            r'\b(\d{1,2}:\d{2}\s*[AP]?M?)\b',
            r'\b(today|tomorrow|yesterday|next week|this week|q1|q2|q3|q4)\b',
            r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
        ]
        
        dates_found = []
        for pattern in date_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dates_found.extend(matches)
        
        if dates_found:
            entities["dates"] = list(set(dates_found))
        
        # Extract monetary amounts
        amount_pattern = r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        amounts = re.findall(amount_pattern, content)
        if amounts:
            entities["amounts"] = amounts
        
        # Extract percentages
        percent_pattern = r'(\d+(?:\.\d+)?\s*%)'
        percentages = re.findall(percent_pattern, content)
        if percentages:
            entities["percentages"] = percentages
        
        # Extract people names (simple heuristic - capitalized words)
        name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        names = re.findall(name_pattern, content)
        # Filter out common non-name phrases
        non_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 
                     "Saturday", "Sunday", "January", "February", "March", "April",
                     "May", "June", "July", "August", "September", "October", 
                     "November", "December"]
        names = [n for n in names if n not in non_names]
        if names:
            entities["people"] = names
        
        # Extract company names (heuristic)
        company_indicators = ["Inc", "LLC", "Ltd", "Corp", "Corporation", "Company", "Co"]
        for indicator in company_indicators:
            pattern = r'\b([A-Z][a-zA-Z]+\s+' + indicator + r'\.?)\b'
            companies = re.findall(pattern, content)
            if companies:
                if "companies" not in entities:
                    entities["companies"] = []
                entities["companies"].extend(companies)
        
        # Extract project codes/names
        project_pattern = r'\b((?:project|proj|prj)[-\s]?[A-Za-z0-9]+)\b'
        projects = re.findall(project_pattern, content, re.IGNORECASE)
        if projects:
            entities["projects"] = projects
        
        # Extract email addresses
        email_pattern = r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
        emails = re.findall(email_pattern, content)
        if emails:
            entities["emails"] = emails
        
        return entities
    
    def _analyze_cross_domain(self, content: str, primary_category: str) -> Dict[str, Any]:
        """Analyze if task has cross-domain implications"""
        cross_domain = {
            "has_personal_implication": False,
            "has_accounting_implication": False,
            "has_social_media_implication": False,
            "reasons": []
        }
        
        content_lower = content.lower()
        
        # Check for personal domain overlap
        personal_indicators = ["personal", "family", "home office", "work-life balance",
                               "vacation", "time off", "personal development"]
        for indicator in personal_indicators:
            if indicator in content_lower:
                cross_domain["has_personal_implication"] = True
                cross_domain["reasons"].append(f"Personal domain overlap: {indicator}")
        
        # Check for accounting domain overlap
        accounting_indicators = ["expense", "budget", "invoice", "payment", "cost",
                                "revenue", "financial", "tax", "receipt", "reimbursement",
                                "profit", "loss", "billing", "accounts"]
        for indicator in accounting_indicators:
            if indicator in content_lower:
                cross_domain["has_accounting_implication"] = True
                cross_domain["reasons"].append(f"Accounting domain overlap: {indicator}")
        
        # Check for social media domain overlap
        social_indicators = ["social media", "facebook", "instagram", "twitter", "linkedin",
                            "post", "tweet", "share", "marketing campaign", "brand awareness"]
        for indicator in social_indicators:
            if indicator in content_lower:
                cross_domain["has_social_media_implication"] = True
                cross_domain["reasons"].append(f"Social media domain overlap: {indicator}")
        
        return cross_domain
    
    def _requires_external_action(self, category: str) -> bool:
        """Determine if category requires external MCP server action"""
        external_categories = ["meeting", "client", "sales", "contract", "operations"]
        return category in external_categories
    
    def _suggest_priority(self, category: str, metadata: Dict[str, Any]) -> str:
        """Suggest priority based on category and metadata"""
        if "priority" in metadata:
            return metadata["priority"]
        
        priority_mapping = {
            "client": "high",
            "contract": "high",
            "sales": "high",
            "meeting": "medium",
            "project": "medium",
            "strategy": "medium",
            "team": "medium",
            "operations": "low"
        }
        
        return priority_mapping.get(category, "medium")
    
    def _execute_business_action(self, task_id: str, content: str, 
                                  task_analysis: Dict[str, Any], 
                                  metadata: Dict[str, Any],
                                  sender: str) -> Dict[str, Any]:
        """Execute the appropriate business action"""
        category = task_analysis["primary_category"]
        entities = task_analysis["entities"]
        cross_domain = task_analysis["cross_domain"]
        
        result = {
            "task_id": task_id,
            "category": category,
            "status": "pending",
            "actions_taken": [],
            "recommendations": [],
            "cross_domain_analysis": cross_domain,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Category-specific handling
            if category == "meeting":
                result = self._handle_meeting(task_id, content, entities, result)
            elif category == "client":
                result = self._handle_client(task_id, content, entities, result)
            elif category == "project":
                result = self._handle_project(task_id, content, entities, result)
            elif category == "strategy":
                result = self._handle_strategy(task_id, content, entities, result)
            elif category == "team":
                result = self._handle_team(task_id, content, entities, result)
            elif category == "sales":
                result = self._handle_sales(task_id, content, entities, result)
            elif category == "contract":
                result = self._handle_contract(task_id, content, entities, result)
            elif category == "operations":
                result = self._handle_operations(task_id, content, entities, result)
            else:
                result["status"] = "categorized"
                result["actions_taken"].append(f"Task categorized as {category}")
            
            # Handle cross-domain integrations
            if cross_domain["has_accounting_implication"]:
                result = self._trigger_accounting_integration(task_id, content, result)
            
            if cross_domain["has_personal_implication"]:
                result = self._trigger_personal_integration(task_id, content, result)
            
            if cross_domain["has_social_media_implication"]:
                result = self._trigger_social_integration(task_id, content, result)
            
            result["status"] = "completed"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _handle_meeting(self, task_id: str, content: str, 
                       entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle meeting-related tasks"""
        result["actions_taken"].append("Analyzed meeting request")
        
        if "dates" in entities:
            result["actions_taken"].append(f"Extracted date/time: {entities['dates']}")
        
        if "people" in entities:
            result["actions_taken"].append(f"Identified participants: {entities['people']}")
        
        # Try to call Business MCP Server for meeting scheduling
        try:
            mcp_response = self._call_business_mcp("schedule_meeting", {
                "title": content[:100],
                "description": content,
                "dates": entities.get("dates", []),
                "participants": entities.get("people", []),
                "emails": entities.get("emails", [])
            })
            if mcp_response.get("success"):
                result["actions_taken"].append("Meeting scheduled via Business MCP Server")
                result["mcp_response"] = mcp_response
        except Exception as e:
            result["recommendations"].append(f"Business MCP Server unavailable: {str(e)}")
        
        result["recommendations"].append("Prepare agenda and materials")
        result["recommendations"].append("Send calendar invites to participants")
        
        return result
    
    def _handle_client(self, task_id: str, content: str, 
                      entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle client-related tasks"""
        result["actions_taken"].append("Analyzed client task")
        
        if "companies" in entities:
            result["actions_taken"].append(f"Identified client companies: {entities['companies']}")
        
        if "emails" in entities:
            result["actions_taken"].append(f"Extracted contact emails: {entities['emails']}")
        
        # Try to call Business MCP Server for CRM update
        try:
            mcp_response = self._call_business_mcp("update_crm", {
                "activity_type": "client_interaction",
                "description": content,
                "companies": entities.get("companies", []),
                "contacts": entities.get("emails", [])
            })
            if mcp_response.get("success"):
                result["actions_taken"].append("CRM updated via Business MCP Server")
                result["mcp_response"] = mcp_response
        except Exception as e:
            result["recommendations"].append(f"Business MCP Server unavailable: {str(e)}")
        
        result["recommendations"].append("Follow up within 24-48 hours")
        result["recommendations"].append("Document interaction in CRM")
        
        return result
    
    def _handle_project(self, task_id: str, content: str, 
                       entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle project-related tasks"""
        result["actions_taken"].append("Analyzed project task")
        
        if "projects" in entities:
            result["actions_taken"].append(f"Identified projects: {entities['projects']}")
        
        if "dates" in entities:
            result["actions_taken"].append(f"Extracted deadlines: {entities['dates']}")
        
        if "people" in entities:
            result["actions_taken"].append(f"Identified team members: {entities['people']}")
        
        result["recommendations"].append("Update project timeline")
        result["recommendations"].append("Assign tasks to team members")
        result["recommendations"].append("Track progress in project management tool")
        
        return result
    
    def _handle_strategy(self, task_id: str, content: str, 
                        entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle strategy-related tasks"""
        result["actions_taken"].append("Analyzed strategic task")
        
        if "amounts" in entities:
            result["actions_taken"].append(f"Identified financial targets: {entities['amounts']}")
        
        if "percentages" in entities:
            result["actions_taken"].append(f"Identified metrics: {entities['percentages']}")
        
        result["recommendations"].append("Schedule strategic planning session")
        result["recommendations"].append("Gather relevant market data")
        result["recommendations"].append("Prepare SWOT analysis")
        
        return result
    
    def _handle_team(self, task_id: str, content: str, 
                    entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle team-related tasks"""
        result["actions_taken"].append("Analyzed team task")
        
        if "people" in entities:
            result["actions_taken"].append(f"Identified team members: {entities['people']}")
        
        result["recommendations"].append("Schedule team meeting if needed")
        result["recommendations"].append("Update team task board")
        result["recommendations"].append("Consider workload distribution")
        
        return result
    
    def _handle_sales(self, task_id: str, content: str, 
                     entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle sales-related tasks"""
        result["actions_taken"].append("Analyzed sales task")
        
        if "amounts" in entities:
            result["actions_taken"].append(f"Identified deal values: {entities['amounts']}")
        
        if "companies" in entities:
            result["actions_taken"].append(f"Identified prospects/clients: {entities['companies']}")
        
        if "percentages" in entities:
            result["actions_taken"].append(f"Identified targets/commissions: {entities['percentages']}")
        
        # Try to call Business MCP Server for sales pipeline update
        try:
            mcp_response = self._call_business_mcp("update_sales_pipeline", {
                "activity_type": "sales_activity",
                "description": content,
                "deal_value": entities.get("amounts", [None])[0] if "amounts" in entities else None,
                "companies": entities.get("companies", [])
            })
            if mcp_response.get("success"):
                result["actions_taken"].append("Sales pipeline updated via Business MCP Server")
                result["mcp_response"] = mcp_response
        except Exception as e:
            result["recommendations"].append(f"Business MCP Server unavailable: {str(e)}")
        
        result["recommendations"].append("Update sales CRM")
        result["recommendations"].append("Schedule follow-up with prospect")
        
        return result
    
    def _handle_contract(self, task_id: str, content: str, 
                        entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle contract-related tasks"""
        result["actions_taken"].append("Analyzed contract task")
        
        if "companies" in entities:
            result["actions_taken"].append(f"Identified parties: {entities['companies']}")
        
        if "amounts" in entities:
            result["actions_taken"].append(f"Identified contract values: {entities['amounts']}")
        
        result["recommendations"].append("Review contract terms carefully")
        result["recommendations"].append("Consult legal if needed")
        result["recommendations"].append("Track contract deadlines")
        
        return result
    
    def _handle_operations(self, task_id: str, content: str, 
                          entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle operations-related tasks"""
        result["actions_taken"].append("Analyzed operations task")
        
        result["recommendations"].append("Document process changes")
        result["recommendations"].append("Communicate with affected teams")
        result["recommendations"].append("Monitor implementation")
        
        return result
    
    def _trigger_accounting_integration(self, task_id: str, content: str, 
                                        result: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger cross-domain integration with Accounting"""
        result["cross_domain_actions"] = result.get("cross_domain_actions", [])
        
        try:
            # Call Accounting MCP Server for financial-related actions
            mcp_response = self._call_accounting_mcp("flag_financial_task", {
                "task_id": task_id,
                "content": content,
                "source_domain": "Business"
            })
            if mcp_response.get("success"):
                result["cross_domain_actions"].append({
                    "domain": "Accounting",
                    "action": "Financial task flagged",
                    "response": mcp_response
                })
        except Exception as e:
            result["recommendations"].append(f"Accounting integration unavailable: {str(e)}")
        
        return result
    
    def _trigger_personal_integration(self, task_id: str, content: str, 
                                      result: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger cross-domain integration with Personal"""
        result["cross_domain_actions"] = result.get("cross_domain_actions", [])
        
        try:
            # Call Personal MCP Server for work-life balance related actions
            mcp_response = self._call_personal_mcp("flag_personal_impact", {
                "task_id": task_id,
                "content": content,
                "source_domain": "Business"
            })
            if mcp_response.get("success"):
                result["cross_domain_actions"].append({
                    "domain": "Personal",
                    "action": "Personal impact flagged",
                    "response": mcp_response
                })
        except Exception as e:
            result["recommendations"].append(f"Personal integration unavailable: {str(e)}")
        
        return result
    
    def _trigger_social_integration(self, task_id: str, content: str, 
                                    result: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger cross-domain integration with Social Media"""
        result["cross_domain_actions"] = result.get("cross_domain_actions", [])
        
        try:
            # Call Social MCP Server for marketing-related actions
            mcp_response = self._call_social_mcp("flag_marketing_task", {
                "task_id": task_id,
                "content": content,
                "source_domain": "Business"
            })
            if mcp_response.get("success"):
                result["cross_domain_actions"].append({
                    "domain": "Social Media",
                    "action": "Marketing task flagged",
                    "response": mcp_response
                })
        except Exception as e:
            result["recommendations"].append(f"Social Media integration unavailable: {str(e)}")
        
        return result
    
    def _call_business_mcp(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Business MCP Server for external actions"""
        url = f"{self.mcp_server_url}/api/{action}"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=params)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            raise Exception("Business MCP Server not available")
        except httpx.HTTPError as e:
            raise Exception(f"Business MCP Server error: {str(e)}")
    
    def _call_accounting_mcp(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Accounting MCP Server for cross-domain actions"""
        url = f"{self.accounting_mcp_url}/api/{action}"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=params)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            raise Exception("Accounting MCP Server not available")
        except httpx.HTTPError as e:
            raise Exception(f"Accounting MCP Server error: {str(e)}")
    
    def _call_personal_mcp(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Personal MCP Server for cross-domain actions"""
        url = f"{self.mcp_server_url}/api/{action}"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=params)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            raise Exception("Personal MCP Server not available")
        except httpx.HTTPError as e:
            raise Exception(f"Personal MCP Server error: {str(e)}")
    
    def _call_social_mcp(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Social MCP Server for cross-domain actions"""
        url = f"http://localhost:8002/api/{action}"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=params)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            raise Exception("Social MCP Server not available")
        except httpx.HTTPError as e:
            raise Exception(f"Social MCP Server error: {str(e)}")
    
    def _log_execution(self, task_id: str, content: str, result: Dict[str, Any]):
        """Log the execution to business_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
## Business Task Execution Log
- **Timestamp:** {timestamp}
- **Task ID:** {task_id}
- **Category:** {result.get('category', 'unknown')}
- **Status:** {result.get('status', 'unknown')}
- **Content Preview:** {content[:100]}...
- **Actions Taken:** {result.get('actions_taken', [])}
- **Cross-Domain Actions:** {result.get('cross_domain_actions', [])}
- **Recommendations:** {result.get('recommendations', [])}

---
"""
        
        try:
            with open("logs/business_log.md", "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
        except Exception:
            pass


# Convenience function for direct usage
def business_analyst_skill(input_data: Dict[str, Any]) -> str:
    """Direct function call interface"""
    skill = BusinessAnalystSkill()
    return skill(input_data)


# Example usage when run directly
if __name__ == "__main__":
    examples = [
        {
            "task_id": "business_001",
            "content": "Schedule client meeting with ABC Inc to discuss Q1 revenue targets of $500K",
            "sender": "sales_team",
            "metadata": {"priority": "high"}
        },
        {
            "task_id": "business_002",
            "content": "Prepare strategic plan for market expansion including budget allocation",
            "sender": "ceo",
            "metadata": {}
        },
        {
            "task_id": "business_003",
            "content": "Review contract proposal with XYZ Corp - $250K deal, needs legal approval",
            "sender": "legal_dept",
            "metadata": {"priority": "high"}
        }
    ]
    
    skill = BusinessAnalystSkill()
    
    for example in examples:
        print(f"\n{'='*60}")
        print(f"Processing: {example['content']}")
        print('='*60)
        result = skill(example)
        print(result)
