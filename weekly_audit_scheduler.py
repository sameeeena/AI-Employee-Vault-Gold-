"""
Weekly Business Audit Scheduler

Script to run the weekly business audit skill automatically every 7 days.
"""

import asyncio
import schedule
import time
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from weekly_business_audit_skill import weekly_business_audit_skill


def run_weekly_audit():
    """Run the weekly business audit skill"""
    logger.info("Starting weekly business audit...")
    try:
        # Run the async function
        result = asyncio.run(weekly_business_audit_skill())
        logger.info("Weekly business audit completed successfully")
        logger.debug(f"Audit result: {result[:200]}...")  # Log first 200 chars
    except Exception as e:
        logger.error(f"Error running weekly business audit: {str(e)}")


def main():
    """Main scheduler function"""
    logger.info("Weekly Business Audit Scheduler started")

    # Schedule the job to run every 7 days (weekly)
    schedule.every(7).days.do(run_weekly_audit)

    # Alternative: Run at a specific day/time each week (e.g., every Monday at 9 AM)
    # schedule.every().monday.at("09:00").do(run_weekly_audit)

    logger.info("Scheduler configured to run weekly audit every 7 days")

    # Run the first audit immediately for testing
    logger.info("Running initial audit...")
    run_weekly_audit()

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour


if __name__ == "__main__":
    main()