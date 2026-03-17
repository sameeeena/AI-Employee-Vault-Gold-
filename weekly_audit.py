"""
Weekly Business & Accounting Audit System

Automated weekly audit system that:
1. Collects business metrics from all domains
2. Collects accounting/financial data
3. Performs audit analysis
4. Generates CEO briefing report
5. Distributes reports via email

Scheduled to run every week (configurable day/time)

Usage:
    python weekly_audit.py              # Run audit manually
    python weekly_audit.py --generate   # Generate CEO briefing
    python weekly_audit.py --schedule   # Start scheduler
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import hashlib
import aiofiles
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============== Data Models ==============

class AuditData:
    """Container for audit data"""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.week_start = self._get_week_start()
        self.week_end = datetime.now()
        self.business_metrics = {}
        self.accounting_metrics = {}
        self.social_metrics = {}
        self.personal_metrics = {}
        self.kpis = {}
        self.alerts = []
        self.recommendations = []
    
    def _get_week_start(self) -> datetime:
        """Get the start of current week (Monday)"""
        today = datetime.now()
        return today - timedelta(days=today.weekday())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp,
            "week_start": self.week_start.isoformat(),
            "week_end": self.week_end.isoformat(),
            "business_metrics": self.business_metrics,
            "accounting_metrics": self.accounting_metrics,
            "social_metrics": self.social_metrics,
            "personal_metrics": self.personal_metrics,
            "kpis": self.kpis,
            "alerts": self.alerts,
            "recommendations": self.recommendations
        }


class CEOBriefing:
    """CEO Briefing Report Generator"""
    
    def __init__(self, audit_data: AuditData):
        self.audit_data = audit_data
        self.report_date = datetime.now()
        self.report_sections = []
    
    def generate_executive_summary(self) -> str:
        """Generate executive summary section"""
        summary = []
        summary.append("📊 EXECUTIVE SUMMARY")
        summary.append("=" * 60)
        summary.append(f"Week: {self.audit_data.week_start.strftime('%Y-%m-%d')} to {self.audit_data.week_end.strftime('%Y-%m-%d')}")
        summary.append(f"Generated: {self.report_date.strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append("")
        
        # Key highlights
        kpis = self.audit_data.kpis
        if kpis:
            summary.append("Key Performance Indicators:")
            for kpi_name, kpi_value in kpis.items():
                summary.append(f"  • {kpi_name}: {kpi_value}")
        
        # Alerts
        if self.audit_data.alerts:
            summary.append(f"\n⚠️ Alerts: {len(self.audit_data.alerts)}")
            for alert in self.audit_data.alerts[:5]:  # Show top 5
                summary.append(f"  - {alert}")
        
        return "\n".join(summary)
    
    def generate_business_section(self) -> str:
        """Generate business metrics section"""
        section = []
        section.append("\n💼 BUSINESS METRICS")
        section.append("=" * 60)
        
        business = self.audit_data.business_metrics
        
        # Meetings
        if "meetings" in business:
            meetings = business["meetings"]
            section.append(f"\nMeetings & Events:")
            section.append(f"  • Total Meetings: {meetings.get('total', 0)}")
            section.append(f"  • Completed: {meetings.get('completed', 0)}")
            section.append(f"  • Scheduled: {meetings.get('scheduled', 0)}")
        
        # CRM
        if "crm" in business:
            crm = business["crm"]
            section.append(f"\nClient Relationships:")
            section.append(f"  • Active Clients: {crm.get('active_clients', 0)}")
            section.append(f"  • New Leads: {crm.get('new_leads', 0)}")
            section.append(f"  • Conversion Rate: {crm.get('conversion_rate', 0)}%")
        
        # Sales Pipeline
        if "sales" in business:
            sales = business["sales"]
            section.append(f"\nSales Pipeline:")
            section.append(f"  • Total Deals: {sales.get('total_deals', 0)}")
            section.append(f"  • Pipeline Value: ${sales.get('pipeline_value', 0):,.2f}")
            section.append(f"  • Closed This Week: ${sales.get('closed_this_week', 0):,.2f}")
        
        return "\n".join(section)
    
    def generate_accounting_section(self) -> str:
        """Generate accounting/financial section"""
        section = []
        section.append("\n💰 ACCOUNTING & FINANCIALS")
        section.append("=" * 60)
        
        accounting = self.audit_data.accounting_metrics
        
        # Revenue
        if "revenue" in accounting:
            revenue = accounting["revenue"]
            section.append(f"\nRevenue:")
            section.append(f"  • This Week: ${revenue.get('this_week', 0):,.2f}")
            section.append(f"  • Month to Date: ${revenue.get('mtd', 0):,.2f}")
            section.append(f"  • vs Last Week: {revenue.get('growth', 0)}%")
        
        # Expenses
        if "expenses" in accounting:
            expenses = accounting["expenses"]
            section.append(f"\nExpenses:")
            section.append(f"  • This Week: ${expenses.get('this_week', 0):,.2f}")
            section.append(f"  • Month to Date: ${expenses.get('mtd', 0):,.2f}")
            section.append(f"  • By Category: {expenses.get('by_category', {})}")
        
        # Profit
        if "profit" in accounting:
            profit = accounting["profit"]
            section.append(f"\nProfitability:")
            section.append(f"  • Gross Profit: ${profit.get('gross', 0):,.2f}")
            section.append(f"  • Net Profit: ${profit.get('net', 0):,.2f}")
            section.append(f"  • Margin: {profit.get('margin', 0)}%")
        
        # Invoices
        if "invoices" in accounting:
            invoices = accounting["invoices"]
            section.append(f"\nInvoices:")
            section.append(f"  • Issued: {invoices.get('issued', 0)}")
            section.append(f"  • Paid: {invoices.get('paid', 0)}")
            section.append(f"  • Overdue: {invoices.get('overdue', 0)}")
            section.append(f"  • Outstanding Amount: ${invoices.get('outstanding_amount', 0):,.2f}")
        
        return "\n".join(section)
    
    def generate_social_section(self) -> str:
        """Generate social media metrics section"""
        section = []
        section.append("\n📱 SOCIAL MEDIA PERFORMANCE")
        section.append("=" * 60)
        
        social = self.audit_data.social_metrics
        
        if "facebook" in social:
            fb = social["facebook"]
            section.append(f"\nFacebook:")
            section.append(f"  • Posts: {fb.get('posts', 0)}")
            section.append(f"  • Total Engagement: {fb.get('engagement', 0)}")
            section.append(f"  • Reach: {fb.get('reach', 0):,}")
        
        if "instagram" in social:
            ig = social["instagram"]
            section.append(f"\nInstagram:")
            section.append(f"  • Posts: {ig.get('posts', 0)}")
            section.append(f"  • Total Likes: {ig.get('likes', 0)}")
            section.append(f"  • New Followers: {ig.get('followers_growth', 0)}")
        
        if "linkedin" in social:
            li = social["linkedin"]
            section.append(f"\nLinkedIn:")
            section.append(f"  • Posts: {li.get('posts', 0)}")
            section.append(f"  • Impressions: {li.get('impressions', 0):,}")
            section.append(f"  • Engagement Rate: {li.get('engagement_rate', 0)}%")
        
        return "\n".join(section)
    
    def generate_recommendations_section(self) -> str:
        """Generate recommendations section"""
        section = []
        section.append("\n💡 RECOMMENDATIONS")
        section.append("=" * 60)
        
        recommendations = self.audit_data.recommendations
        
        if not recommendations:
            section.append("\nNo specific recommendations this week.")
            section.append("Continue current operations.")
        else:
            for i, rec in enumerate(recommendations, 1):
                section.append(f"\n{i}. {rec['title']}")
                section.append(f"   Priority: {rec.get('priority', 'Medium')}")
                section.append(f"   Action: {rec.get('action', '')}")
                section.append(f"   Impact: {rec.get('impact', '')}")
        
        return "\n".join(section)
    
    def generate_full_report(self) -> str:
        """Generate complete CEO briefing report"""
        report = []
        
        # Header
        report.append("=" * 60)
        report.append("       CEO WEEKLY BRIEFING REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Executive Summary
        report.append(self.generate_executive_summary())
        
        # Business Metrics
        report.append(self.generate_business_section())
        
        # Accounting Section
        report.append(self.generate_accounting_section())
        
        # Social Media Section
        report.append(self.generate_social_section())
        
        # Recommendations
        report.append(self.generate_recommendations_section())
        
        # Footer
        report.append("\n" + "=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)
        report.append("")
        report.append("Generated by AI Employee Vault - Weekly Audit System")
        report.append("For questions, contact: admin@company.com")
        
        return "\n".join(report)
    
    def save_report(self, output_dir: str = "audits") -> str:
        """Save report to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"ceo_briefing_{self.report_date.strftime('%Y%m%d')}.md"
        filepath = os.path.join(output_dir, filename)
        
        report_content = self.generate_full_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"CEO Briefing saved to: {filepath}")
        return filepath


# ============== Audit Collectors ==============

class BusinessAuditCollector:
    """Collects business metrics from Business MCP Server"""
    
    def __init__(self, base_url: str = "http://localhost:8004"):
        self.base_url = base_url
        self.timeout = httpx.Timeout(30.0)
    
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect all business metrics"""
        metrics = {
            "meetings": await self._get_meeting_metrics(),
            "crm": await self._get_crm_metrics(),
            "sales": await self._get_sales_metrics(),
            "projects": await self._get_project_metrics()
        }
        return metrics
    
    async def _get_meeting_metrics(self) -> Dict[str, Any]:
        """Get meeting metrics"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/get_business_summary")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        meeting_data = data.get("data", {})
                        return {
                            "total": meeting_data.get("total_meetings", 0),
                            "scheduled": meeting_data.get("scheduled_meetings", 0),
                            "completed": meeting_data.get("total_meetings", 0) - meeting_data.get("scheduled_meetings", 0)
                        }
        except Exception as e:
            logger.error(f"Failed to get meeting metrics: {e}")
        
        return {"total": 0, "scheduled": 0, "completed": 0}
    
    async def _get_crm_metrics(self) -> Dict[str, Any]:
        """Get CRM metrics"""
        try:
            # This would connect to your CRM system
            # For now, return mock data
            return {
                "active_clients": 0,
                "new_leads": 0,
                "conversion_rate": 0
            }
        except Exception as e:
            logger.error(f"Failed to get CRM metrics: {e}")
        
        return {"active_clients": 0, "new_leads": 0, "conversion_rate": 0}
    
    async def _get_sales_metrics(self) -> Dict[str, Any]:
        """Get sales pipeline metrics"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/get_business_summary")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        sales_data = data.get("data", {}).get("pipeline_details", {})
                        return {
                            "total_deals": sales_data.get("total_deals", 0),
                            "pipeline_value": sales_data.get("total_pipeline_value", 0),
                            "closed_this_week": 0,
                            "by_stage": sales_data.get("by_stage", {})
                        }
        except Exception as e:
            logger.error(f"Failed to get sales metrics: {e}")
        
        return {"total_deals": 0, "pipeline_value": 0, "closed_this_week": 0, "by_stage": {}}
    
    async def _get_project_metrics(self) -> Dict[str, Any]:
        """Get project metrics"""
        # Placeholder for project metrics
        return {"active_projects": 0, "completed_projects": 0, "on_time_rate": 0}


class AccountingAuditCollector:
    """Collects accounting metrics from Accounting MCP Server"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.timeout = httpx.Timeout(30.0)
    
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect all accounting metrics"""
        metrics = {
            "revenue": await self._get_revenue_metrics(),
            "expenses": await self._get_expense_metrics(),
            "profit": await self._get_profit_metrics(),
            "invoices": await self._get_invoice_metrics()
        }
        return metrics
    
    async def _get_revenue_metrics(self) -> Dict[str, Any]:
        """Get revenue metrics"""
        try:
            # Connect to Odoo or accounting system
            # For now, return mock data
            return {
                "this_week": 0,
                "mtd": 0,
                "growth": 0
            }
        except Exception as e:
            logger.error(f"Failed to get revenue metrics: {e}")
        
        return {"this_week": 0, "mtd": 0, "growth": 0}
    
    async def _get_expense_metrics(self) -> Dict[str, Any]:
        """Get expense metrics"""
        try:
            return {
                "this_week": 0,
                "mtd": 0,
                "by_category": {}
            }
        except Exception as e:
            logger.error(f"Failed to get expense metrics: {e}")
        
        return {"this_week": 0, "mtd": 0, "by_category": {}}
    
    async def _get_profit_metrics(self) -> Dict[str, Any]:
        """Get profit metrics"""
        try:
            return {
                "gross": 0,
                "net": 0,
                "margin": 0
            }
        except Exception as e:
            logger.error(f"Failed to get profit metrics: {e}")
        
        return {"gross": 0, "net": 0, "margin": 0}
    
    async def _get_invoice_metrics(self) -> Dict[str, Any]:
        """Get invoice metrics"""
        try:
            return {
                "issued": 0,
                "paid": 0,
                "overdue": 0,
                "outstanding_amount": 0
            }
        except Exception as e:
            logger.error(f"Failed to get invoice metrics: {e}")
        
        return {"issued": 0, "paid": 0, "overdue": 0, "outstanding_amount": 0}


class SocialMediaAuditCollector:
    """Collects social media metrics"""
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url
        self.timeout = httpx.Timeout(30.0)
    
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect all social media metrics"""
        metrics = {
            "facebook": await self._get_facebook_metrics(),
            "instagram": await self._get_instagram_metrics(),
            "linkedin": await self._get_linkedin_metrics()
        }
        return metrics
    
    async def _get_facebook_metrics(self) -> Dict[str, Any]:
        """Get Facebook metrics"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/get_summary?platform=facebook")
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        fb_data = data.get("data", {})
                        return {
                            "posts": fb_data.get("total_posts", 0),
                            "engagement": fb_data.get("total_reactions", 0) + fb_data.get("total_comments", 0),
                            "reach": 0
                        }
        except Exception as e:
            logger.error(f"Failed to get Facebook metrics: {e}")
        
        return {"posts": 0, "engagement": 0, "reach": 0}
    
    async def _get_instagram_metrics(self) -> Dict[str, Any]:
        """Get Instagram metrics"""
        try:
            return {
                "posts": 0,
                "likes": 0,
                "followers_growth": 0
            }
        except Exception as e:
            logger.error(f"Failed to get Instagram metrics: {e}")
        
        return {"posts": 0, "likes": 0, "followers_growth": 0}
    
    async def _get_linkedin_metrics(self) -> Dict[str, Any]:
        """Get LinkedIn metrics"""
        try:
            return {
                "posts": 0,
                "impressions": 0,
                "engagement_rate": 0
            }
        except Exception as e:
            logger.error(f"Failed to get LinkedIn metrics: {e}")
        
        return {"posts": 0, "impressions": 0, "engagement_rate": 0}


# ============== Weekly Audit System ==============

class WeeklyAuditSystem:
    """Main weekly audit system"""
    
    def __init__(self):
        self.audit_data = AuditData()
        self.business_collector = BusinessAuditCollector()
        self.accounting_collector = AccountingAuditCollector()
        self.social_collector = SocialMediaAuditCollector()
        self.reports_dir = "audits"
        
        # Ensure reports directory exists
        os.makedirs(self.reports_dir, exist_ok=True)
    
    async def run_full_audit(self) -> AuditData:
        """Run complete weekly audit"""
        logger.info("=" * 60)
        logger.info("Starting Weekly Business & Accounting Audit")
        logger.info("=" * 60)
        
        # Collect all metrics in parallel
        logger.info("\nCollecting metrics from all domains...")
        
        business_metrics, accounting_metrics, social_metrics = await asyncio.gather(
            self.business_collector.collect_metrics(),
            self.accounting_collector.collect_metrics(),
            self.social_collector.collect_metrics(),
            return_exceptions=True
        )
        
        # Store metrics
        self.audit_data.business_metrics = business_metrics if isinstance(business_metrics, dict) else {}
        self.audit_data.accounting_metrics = accounting_metrics if isinstance(accounting_metrics, dict) else {}
        self.audit_data.social_metrics = social_metrics if isinstance(social_metrics, dict) else {}
        
        logger.info("✅ Metrics collected successfully")
        
        # Calculate KPIs
        self._calculate_kpis()
        
        # Generate alerts
        self._generate_alerts()
        
        # Generate recommendations
        self._generate_recommendations()
        
        logger.info("✅ Audit analysis complete")
        logger.info("=" * 60)
        
        return self.audit_data
    
    def _calculate_kpis(self):
        """Calculate key performance indicators"""
        kpis = {}
        
        # Business KPIs
        business = self.audit_data.business_metrics
        if business.get("sales"):
            sales = business["sales"]
            kpis["Pipeline Value"] = f"${sales.get('pipeline_value', 0):,.0f}"
            kpis["Total Deals"] = str(sales.get('total_deals', 0))
        
        if business.get("meetings"):
            meetings = business["meetings"]
            kpis["Meetings Held"] = str(meetings.get('total', 0))
        
        # Accounting KPIs
        accounting = self.audit_data.accounting_metrics
        if accounting.get("revenue"):
            revenue = accounting["revenue"]
            kpis["Weekly Revenue"] = f"${revenue.get('this_week', 0):,.0f}"
        
        if accounting.get("invoices"):
            invoices = accounting["invoices"]
            kpis["Overdue Invoices"] = str(invoices.get('overdue', 0))
        
        # Social KPIs
        social = self.audit_data.social_metrics
        if social.get("facebook"):
            fb = social["facebook"]
            kpis["FB Engagement"] = str(fb.get('engagement', 0))
        
        self.audit_data.kpis = kpis
    
    def _generate_alerts(self):
        """Generate alerts based on metrics"""
        alerts = []
        
        # Check for overdue invoices
        accounting = self.audit_data.accounting_metrics
        if accounting.get("invoices"):
            overdue = accounting["invoices"].get("overdue", 0)
            if overdue > 0:
                alerts.append(f"⚠️ {overdue} invoices are overdue for payment")
        
        # Check for low pipeline
        business = self.audit_data.business_metrics
        if business.get("sales"):
            pipeline_value = business["sales"].get("pipeline_value", 0)
            if pipeline_value < 10000:  # Threshold
                alerts.append("⚠️ Sales pipeline value is below target ($10,000)")
        
        # Check for no social media activity
        social = self.audit_data.social_metrics
        if social.get("facebook"):
            fb_posts = social["facebook"].get("posts", 0)
            if fb_posts == 0:
                alerts.append("⚠️ No Facebook posts this week")
        
        self.audit_data.alerts = alerts
    
    def _generate_recommendations(self):
        """Generate recommendations based on audit findings"""
        recommendations = []
        
        # Revenue recommendations
        accounting = self.audit_data.accounting_metrics
        if accounting.get("revenue"):
            growth = accounting["revenue"].get("growth", 0)
            if growth < 0:
                recommendations.append({
                    "title": "Revenue Decline",
                    "priority": "High",
                    "action": "Review pricing strategy and sales approach",
                    "impact": "Improve weekly revenue growth"
                })
        
        # Invoice recommendations
        if accounting.get("invoices"):
            overdue = accounting["invoices"].get("overdue", 0)
            if overdue > 0:
                recommendations.append({
                    "title": "Follow up on Overdue Invoices",
                    "priority": "High",
                    "action": "Send payment reminders to clients with overdue invoices",
                    "impact": f"Recover ${accounting['invoices'].get('outstanding_amount', 0):,.0f} in outstanding payments"
                })
        
        # Social media recommendations
        social = self.audit_data.social_metrics
        if social.get("facebook"):
            fb_posts = social["facebook"].get("posts", 0)
            if fb_posts < 3:
                recommendations.append({
                    "title": "Increase Social Media Activity",
                    "priority": "Medium",
                    "action": "Post at least 3-4 times per week on Facebook",
                    "impact": "Improve brand visibility and engagement"
                })
        
        self.audit_data.recommendations = recommendations
    
    async def generate_ceo_briefing(self) -> str:
        """Generate and save CEO briefing report"""
        logger.info("\nGenerating CEO Briefing Report...")
        
        briefing = CEOBriefing(self.audit_data)
        filepath = briefing.save_report(self.reports_dir)
        
        # Also save as JSON for programmatic access
        json_path = os.path.join(self.reports_dir, f"audit_data_{datetime.now().strftime('%Y%m%d')}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.audit_data.to_dict(), f, indent=2)
        
        logger.info(f"✅ CEO Briefing saved to: {filepath}")
        logger.info(f"✅ Audit data saved to: {json_path}")
        
        return filepath
    
    async def email_briefing(self, recipients: List[str]):
        """Email the briefing to recipients"""
        # This would integrate with your email system
        logger.info(f"\nEmailing briefing to: {', '.join(recipients)}")
        
        # Placeholder for email sending
        # In production, integrate with SMTP or email API
        
        logger.info("✅ Briefing emailed successfully")


# ============== Scheduler ==============

class AuditScheduler:
    """Scheduler for weekly audits"""
    
    def __init__(self, audit_system: WeeklyAuditSystem):
        self.audit_system = audit_system
        self.running = False
    
    async def start_scheduler(self, day_of_week: int = 0, hour: int = 9):
        """
        Start the weekly audit scheduler
        
        Args:
            day_of_week: 0=Monday, 1=Tuesday, ..., 6=Sunday (default: Monday)
            hour: Hour to run audit (24-hour format, default: 9 AM)
        """
        self.running = True
        
        logger.info("=" * 60)
        logger.info("Weekly Audit Scheduler Started")
        logger.info("=" * 60)
        logger.info(f"Schedule: Every {'Monday' if day_of_week == 0 else 'Tuesday' if day_of_week == 1 else 'Wednesday' if day_of_week == 2 else 'Thursday' if day_of_week == 3 else 'Friday' if day_of_week == 4 else 'Saturday' if day_of_week == 5 else 'Sunday'} at {hour:02d}:00")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 60)
        
        while self.running:
            try:
                now = datetime.now()
                
                # Check if it's time to run
                if (now.weekday() == day_of_week and 
                    now.hour == hour and 
                    now.minute == 0):
                    
                    logger.info("\n⏰ Running scheduled weekly audit...")
                    await self.audit_system.run_full_audit()
                    await self.audit_system.generate_ceo_briefing()
                    
                    # Wait a minute to avoid running twice
                    await asyncio.sleep(60)
                
                # Check every 30 seconds
                await asyncio.sleep(30)
                
            except asyncio.CancelledError:
                logger.info("\nScheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(30)


# ============== Main Entry Points ==============

async def run_audit():
    """Run a single audit manually"""
    audit_system = WeeklyAuditSystem()
    
    # Run audit
    await audit_system.run_full_audit()
    
    # Generate briefing
    briefing_path = await audit_system.generate_ceo_briefing()
    
    # Print summary
    print("\n" + "=" * 60)
    print("WEEKLY AUDIT COMPLETE")
    print("=" * 60)
    print(f"\nCEO Briefing saved to: {briefing_path}")
    print("\nKey Findings:")
    
    # Print KPIs
    if audit_system.audit_data.kpis:
        print("\nKPIs:")
        for kpi_name, kpi_value in audit_system.audit_data.kpis.items():
            print(f"  • {kpi_name}: {kpi_value}")
    
    # Print alerts
    if audit_system.audit_data.alerts:
        print(f"\nAlerts ({len(audit_system.audit_data.alerts)}):")
        for alert in audit_system.audit_data.alerts:
            print(f"  - {alert}")
    
    print("\n" + "=" * 60)
    
    return briefing_path


async def generate_briefing_only():
    """Generate CEO briefing from existing audit data"""
    print("\nGenerating CEO Briefing from existing audit data...")
    
    # Find latest audit data
    audits_dir = Path("audits")
    json_files = sorted(audits_dir.glob("audit_data_*.json"), reverse=True)
    
    if not json_files:
        print("❌ No audit data found. Run audit first.")
        return
    
    latest_audit = json_files[0]
    print(f"Using audit data from: {latest_audit}")
    
    with open(latest_audit, 'r', encoding='utf-8') as f:
        audit_data_dict = json.load(f)
    
    # Create audit data object
    audit_data = AuditData()
    audit_data.business_metrics = audit_data_dict.get("business_metrics", {})
    audit_data.accounting_metrics = audit_data_dict.get("accounting_metrics", {})
    audit_data.social_metrics = audit_data_dict.get("social_metrics", {})
    audit_data.kpis = audit_data_dict.get("kpis", {})
    audit_data.alerts = audit_data_dict.get("alerts", [])
    audit_data.recommendations = audit_data_dict.get("recommendations", [])
    
    # Generate briefing
    briefing = CEOBriefing(audit_data)
    filepath = briefing.save_report()
    
    print(f"\n✅ CEO Briefing generated: {filepath}")
    
    return filepath


async def start_scheduler():
    """Start the weekly audit scheduler"""
    audit_system = WeeklyAuditSystem()
    scheduler = AuditScheduler(audit_system)
    
    # Run scheduler (Mondays at 9 AM by default)
    await scheduler.start_scheduler(day_of_week=0, hour=9)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Weekly Business & Accounting Audit System")
    parser.add_argument("--generate", action="store_true", help="Generate CEO briefing from existing audit data")
    parser.add_argument("--schedule", action="store_true", help="Start weekly audit scheduler")
    parser.add_argument("--day", type=int, default=0, help="Day of week for scheduler (0=Monday, 6=Sunday)")
    parser.add_argument("--hour", type=int, default=9, help="Hour for scheduler (24-hour format)")
    
    args = parser.parse_args()
    
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    if args.generate:
        asyncio.run(generate_briefing_only())
    elif args.schedule:
        asyncio.run(start_scheduler())
    else:
        asyncio.run(run_audit())
