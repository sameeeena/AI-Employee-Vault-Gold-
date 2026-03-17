"""
Social Media Scheduled Posting Manager

Handles automatic posting of scheduled content:
- Recurring post schedules (daily, weekly, monthly)
- Auto-posting at scheduled times
- Post queue management
- Integration with Facebook/Instagram module

Usage:
    python social_scheduler.py
    
Or run as background service:
    start python social_scheduler.py
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import aiofiles
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

# Import integration module
from facebook_instagram_integration import FacebookInstagramIntegration
from social_content_calendar import (
    ContentCalendarManager,
    PostTemplatesLibrary,
    ScheduledPost
)


# ============== Recurring Post Configuration ==============

class RecurringPostSchedule:
    """Defines a recurring post schedule"""

    def __init__(self, id: str, template_id: str, variables: Dict[str, str],
                 platforms: List[str], recurrence: str,  # daily, weekly, monthly
                 posting_times: List[str],  # ["09:00", "18:00"]
                 days_of_week: Optional[List[int]] = None,  # 0=Monday, 6=Sunday
                 day_of_month: Optional[int] = None,  # 1-31
                 active: bool = True):
        self.id = id
        self.template_id = template_id
        self.variables = variables
        self.platforms = platforms
        self.recurrence = recurrence
        self.posting_times = posting_times
        self.days_of_week = days_of_week or []
        self.day_of_month = day_of_month
        self.active = active
        self.created_at = datetime.now().isoformat()
        self.last_posted = None
        self.total_posts = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "id": self.id,
            "template_id": self.template_id,
            "variables": self.variables,
            "platforms": self.platforms,
            "recurrence": self.recurrence,
            "posting_times": self.posting_times,
            "days_of_week": self.days_of_week,
            "day_of_month": self.day_of_month,
            "active": self.active,
            "created_at": self.created_at,
            "last_posted": self.last_posted,
            "total_posts": self.total_posts
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecurringPostSchedule":
        """Create from dictionary"""
        schedule = cls(
            id=data["id"],
            template_id=data["template_id"],
            variables=data["variables"],
            platforms=data["platforms"],
            recurrence=data["recurrence"],
            posting_times=data["posting_times"],
            days_of_week=data.get("days_of_week", []),
            day_of_month=data.get("day_of_month"),
            active=data.get("active", True)
        )
        schedule.created_at = data.get("created_at", schedule.created_at)
        schedule.last_posted = data.get("last_posted")
        schedule.total_posts = data.get("total_posts", 0)
        return schedule

    def should_post_today(self, date: datetime) -> bool:
        """Check if we should post on this day based on schedule"""
        if not self.active:
            return False

        if self.recurrence == "daily":
            return True
        elif self.recurrence == "weekly":
            # Convert Python weekday (0=Monday) to schedule format
            return date.weekday() in self.days_of_week
        elif self.recurrence == "monthly":
            return date.day == self.day_of_month

        return False

    def get_posting_times_today(self) -> List[str]:
        """Get posting times for today"""
        return self.posting_times


# ============== Scheduled Post Manager ==============

class ScheduledPostManager:
    """Manages scheduled and recurring posts"""

    def __init__(self):
        self.schedules_file = "state/recurring_schedules.json"
        self.post_log_file = "logs/scheduled_posts_log.md"
        self._ensure_files()
        self.calendar_manager = ContentCalendarManager()
        self.templates = PostTemplatesLibrary()
        self.integration = FacebookInstagramIntegration(
            mock_mode=os.getenv("SOCIAL_MOCK_MODE", "true").lower() == "true"
        )

    def _ensure_files(self):
        """Ensure required files exist"""
        os.makedirs("state", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.schedules_file):
            self._save_schedules([])

        if not os.path.exists(self.post_log_file):
            with open(self.post_log_file, "w", encoding="utf-8") as f:
                f.write("# Scheduled Posts Log\n\n")

    def _load_schedules(self) -> List[Dict[str, Any]]:
        """Load recurring schedules"""
        try:
            with open(self.schedules_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_schedules(self, schedules: List[Dict[str, Any]]):
        """Save recurring schedules"""
        with open(self.schedules_file, "w", encoding="utf-8") as f:
            json.dump(schedules, f, indent=2)

    async def create_recurring_schedule(self, template_id: str, variables: Dict[str, str],
                                        platforms: List[str], recurrence: str,
                                        posting_times: List[str],
                                        days_of_week: Optional[List[int]] = None,
                                        day_of_month: Optional[int] = None) -> str:
        """
        Create a new recurring post schedule

        Args:
            template_id: Template to use
            variables: Template variables
            platforms: Target platforms
            recurrence: daily, weekly, monthly
            posting_times: Times to post (e.g., ["09:00", "18:00"])
            days_of_week: For weekly: [0, 2, 4] = Mon, Wed, Fri
            day_of_month: For monthly: 15 = 15th of each month

        Returns:
            Schedule ID
        """
        schedules = self._load_schedules()

        schedule = RecurringPostSchedule(
            id=f"schedule_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            template_id=template_id,
            variables=variables,
            platforms=platforms,
            recurrence=recurrence,
            posting_times=posting_times,
            days_of_week=days_of_week,
            day_of_month=day_of_month
        )

        schedules.append(schedule.to_dict())
        self._save_schedules(schedules)

        logger.info(f"✅ Created recurring schedule: {schedule.id} ({recurrence})")
        return schedule.id

    async def get_all_schedules(self) -> List[RecurringPostSchedule]:
        """Get all recurring schedules"""
        schedules = self._load_schedules()
        return [RecurringPostSchedule.from_dict(s) for s in schedules]

    async def activate_schedule(self, schedule_id: str) -> bool:
        """Activate a schedule"""
        schedules = self._load_schedules()

        for schedule in schedules:
            if schedule["id"] == schedule_id:
                schedule["active"] = True
                self._save_schedules(schedules)
                logger.info(f"✅ Activated schedule: {schedule_id}")
                return True

        return False

    async def deactivate_schedule(self, schedule_id: str) -> bool:
        """Deactivate a schedule"""
        schedules = self._load_schedules()

        for schedule in schedules:
            if schedule["id"] == schedule_id:
                schedule["active"] = False
                self._save_schedules(schedules)
                logger.info(f"✅ Deactivated schedule: {schedule_id}")
                return True

        return False

    async def delete_schedule(self, schedule_id: str) -> bool:
        """Delete a schedule"""
        schedules = self._load_schedules()
        original_count = len(schedules)

        schedules = [s for s in schedules if s["id"] != schedule_id]

        if len(schedules) < original_count:
            self._save_schedules(schedules)
            logger.info(f"✅ Deleted schedule: {schedule_id}")
            return True

        return False

    async def process_schedules(self) -> List[Dict[str, Any]]:
        """
        Process all schedules and create posts for today
        Returns list of posts created
        """
        schedules = await self.get_all_schedules()
        today = datetime.now()
        posts_created = []

        logger.info(f"🔄 Processing schedules for {today.strftime('%Y-%m-%d')}...")

        for schedule in schedules:
            if not schedule.should_post_today(today):
                continue

            for time_str in schedule.get_posting_times_today():
                try:
                    # Parse time
                    hour, minute = map(int, time_str.split(":"))
                    scheduled_time = today.replace(
                        hour=hour, minute=minute, second=0, microsecond=0
                    )

                    # Render message from template
                    message = self.templates.render_template(
                        schedule.template_id,
                        schedule.variables
                    )

                    if not message:
                        logger.error(f"Template {schedule.template_id} not found")
                        continue

                    # Schedule the post
                    post = await self.calendar_manager.schedule_post(
                        message=message,
                        platforms=schedule.platforms,
                        scheduled_time=scheduled_time,
                        template_id=schedule.template_id
                    )

                    posts_created.append({
                        "schedule_id": schedule.id,
                        "post_id": post.id,
                        "scheduled_time": scheduled_time.isoformat()
                    })

                    logger.info(f"  ✅ Scheduled post from {schedule.recurrence} schedule")

                except Exception as e:
                    logger.error(f"  ❌ Error processing schedule {schedule.id}: {e}")

        return posts_created

    async def post_due_content(self) -> List[Dict[str, Any]]:
        """
        Check for posts that are due and post them now
        Returns list of posts that were published
        """
        pending_posts = await self.calendar_manager.get_pending_posts()
        now = datetime.now()
        posted = []

        logger.info(f"📤 Checking for posts due... ({len(pending_posts)} pending)")

        for post in pending_posts:
            scheduled_time = datetime.fromisoformat(post.scheduled_time)

            # Check if post is due (within last hour)
            time_diff = now - scheduled_time
            if time_diff.total_seconds() < 0:
                # Not yet time
                continue

            if time_diff.total_seconds() > 3600:
                # More than an hour late, skip
                logger.warning(f"  ⚠️ Skipping post {post.id} - over an hour late")
                continue

            try:
                # Post to platforms
                result = None
                if "both" in post.platforms or len(post.platforms) > 1:
                    result = await self.integration.post_to_both(
                        message=post.message,
                        image_url=post.image_url,
                        link=post.link
                    )
                elif "facebook" in post.platforms:
                    result = await self.integration.post_to_facebook(
                        message=post.message,
                        image_url=post.image_url,
                        link=post.link
                    )
                elif "instagram" in post.platforms:
                    result = await self.integration.post_to_instagram(
                        message=post.message,
                        image_url=post.image_url,
                        is_reel=post.is_reel
                    )

                if result:
                    # Mark as posted
                    post_ids = {}
                    if isinstance(result, dict):
                        if "facebook" in result:
                            post_ids["facebook"] = result["facebook"].get("post_id")
                        if "instagram" in result:
                            post_ids["instagram"] = result["instagram"].get("post_id")
                        if "post_id" in result:
                            post_ids["single"] = result["post_id"]

                    await self.calendar_manager.mark_post_posted(post.id, post_ids)

                    # Log the post
                    await self._log_post(post, result)

                    posted.append({
                        "post_id": post.id,
                        "platforms": post.platforms,
                        "result": result
                    })

                    logger.info(f"  ✅ Posted to {post.platforms}: {post.message[:50]}...")

            except Exception as e:
                logger.error(f"  ❌ Error posting {post.id}: {e}")
                # Mark as failed
                calendar = self.calendar_manager._load_calendar()
                for p in calendar:
                    if p["id"] == post.id:
                        p["status"] = "failed"
                        p["error"] = str(e)
                        self.calendar_manager._save_calendar(calendar)
                        break

        return posted

    async def _log_post(self, post: ScheduledPost, result: Dict[str, Any]):
        """Log a posted item to the log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"""
## Post Published - {timestamp}

- **Post ID:** {post.id}
- **Platforms:** {', '.join(post.platforms)}
- **Status:** ✅ Success
- **Message:** {post.message[:200]}...
- **Hashtags:** {' '.join(post.hashtags[:5]) if post.hashtags else 'None'}
- **Scheduled Time:** {post.scheduled_time}
- **Posted At:** {datetime.now().isoformat()}

### Results:
```json
{json.dumps(result, indent=2)[:500]}
```

---
"""

        async with aiofiles.open(self.post_log_file, "a", encoding="utf-8") as f:
            await f.write(log_entry)

    async def run_scheduler(self, check_interval: int = 60):
        """
        Run the scheduler continuously

        Args:
            check_interval: How often to check for posts (seconds)
        """
        logger.info("🚀 Starting Scheduled Post Manager...")
        logger.info(f"   Check interval: {check_interval} seconds")
        logger.info(f"   Mock mode: {self.integration.mock_mode}")

        last_date = None

        while True:
            try:
                current_date = datetime.now().date()

                # Process recurring schedules once per day
                if current_date != last_date:
                    logger.info(f"\n📅 New day detected: {current_date}")
                    await self.process_schedules()
                    last_date = current_date

                # Check for posts due
                await self.post_due_content()

                # Wait
                await asyncio.sleep(check_interval)

            except asyncio.CancelledError:
                logger.info("🛑 Scheduler stopped")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(check_interval)


# ============== Quick Setup Helpers ==============

async def setup_default_schedules():
    """Set up some default recurring schedules"""
    manager = ScheduledPostManager()

    print("Setting up default recurring schedules...")
    print("-" * 80)

    # Daily motivational quote (morning)
    schedule1 = await manager.create_recurring_schedule(
        template_id="template_motivation",
        variables={
            "motivational_quote": "Success is not final, failure is not fatal: It is the courage to continue that counts.",
            "quote_author": "Winston Churchill"
        },
        platforms=["facebook", "instagram"],
        recurrence="daily",
        posting_times=["08:00"],
        days_of_week=[0, 1, 2, 3, 4]  # Weekdays
    )
    print(f"  ✅ Created: Daily Motivation (Weekdays @ 8:00 AM) - ID: {schedule1}")

    # Daily tip (afternoon)
    schedule2 = await manager.create_recurring_schedule(
        template_id="template_educational",
        variables={
            "tip_title": "Boost Your Productivity",
            "tip_content": "Use the Pomodoro Technique: Work for 25 minutes, then take a 5-minute break. Repeat 4 times, then take a longer 15-30 minute break."
        },
        platforms=["facebook", "instagram"],
        recurrence="daily",
        posting_times=["14:00"],
        days_of_week=[0, 1, 2, 3, 4]
    )
    print(f"  ✅ Created: Daily Tip (Weekdays @ 2:00 PM) - ID: {schedule2}")

    # Friday fun post
    schedule3 = await manager.create_recurring_schedule(
        template_id="template_friday_fun",
        variables={
            "friday_content": "Time to celebrate another week of achievements! 🎉"
        },
        platforms=["facebook", "instagram"],
        recurrence="weekly",
        posting_times=["17:00"],
        days_of_week=[4]  # Friday
    )
    print(f"  ✅ Created: Friday Fun (Fridays @ 5:00 PM) - ID: {schedule3}")

    # Weekly engagement question
    schedule4 = await manager.create_recurring_schedule(
        template_id="template_engagement",
        variables={
            "engagement_question": "What's one goal you want to achieve this week?"
        },
        platforms=["facebook", "instagram"],
        recurrence="weekly",
        posting_times=["09:00"],
        days_of_week=[0]  # Monday
    )
    print(f"  ✅ Created: Monday Question (Mondays @ 9:00 AM) - ID: {schedule4}")

    # Monthly announcement
    schedule5 = await manager.create_recurring_schedule(
        template_id="template_announcement",
        variables={
            "announcement_title": "Monthly Update",
            "announcement_details": "Check out what we've accomplished this month! Thank you for your continued support."
        },
        platforms=["facebook", "instagram"],
        recurrence="monthly",
        posting_times=["10:00"],
        day_of_month=1
    )
    print(f"  ✅ Created: Monthly Update (1st of month @ 10:00 AM) - ID: {schedule5}")

    print("\n" + "=" * 80)
    print("Default schedules created successfully!")
    print("\nTo modify or add schedules, edit 'state/recurring_schedules.json'")

    return manager


# ============== Main Entry Points ==============

async def run_demo():
    """Run a demo of the scheduler"""
    print("=" * 80)
    print(" SCHEDULED POST MANAGER - DEMO")
    print("=" * 80)

    manager = ScheduledPostManager()

    # Show existing schedules
    print("\n📋 Existing Recurring Schedules:")
    print("-" * 80)
    schedules = await manager.get_all_schedules()

    if not schedules:
        print("  No schedules found. Setting up default schedules...")
        await setup_default_schedules()
        schedules = await manager.get_all_schedules()

    for schedule in schedules:
        status = "🟢 Active" if schedule.active else "🔴 Inactive"
        print(f"  {status} | {schedule.id}")
        print(f"    Template: {schedule.template_id}")
        print(f"    Recurrence: {schedule.recurrence}")
        print(f"    Times: {', '.join(schedule.posting_times)}")
        if schedule.recurrence == "weekly":
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            day_names = [days[d] for d in schedule.days_of_week]
            print(f"    Days: {', '.join(day_names)}")
        elif schedule.recurrence == "monthly":
            print(f"    Day of month: {schedule.day_of_month}")
        print(f"    Total posts: {schedule.total_posts}")
        print()

    # Process today's schedules
    print("\n🔄 Processing Today's Schedules:")
    print("-" * 80)
    posts_created = await manager.process_schedules()

    if posts_created:
        for item in posts_created:
            print(f"  ✅ Created: {item['post_id']} @ {item['scheduled_time']}")
    else:
        print("  No new posts scheduled for today")

    # Check for posts due now
    print("\n📤 Checking for Posts Due Now:")
    print("-" * 80)
    posted = await manager.post_due_content()

    if posted:
        for item in posted:
            print(f"  ✅ Posted: {item['post_id']} to {item['platforms']}")
    else:
        print("  No posts due at this time")

    print("\n" + "=" * 80)
    print(" DEMO COMPLETED!")
    print("=" * 80)
    print("\nTo run the scheduler continuously:")
    print("  python social_scheduler.py")
    print("\nTo set up default schedules:")
    print("  python -c \"import asyncio; from social_scheduler import setup_default_schedules; asyncio.run(setup_default_schedules())\"")


async def main():
    """Main entry point - runs the scheduler"""
    manager = ScheduledPostManager()

    # Process schedules once at startup
    await manager.process_schedules()

    # Run continuous scheduler
    await manager.run_scheduler(check_interval=60)  # Check every minute


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        asyncio.run(run_demo())
    else:
        asyncio.run(main())
