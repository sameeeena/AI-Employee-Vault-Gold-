"""
Domain Router Skill

Classifies tasks into one of the following domains:
- Personal
- Business
- Accounting
- Social Media

Based on: metadata, keywords, sender, content context
"""
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional

def domain_router_skill(input_data: Dict[str, Any]) -> str:
    """
    Classifies a task into one of four domains based on content analysis.

    Args:
        input_data: Dictionary containing:
            - task_id: Unique identifier for the task
            - content: The content to classify
            - metadata: Additional metadata (optional)
            - sender: Information about sender (optional)

    Returns:
        JSON string with classification results
    """
    # Extract input parameters
    task_id = input_data.get("task_id", "")
    content = input_data.get("content", "").lower()
    metadata = input_data.get("metadata", {})
    sender = input_data.get("sender", "")

    # Define domain keywords
    domain_keywords = {
        "Personal": [
            "personal", "family", "home", "private", "myself", "vacation",
            "travel", "health", "fitness", "hobby", "friend", "relationship",
            "birthday", "anniversary", "appointment", "doctor", "dentist"
        ],
        "Business": [
            "business", "company", "work", "meeting", "project", "client",
            "customer", "sales", "marketing", "strategy", "revenue", "profit",
            "team", "employee", "boss", "office", "presentation", "proposal",
            "contract", "negotiation", "partnership", "corporate"
        ],
        "Accounting": [
            "accounting", "finance", "tax", "invoice", "payment", "expense",
            "revenue", "budget", "cost", "financial", "statement", "audit",
            "balance", "ledger", "bookkeeping", "payroll", "receipt",
            "transaction", "income", "debt", "loan", "investment", "stock",
            "bond", "asset", "liability", "equity", "cashflow"
        ],
        "Social Media": [
            "social media", "facebook", "twitter", "instagram", "linkedin",
            "tiktok", "youtube", "post", "tweet", "share", "like", "follow",
            "comment", "hashtag", "influencer", "engagement", "reach",
            "audience", "content creator", "story", "live", "stream",
            "follower", "profile", "bio", "post", "upload", "publish"
        ]
    }

    # Initialize scores
    scores = {domain: 0 for domain in domain_keywords.keys()}

    # Score based on content keywords
    for domain, keywords in domain_keywords.items():
        for keyword in keywords:
            # Count occurrences of each keyword
            matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content))
            scores[domain] += matches

    # Score based on sender if provided
    sender_lower = sender.lower()
    for domain, keywords in domain_keywords.items():
        for keyword in keywords:
            if keyword in sender_lower:
                scores[domain] += 1

    # Score based on metadata if provided
    metadata_str = json.dumps(metadata).lower() if metadata else ""
    for domain, keywords in domain_keywords.items():
        for keyword in keywords:
            if keyword in metadata_str:
                scores[domain] += 1

    # Determine the highest scoring domain
    max_domain = max(scores, key=scores.get)
    max_score = scores[max_domain]

    # Calculate confidence score (normalize based on total keywords found)
    total_score = sum(scores.values())
    confidence_score = round(max_score / max(total_score, 1), 2) if total_score > 0 else 0.0

    # Determine recommended next skill based on domain
    # Updated with cross-domain integration support
    skill_mapping = {
        "Personal": "personal_assistant_skill",
        "Business": "business_analyst_skill",
        "Accounting": "accounting_mcp_server",
        "Social Media": "social_mcp_server"
    }

    # MCP Server endpoints for each domain
    mcp_endpoints = {
        "Personal": "http://localhost:8003",
        "Business": "http://localhost:8004",
        "Accounting": "http://localhost:8001",
        "Social Media": "http://localhost:8002"
    }

    recommended_next_skill = skill_mapping.get(max_domain, "general_assistant_skill")
    mcp_endpoint = mcp_endpoints.get(max_domain, None)

    # Prepare result
    result = {
        "task_id": task_id,
        "domain": max_domain,
        "confidence_score": confidence_score,
        "recommended_next_skill": recommended_next_skill,
        "mcp_endpoint": mcp_endpoint,
        "cross_domain_enabled": True,
        "integration_notes": get_integration_notes(max_domain)
    }

    # Log the decision
    log_decision(result, content, sender, metadata)

    return json.dumps(result, indent=2)


def log_decision(result: Dict[str, Any], content: str, sender: str, metadata: Dict[str, Any]):
    """Log the classification decision to decision_log.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"""
## Decision Log Entry
- **Timestamp:** {timestamp}
- **Task ID:** {result['task_id']}
- **Domain:** {result['domain']}
- **Confidence Score:** {result['confidence_score']}
- **Recommended Next Skill:** {result['recommended_next_skill']}
- **MCP Endpoint:** {result.get('mcp_endpoint', 'N/A')}
- **Cross-Domain Enabled:** {result.get('cross_domain_enabled', False)}
- **Integration Notes:** {result.get('integration_notes', 'None')}
- **Content Preview:** {content[:100]}...
- **Sender:** {sender}
- **Metadata Keys:** {list(metadata.keys()) if metadata else []}

---
"""

    # Append to decision log
    with open("decision_log.md", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)


def get_integration_notes(domain: str) -> str:
    """
    Get integration notes for a domain.
    Describes cross-domain integration capabilities.
    """
    integration_notes = {
        "Personal": """
- **Cross-Domain Integration:** Enabled
- **Can Receive From:** Business (work-life balance flags)
- **Can Trigger:** Accounting (personal expense tracking)
- **MCP Server:** Personal MCP Server (port 8003)
- **Key Features:** Appointments, reminders, travel planning, personal finance
""",
        "Business": """
- **Cross-Domain Integration:** Enabled (Full)
- **Can Trigger:** Accounting, Personal, Social Media
- **Key Integrations:**
  - → Accounting: Financial task flagging
  - → Personal: Work-life balance monitoring
  - → Social Media: Marketing task coordination
- **MCP Server:** Business MCP Server (port 8004)
- **Key Features:** Meetings, CRM, sales pipeline, contracts
""",
        "Accounting": """
- **Cross-Domain Integration:** Receive-only
- **Can Receive From:** Personal, Business
- **Key Integrations:**
  - From Business: Financial task flags
  - From Personal: Expense categorization review
- **MCP Server:** Accounting MCP Server (port 8001)
- **Key Features:** Invoicing, expenses, financial reports (Odoo integration)
""",
        "Social Media": """
- **Cross-Domain Integration:** Receive-only
- **Can Receive From:** Business
- **Key Integrations:**
  - From Business: Marketing task flags
- **MCP Server:** Social MCP Server (port 8002)
- **Key Features:** Facebook, Instagram, Twitter posting and analytics
"""
    }
    
    return integration_notes.get(domain, "No integration notes available")


# Example usage when run directly
if __name__ == "__main__":
    # Example input
    example_input = {
        "task_id": "task_123",
        "content": "Please prepare the quarterly financial statements and tax documents for the company.",
        "sender": "Finance Department",
        "metadata": {
            "priority": "high",
            "department": "accounting"
        }
    }

    result = domain_router_skill(example_input)
    print(result)