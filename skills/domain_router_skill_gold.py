"""
Domain Router Skill with Gold Tier Logging

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
import hashlib
import aiofiles
import os
from pathlib import Path


async def enhanced_log_entry(
    log_type: str,
    task_id: str,
    domain: str,
    skill_used: str,
    action_taken: str,
    result: str,
    error: str = None,
    details: dict = None
):
    """Enhanced logging function with Gold Tier standards"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    correlation_id = hashlib.md5(f"{timestamp}_{task_id}".encode()).hexdigest()[:12]

    log_entry = f"""
## {log_type} - {timestamp}
- **Task ID:** {task_id}
- **Domain:** {domain}
- **Skill:** {skill_used}
- **Action:** {action_taken}
- **Result:** {result}
- **Timestamp:** {timestamp}
- **Correlation ID:** {correlation_id}

### Details
"""

    if details:
        for key, value in details.items():
            log_entry += f"- **{key.title()}:** {json.dumps(value, default=str)[:500]}\n"

    if error:
        log_entry += f"""
### Errors
- **Error:** {error}
"""

    log_entry += "\n---\n"

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Write to appropriate log file based on log_type
    log_filename = f"logs/{log_type.lower().replace('_log', '')}.md"
    async with aiofiles.open(log_filename, "a", encoding="utf-8") as log_file:
        await log_file.write(log_entry)


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
    task_id = input_data.get("task_id", "unknown")
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
    skill_mapping = {
        "Personal": "personal_assistant_skill",
        "Business": "business_analyst_skill",
        "Accounting": "accounting_assistant_skill",
        "Social Media": "social_media_manager_skill"
    }

    recommended_next_skill = skill_mapping.get(max_domain, "general_assistant_skill")

    # Prepare result
    result_obj = {
        "task_id": task_id,
        "domain": max_domain,
        "confidence_score": confidence_score,
        "recommended_next_skill": recommended_next_skill
    }

    # Log the decision with Gold Tier standards
    import asyncio
    # Since this function is synchronous, we'll log synchronously as well
    # In a real async implementation, we'd await the logging

    log_details = {
        "input_content_length": len(content),
        "keyword_matches": dict(scores),
        "confidence_score": confidence_score,
        "recommended_skill": recommended_next_skill
    }

    # Synchronous logging for compatibility with sync function
    import threading
    def async_log():
        async def log_async():
            await enhanced_log_entry(
                log_type="DECISION_LOG",
                task_id=task_id,
                domain=max_domain,
                skill_used="domain_router_skill",
                action_taken="Domain classification performed",
                result="success",
                details=log_details
            )

        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(log_async())
        finally:
            loop.close()

    # Run logging in a separate thread to maintain sync compatibility
    log_thread = threading.Thread(target=async_log)
    log_thread.start()
    log_thread.join()  # Wait for logging to complete

    return json.dumps(result_obj, indent=2)


def log_decision(result: Dict[str, Any], content: str, sender: str, metadata: Dict[str, Any]):
    """Legacy log function - maintained for compatibility"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"""
## Decision Log Entry
- **Timestamp:** {timestamp}
- **Task ID:** {result['task_id']}
- **Domain:** {result['domain']}
- **Confidence Score:** {result['confidence_score']}
- **Recommended Next Skill:** {result['recommended_next_skill']}
- **Content Preview:** {content[:100]}...
- **Sender:** {sender}
- **Metadata Keys:** {list(metadata.keys()) if metadata else []}

---
"""

    # Append to decision log
    with open("decision_log.md", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)


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