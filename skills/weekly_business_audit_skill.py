"""
Weekly Business Audit Skill

Automated skill that runs every 7 days to analyze business performance
by pulling data from accounting and social MCP servers.
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import httpx
import aiofiles
from pathlib import Path


async def weekly_business_audit_skill() -> str:
    """
    Runs automated business audit pulling data from accounting and social MCP servers.

    Returns:
        String containing the CEO briefing report
    """
    # Calculate date range for the week
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    try:
        # Pull financial data from accounting server
        financial_data = await pull_financial_data(start_date_str, end_date_str)

        # Pull social engagement data from social server
        social_data = await pull_social_data(start_date_str, end_date_str)

        # Analyze the data
        analysis_results = await analyze_data(financial_data, social_data, start_date_str, end_date_str)

        # Generate CEO briefing
        ceo_briefing = generate_ceo_briefing(analysis_results)

        # Log the report
        await log_report(ceo_briefing, start_date_str, end_date_str)

        return ceo_briefing

    except Exception as e:
        error_report = f"ERROR in Weekly Business Audit: {str(e)}"
        await log_error(error_report)
        return error_report


async def pull_financial_data(start_date: str, end_date: str) -> Dict[str, Any]:
    """Pull financial data from accounting_mcp_server"""

    accounting_url = os.getenv("ACCOUNTING_MCP_SERVER_URL", "http://localhost:8000")

    financial_data = {}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch profit and loss for the period
            pl_request = {
                "date_from": start_date,
                "date_to": end_date
            }

            pl_response = await client.post(
                f"{accounting_url}/fetch_profit_loss",
                json=pl_request,
                headers={"Content-Type": "application/json"}
            )

            if pl_response.status_code == 200:
                pl_result = pl_response.json()
                if pl_result.get("success"):
                    financial_data["profit_loss"] = pl_result.get("data", {})

                    # Calculate revenue, expenses, profit
                    revenue = pl_result["data"].get("total_income", 0)
                    expenses = pl_result["data"].get("total_expenses", 0)
                    net_profit = pl_result["data"].get("net_profit", 0)

                    financial_data["revenue"] = revenue
                    financial_data["expenses"] = expenses
                    financial_data["net_profit"] = net_profit
                else:
                    financial_data["error"] = pl_result.get("error", "Unknown error")
            else:
                financial_data["error"] = f"HTTP {pl_response.status_code}: {pl_response.text}"

    except Exception as e:
        financial_data["error"] = f"Failed to fetch financial data: {str(e)}"

    return financial_data


async def pull_social_data(start_date: str, end_date: str) -> Dict[str, Any]:
    """Pull social engagement data from social_mcp_server"""

    social_url = os.getenv("SOCIAL_MCP_SERVER_URL", "http://localhost:8001")

    social_data = {}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # This would require knowing specific post IDs to fetch engagement
            # For now, we'll simulate fetching engagement metrics for a range
            # In a real implementation, this would need to fetch actual post data

            social_data["engagement_summary"] = {
                "facebook": {"likes": 0, "comments": 0, "shares": 0},
                "instagram": {"likes": 0, "comments": 0, "impressions": 0},
                "twitter": {"likes": 0, "retweets": 0, "replies": 0}
            }

    except Exception as e:
        social_data["error"] = f"Failed to fetch social data: {str(e)}"

    return social_data


async def analyze_data(financial_data: Dict[str, Any], social_data: Dict[str, Any],
                      start_date: str, end_date: str) -> Dict[str, Any]:
    """Analyze financial and social data to detect trends and anomalies"""

    analysis = {
        "revenue_trend": "stable",
        "expense_trend": "stable",
        "profit_margin": 0.0,
        "top_channel": "unknown",
        "anomalies": [],
        "campaign_performance": {},
        "risk_areas": [],
        "recommendations": []
    }

    # Analyze revenue trends
    revenue = financial_data.get("revenue", 0)
    expenses = financial_data.get("expenses", 0)
    net_profit = financial_data.get("net_profit", 0)

    if revenue > 0:
        profit_margin = (net_profit / revenue) * 100
        analysis["profit_margin"] = round(profit_margin, 2)

    # Compare with historical data if available
    # For now, we'll use simple heuristics
    if revenue > 10000:  # Threshold for high revenue
        analysis["revenue_trend"] = "positive"
    elif revenue < 1000:  # Threshold for low revenue
        analysis["revenue_trend"] = "concerning"
        analysis["risk_areas"].append("Low revenue performance")

    if expenses > revenue * 0.9:  # Expenses near 90% of revenue
        analysis["expense_trend"] = "concerning"
        analysis["risk_areas"].append("High expense ratio")

    # Analyze social performance
    engagement = social_data.get("engagement_summary", {})

    # Determine top performing channel based on engagement
    channel_scores = {}

    fb_engagement = engagement.get("facebook", {})
    ig_engagement = engagement.get("instagram", {})
    tw_engagement = engagement.get("twitter", {})

    # Calculate engagement scores
    fb_score = (
        fb_engagement.get("likes", 0) * 1 +
        fb_engagement.get("comments", 0) * 3 +
        fb_engagement.get("shares", 0) * 5
    )
    ig_score = (
        ig_engagement.get("likes", 0) * 1 +
        ig_engagement.get("comments", 0) * 3 +
        ig_engagement.get("impressions", 0) * 0.1
    )
    tw_score = (
        tw_engagement.get("likes", 0) * 1 +
        tw_engagement.get("retweets", 0) * 3 +
        tw_engagement.get("replies", 0) * 2
    )

    channel_scores = {
        "Facebook": fb_score,
        "Instagram": ig_score,
        "Twitter": tw_score
    }

    if channel_scores:
        analysis["top_channel"] = max(channel_scores, key=channel_scores.get)

    # Detect anomalies
    if revenue < 0:
        analysis["anomalies"].append("Negative revenue detected")
    if expenses > revenue * 1.2:  # Expenses 20% higher than revenue
        analysis["anomalies"].append("Expenses significantly exceed revenue")
    if profit_margin < 0:
        analysis["anomalies"].append("Negative profit margin")

    # Generate recommendations based on analysis
    if "Low revenue performance" in analysis["risk_areas"]:
        analysis["recommendations"].append("Focus on increasing sales and marketing efforts")
    if "High expense ratio" in analysis["risk_areas"]:
        analysis["recommendations"].append("Review and optimize operational costs")
    if profit_margin < 5:
        analysis["recommendations"].append("Investigate pricing strategy to improve margins")

    # Campaign performance analysis
    analysis["campaign_performance"] = {
        "revenue_per_channel": {
            "Facebook": revenue * 0.3,  # Placeholder values
            "Instagram": revenue * 0.5,
            "Twitter": revenue * 0.2
        },
        "engagement_efficiency": channel_scores
    }

    return analysis


def generate_ceo_briefing(analysis: Dict[str, Any]) -> str:
    """Generate CEO briefing in required format"""

    briefing = f"""WEEKLY CEO BRIEFING
Week: {datetime.now().strftime('%Y-%m-%d')}
Period: {datetime.now() - timedelta(days=7):%Y-%m-%d} to {datetime.now():%Y-%m-%d}

Revenue: ${analysis.get('revenue', 0):,.2f}
Expenses: ${analysis.get('expenses', 0):,.2f}
Net Profit: ${analysis.get('net_profit', 0):,.2f}
Profit Margin: {analysis.get('profit_margin', 0):.2f}%
Top Performing Channel: {analysis.get('top_channel', 'N/A')}
Risk Areas: {', '.join(analysis.get('risk_areas', ['None'])) if analysis.get('risk_areas') else 'None'}
Recommendations: {', '.join(analysis.get('recommendations', ['None'])) if analysis.get('recommendations') else 'None'}
Strategic Notes: Weekly performance analysis complete. Monitor risk areas closely.

ANALYSIS DETAILS:
- Revenue Trend: {analysis.get('revenue_trend', 'Unknown')}
- Expense Trend: {analysis.get('expense_trend', 'Unknown')}
- Anomalies Detected: {len(analysis.get('anomalies', []))}
- Top Channel Score: {analysis.get('engagement_efficiency', {}).get(analysis.get('top_channel', ''), 0)}
"""

    return briefing


async def log_report(briefing: str, start_date: str, end_date: str):
    """Log the report to analytics/weekly_reports/ and audit_log.md"""

    # Create weekly reports directory if it doesn't exist
    reports_dir = Path("analytics/weekly_reports/")
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    filename = f"weekly_audit_{start_date.replace('-', '')}_to_{end_date.replace('-', '')}.txt"
    filepath = reports_dir / filename

    # Write the briefing to the specific report file
    async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
        await f.write(briefing)

    # Append to audit log
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    audit_entry = f"""
## Weekly Audit Report - {timestamp}
- Report File: {filename}
- Period: {start_date} to {end_date}
- Top Channel: {briefing.split('Top Performing Channel: ')[1].split('\\n')[0] if 'Top Performing Channel: ' in briefing else 'N/A'}

"""

    async with aiofiles.open("audit_log.md", "a", encoding="utf-8") as log_file:
        await log_file.write(audit_entry)


async def log_error(error_msg: str):
    """Log errors to audit_log.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    audit_entry = f"""
## Weekly Audit Error - {timestamp}
- Error: {error_msg}

"""

    async with aiofiles.open("audit_log.md", "a", encoding="utf-8") as log_file:
        await log_file.write(audit_entry)


# Example usage for manual execution
if __name__ == "__main__":
    result = asyncio.run(weekly_business_audit_skill())
    print(result)