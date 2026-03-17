"""
Personal Assistant Skill

Handles personal domain tasks including:
- Personal appointments and reminders
- Family-related tasks
- Health and fitness tracking
- Personal finance (non-business)
- Travel planning
- Hobby management
- Personal communications

Integrates with Personal MCP Server for external actions.
"""
import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import httpx
import os

class PersonalAssistantSkill:
    """Skill for handling personal domain tasks"""
    
    def __init__(self):
        self.mcp_server_url = os.getenv("PERSONAL_MCP_URL", "http://localhost:8003")
        self.timeout = httpx.Timeout(30.0)
        
    def __call__(self, input_data: Dict[str, Any]) -> str:
        """
        Main entry point for the personal assistant skill.
        
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
        
        # Analyze the personal task type
        task_analysis = self._analyze_personal_task(content, metadata)
        
        # Execute appropriate action
        result = self._execute_personal_action(task_id, content, task_analysis, metadata)
        
        # Log the execution
        self._log_execution(task_id, content, result)
        
        return json.dumps(result, indent=2, default=str)
    
    def _analyze_personal_task(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze personal task to determine specific category and required actions.
        
        Categories:
        - appointment: Doctor, dentist, meetings, etc.
        - reminder: Personal reminders, anniversaries, birthdays
        - family: Family-related tasks
        - health_fitness: Exercise, diet, health tracking
        - travel: Trip planning, bookings, itineraries
        - finance: Personal budget, bills, non-business expenses
        - hobby: Personal projects, hobbies
        - communication: Personal emails, messages, calls
        """
        content_lower = content.lower()
        
        category_scores = {
            "appointment": 0,
            "reminder": 0,
            "family": 0,
            "health_fitness": 0,
            "travel": 0,
            "finance": 0,
            "hobby": 0,
            "communication": 0
        }
        
        # Appointment keywords
        appointment_keywords = ["appointment", "meeting", "schedule", "booking", "reservation", 
                               "doctor", "dentist", "clinic", "haircut", "gym session"]
        for keyword in appointment_keywords:
            if keyword in content_lower:
                category_scores["appointment"] += 2
        
        # Reminder keywords
        reminder_keywords = ["remember", "reminder", "don't forget", "anniversary", "birthday",
                            "celebration", "party", "event", "deadline"]
        for keyword in reminder_keywords:
            if keyword in content_lower:
                category_scores["reminder"] += 2
        
        # Family keywords
        family_keywords = ["family", "spouse", "wife", "husband", "child", "children", "kid",
                          "parent", "mother", "father", "sibling", "brother", "sister",
                          "relative", "cousin", "uncle", "aunt"]
        for keyword in family_keywords:
            if keyword in content_lower:
                category_scores["family"] += 2
        
        # Health & fitness keywords
        health_keywords = ["health", "fitness", "exercise", "workout", "gym", "run", "jog",
                          "diet", "nutrition", "weight", "yoga", "meditation", "sleep",
                          "vitamin", "medicine", "prescription"]
        for keyword in health_keywords:
            if keyword in content_lower:
                category_scores["health_fitness"] += 2
        
        # Travel keywords
        travel_keywords = ["travel", "trip", "vacation", "flight", "hotel", "booking",
                          "airport", "train", "bus", "rental car", "itinerary", "passport",
                          "visa", "luggage", "destination"]
        for keyword in travel_keywords:
            if keyword in content_lower:
                category_scores["travel"] += 2
        
        # Personal finance keywords
        finance_keywords = ["bill", "payment", "budget", "personal expense", "salary",
                           "savings", "investment", "loan", "mortgage", "rent", "utility",
                           "insurance", "tax return"]
        for keyword in finance_keywords:
            if keyword in content_lower:
                category_scores["finance"] += 2
        
        # Hobby keywords
        hobby_keywords = ["hobby", "project", "craft", "art", "music", "reading", "book",
                         "game", "sport", "collection", "gardening", "cooking", "baking"]
        for keyword in hobby_keywords:
            if keyword in content_lower:
                category_scores["hobby"] += 2
        
        # Communication keywords
        communication_keywords = ["call", "email", "message", "text", "contact", "reach out",
                                 "send", "reply", "respond", "write to"]
        for keyword in communication_keywords:
            if keyword in content_lower:
                category_scores["communication"] += 2
        
        # Determine primary category
        primary_category = max(category_scores, key=category_scores.get)
        confidence = category_scores[primary_category] / max(sum(category_scores.values()), 1)
        
        # Extract entities
        entities = self._extract_entities(content, primary_category)
        
        return {
            "primary_category": primary_category,
            "confidence": round(confidence, 2),
            "category_scores": category_scores,
            "entities": entities,
            "requires_external_action": self._requires_external_action(primary_category),
            "suggested_priority": self._suggest_priority(primary_category, metadata)
        }
    
    def _extract_entities(self, content: str, category: str) -> Dict[str, Any]:
        """Extract relevant entities based on category"""
        entities = {}
        
        # Extract dates/times
        date_patterns = [
            r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',  # MM/DD/YYYY or DD-MM-YYYY
            r'\b(\d{1,2}:\d{2}\s*[AP]?M?)\b',  # HH:MM AM/PM
            r'\b(today|tomorrow|yesterday|next week|this week)\b',
            r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
        ]
        
        dates_found = []
        for pattern in date_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dates_found.extend(matches)
        
        if dates_found:
            entities["dates"] = dates_found
        
        # Extract phone numbers
        phone_pattern = r'\b(\d{3}[-.]?\d{3}[-.]?\d{4})\b'
        phones = re.findall(phone_pattern, content)
        if phones:
            entities["phone_numbers"] = phones
        
        # Extract email addresses
        email_pattern = r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
        emails = re.findall(email_pattern, content)
        if emails:
            entities["emails"] = emails
        
        # Extract amounts (for finance category)
        if category == "finance":
            amount_pattern = r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
            amounts = re.findall(amount_pattern, content)
            if amounts:
                entities["amounts"] = amounts
        
        # Extract locations
        location_keywords = ["at ", "in ", "near ", "location: ", "place: "]
        for keyword in location_keywords:
            if keyword in content_lower := content.lower():
                # Simple extraction - text after keyword until next punctuation
                idx = content_lower.find(keyword)
                if idx >= 0:
                    start = idx + len(keyword)
                    end = min(content.find(".", start), content.find(",", start), len(content))
                    if end > start:
                        location = content[start:end].strip()
                        if "locations" not in entities:
                            entities["locations"] = []
                        entities["locations"].append(location)
        
        return entities
    
    def _requires_external_action(self, category: str) -> bool:
        """Determine if category requires external MCP server action"""
        external_categories = ["appointment", "communication", "finance", "travel"]
        return category in external_categories
    
    def _suggest_priority(self, category: str, metadata: Dict[str, Any]) -> str:
        """Suggest priority based on category and metadata"""
        # Check explicit priority in metadata
        if "priority" in metadata:
            return metadata["priority"]
        
        # Default priorities by category
        priority_mapping = {
            "appointment": "high",
            "health_fitness": "medium",
            "finance": "high",
            "communication": "medium",
            "family": "high",
            "reminder": "medium",
            "travel": "medium",
            "hobby": "low"
        }
        
        return priority_mapping.get(category, "medium")
    
    def _execute_personal_action(self, task_id: str, content: str, 
                                  task_analysis: Dict[str, Any], 
                                  metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the appropriate personal action"""
        category = task_analysis["primary_category"]
        entities = task_analysis["entities"]
        
        result = {
            "task_id": task_id,
            "category": category,
            "status": "pending",
            "actions_taken": [],
            "recommendations": [],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Category-specific handling
            if category == "appointment":
                result = self._handle_appointment(task_id, content, entities, result)
            elif category == "reminder":
                result = self._handle_reminder(task_id, content, entities, result)
            elif category == "family":
                result = self._handle_family(task_id, content, entities, result)
            elif category == "health_fitness":
                result = self._handle_health_fitness(task_id, content, entities, result)
            elif category == "travel":
                result = self._handle_travel(task_id, content, entities, result)
            elif category == "finance":
                result = self._handle_personal_finance(task_id, content, entities, result)
            elif category == "hobby":
                result = self._handle_hobby(task_id, content, entities, result)
            elif category == "communication":
                result = self._handle_communication(task_id, content, entities, result)
            else:
                result["status"] = "categorized"
                result["actions_taken"].append(f"Task categorized as {category}")
                result["recommendations"].append("No specific action required")
            
            result["status"] = "completed"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def _handle_appointment(self, task_id: str, content: str, 
                           entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle appointment-related tasks"""
        result["actions_taken"].append("Analyzed appointment request")
        
        if "dates" in entities:
            result["actions_taken"].append(f"Extracted date/time: {entities['dates']}")
            result["recommendations"].append("Consider adding to calendar")
        
        if "locations" in entities:
            result["actions_taken"].append(f"Extracted location: {entities['locations']}")
            result["recommendations"].append("Consider mapping the location")
        
        # Try to call Personal MCP Server for calendar integration
        try:
            mcp_response = self._call_personal_mcp("create_appointment", {
                "title": content[:50],
                "description": content,
                "dates": entities.get("dates", []),
                "location": entities.get("locations", [None])[0] if "locations" in entities else None
            })
            if mcp_response.get("success"):
                result["actions_taken"].append("Appointment created in Personal MCP Server")
                result["mcp_response"] = mcp_response
        except Exception as e:
            result["recommendations"].append(f"MCP Server unavailable: {str(e)}")
        
        return result
    
    def _handle_reminder(self, task_id: str, content: str, 
                        entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle reminder-related tasks"""
        result["actions_taken"].append("Analyzed reminder request")
        
        if "dates" in entities:
            result["actions_taken"].append(f"Extracted reminder date: {entities['dates']}")
        
        # Try to call Personal MCP Server for reminder creation
        try:
            mcp_response = self._call_personal_mcp("create_reminder", {
                "title": content[:50],
                "description": content,
                "reminder_date": entities.get("dates", [None])[0] if "dates" in entities else None
            })
            if mcp_response.get("success"):
                result["actions_taken"].append("Reminder created in Personal MCP Server")
                result["mcp_response"] = mcp_response
        except Exception as e:
            result["recommendations"].append(f"MCP Server unavailable: {str(e)}")
        
        return result
    
    def _handle_family(self, task_id: str, content: str, 
                      entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle family-related tasks"""
        result["actions_taken"].append("Analyzed family task")
        result["recommendations"].append("Consider adding to family calendar")
        result["recommendations"].append("May require coordination with family members")
        
        return result
    
    def _handle_health_fitness(self, task_id: str, content: str, 
                               entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle health and fitness tasks"""
        result["actions_taken"].append("Analyzed health/fitness task")
        
        # Check for medication/health tracking
        health_keywords = ["medicine", "medication", "vitamin", "supplement"]
        for keyword in health_keywords:
            if keyword in content.lower():
                result["recommendations"].append("Consider setting up recurring health reminder")
        
        return result
    
    def _handle_travel(self, task_id: str, content: str, 
                      entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle travel-related tasks"""
        result["actions_taken"].append("Analyzed travel request")
        
        if "dates" in entities:
            result["actions_taken"].append(f"Extracted travel dates: {entities['dates']}")
        
        result["recommendations"].append("Consider creating travel itinerary")
        result["recommendations"].append("Check passport/visa requirements if international")
        
        # Try to call Personal MCP Server for travel planning
        try:
            mcp_response = self._call_personal_mcp("create_travel_plan", {
                "description": content,
                "dates": entities.get("dates", []),
                "destinations": entities.get("locations", [])
            })
            if mcp_response.get("success"):
                result["actions_taken"].append("Travel plan initiated in Personal MCP Server")
                result["mcp_response"] = mcp_response
        except Exception as e:
            result["recommendations"].append(f"MCP Server unavailable: {str(e)}")
        
        return result
    
    def _handle_personal_finance(self, task_id: str, content: str, 
                                 entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle personal finance tasks"""
        result["actions_taken"].append("Analyzed personal finance task")
        
        if "amounts" in entities:
            result["actions_taken"].append(f"Extracted amounts: {entities['amounts']}")
        
        # Check if this might be a business expense (cross-domain)
        business_indicators = ["business", "work", "client", "company", "office"]
        is_potentially_business = any(indicator in content.lower() for indicator in business_indicators)
        
        if is_potentially_business:
            result["cross_domain_flag"] = True
            result["recommendations"].append("⚠️ This may be a business expense - consider routing to Business domain")
            result["recommendations"].append("Cross-domain integration: Personal↔Business expense classification")
        
        # Try to call Personal MCP Server for expense tracking
        try:
            mcp_response = self._call_personal_mcp("track_personal_expense", {
                "description": content,
                "amount": entities.get("amounts", [None])[0] if "amounts" in entities else None,
                "date": entities.get("dates", [None])[0] if "dates" in entities else None
            })
            if mcp_response.get("success"):
                result["actions_taken"].append("Expense tracked in Personal MCP Server")
                result["mcp_response"] = mcp_response
        except Exception as e:
            result["recommendations"].append(f"MCP Server unavailable: {str(e)}")
        
        return result
    
    def _handle_hobby(self, task_id: str, content: str, 
                     entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle hobby-related tasks"""
        result["actions_taken"].append("Analyzed hobby task")
        result["recommendations"].append("Consider scheduling dedicated time for this activity")
        
        return result
    
    def _handle_communication(self, task_id: str, content: str, 
                             entities: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Handle communication tasks"""
        result["actions_taken"].append("Analyzed communication request")
        
        if "emails" in entities:
            result["actions_taken"].append(f"Extracted email addresses: {entities['emails']}")
        
        if "phone_numbers" in entities:
            result["actions_taken"].append(f"Extracted phone numbers: {entities['phone_numbers']}")
        
        # Try to call Personal MCP Server for communication
        try:
            mcp_response = self._call_personal_mcp("send_personal_message", {
                "content": content,
                "recipients": entities.get("emails", []) + entities.get("phone_numbers", []),
                "method": "email" if entities.get("emails") else "sms"
            })
            if mcp_response.get("success"):
                result["actions_taken"].append("Communication sent via Personal MCP Server")
                result["mcp_response"] = mcp_response
        except Exception as e:
            result["recommendations"].append(f"MCP Server unavailable: {str(e)}")
        
        return result
    
    def _call_personal_mcp(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call Personal MCP Server for external actions"""
        url = f"{self.mcp_server_url}/api/{action}"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=params)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            raise Exception("Personal MCP Server not available")
        except httpx.HTTPError as e:
            raise Exception(f"MCP Server error: {str(e)}")
    
    def _log_execution(self, task_id: str, content: str, result: Dict[str, Any]):
        """Log the execution to personal_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
## Personal Task Execution Log
- **Timestamp:** {timestamp}
- **Task ID:** {task_id}
- **Category:** {result.get('category', 'unknown')}
- **Status:** {result.get('status', 'unknown')}
- **Content Preview:** {content[:100]}...
- **Actions Taken:** {result.get('actions_taken', [])}
- **Recommendations:** {result.get('recommendations', [])}

---
"""
        
        try:
            with open("logs/personal_log.md", "a", encoding="utf-8") as log_file:
                log_file.write(log_entry)
        except Exception:
            pass  # Logging failure should not break execution


# Convenience function for direct usage
def personal_assistant_skill(input_data: Dict[str, Any]) -> str:
    """Direct function call interface"""
    skill = PersonalAssistantSkill()
    return skill(input_data)


# Example usage when run directly
if __name__ == "__main__":
    # Example inputs for different categories
    examples = [
        {
            "task_id": "personal_001",
            "content": "Schedule dentist appointment for next Tuesday at 3 PM",
            "sender": "user",
            "metadata": {"priority": "high"}
        },
        {
            "task_id": "personal_002",
            "content": "Remember to buy birthday gift for mom - budget $50",
            "sender": "user",
            "metadata": {}
        },
        {
            "task_id": "personal_003",
            "content": "Plan family vacation to Hawaii in July, need flight and hotel bookings",
            "sender": "spouse",
            "metadata": {"priority": "medium"}
        }
    ]
    
    skill = PersonalAssistantSkill()
    
    for example in examples:
        print(f"\n{'='*60}")
        print(f"Processing: {example['content']}")
        print('='*60)
        result = skill(example)
        print(result)
