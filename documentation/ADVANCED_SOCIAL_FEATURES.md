# 🚀 Advanced Social Media Features - COMPLETE

**Facebook & Instagram Integration - Enhanced with Advanced Features**

**Status:** ✅ COMPLETE | **Version:** 3.0.0 | **Date:** 2026-03-10

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [New Features](#new-features)
3. [File Structure](#file-structure)
4. [Setup & Installation](#setup--installation)
5. [Feature 1: Post Templates Library](#feature-1-post-templates-library)
6. [Feature 2: Hashtag Suggestions](#feature-2-hashtag-suggestions)
7. [Feature 3: Content Calendar](#feature-3-content-calendar)
8. [Feature 4: Scheduled Posting](#feature-4-scheduled-posting)
9. [Feature 5: Analytics Dashboard](#feature-5-analytics-dashboard)
10. [API Reference](#api-reference)
11. [Usage Examples](#usage-examples)
12. [Testing](#testing)
13. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This enhanced social media integration builds upon the existing Facebook & Instagram module to provide **advanced automation and content management** capabilities:

- ✅ **10 Pre-built Post Templates** for common use cases
- ✅ **Smart Hashtag Suggestions** based on content analysis
- ✅ **Content Calendar** for visualizing and managing posts
- ✅ **Recurring Post Schedules** (daily, weekly, monthly)
- ✅ **Auto-Posting Scheduler** for hands-free operation
- ✅ **Analytics Dashboard** generation (HTML reports)

---

## ✨ New Features

### Feature Comparison

| Feature | Basic Integration | Advanced Module |
|---------|------------------|-----------------|
| Post to Facebook/Instagram | ✅ | ✅ |
| Fetch Metrics | ✅ | ✅ |
| Generate Summaries | ✅ | ✅ |
| **Post Templates** | ❌ | ✅ 10 templates |
| **Hashtag Suggestions** | ❌ | ✅ Auto-generated |
| **Content Calendar** | ❌ | ✅ Monthly view |
| **Recurring Schedules** | ❌ | ✅ Daily/Weekly/Monthly |
| **Auto-Posting** | ❌ | ✅ Scheduled times |
| **Analytics Dashboard** | ❌ | ✅ HTML reports |

---

## 📁 File Structure

```
AI Employee Vault [Gold]/
├── facebook_instagram_integration.py    # Core FB/IG integration
├── social_mcp_server_v2.py              # MCP API server
├── social_content_calendar.py           # NEW: Content calendar & templates
├── social_scheduler.py                  # NEW: Auto-posting scheduler
├── test_advanced_social_features.py     # NEW: Test suite
├── ADVANCED_SOCIAL_FEATURES.md          # NEW: This documentation
├── state/
│   ├── post_templates.json             # Custom templates
│   ├── content_calendar.json           # Scheduled posts
│   └── recurring_schedules.json        # Recurring schedules
├── dashboards/
│   └── social_analytics.html           # Analytics dashboard
└── logs/
    └── scheduled_posts_log.md          # Auto-posting log
```

---

## 🔧 Setup & Installation

### Prerequisites

Ensure you have the basic Facebook & Instagram integration working:

```bash
# Verify basic integration
python test_facebook_instagram.py
```

### Step 1: Install Dependencies

```bash
pip install fastapi uvicorn httpx python-dotenv pydantic aiofiles
```

### Step 2: Verify Configuration

Check your `.env` file has:

```bash
# Facebook Configuration
FACEBOOK_PAGE_ACCESS_TOKEN=your_token_here
FACEBOOK_PAGE_ID=1496288429174042

# Instagram Configuration
INSTAGRAM_USER_ID=your_ig_id
INSTAGRAM_ACCESS_TOKEN=your_ig_token

# Mock Mode (true for testing, false for live)
SOCIAL_MOCK_MODE=true
```

### Step 3: Run Test Suite

```bash
python test_advanced_social_features.py
```

Expected output:
```
================================================================================
   ADVANCED SOCIAL MEDIA FEATURES - TEST SUITE
================================================================================
 TEST 1: Post Templates Library
   ✅ Found 10 templates
   ...
 ALL TESTS PASSED! 🎉
```

---

## Feature 1: Post Templates Library

### Overview

Pre-built templates for common post types save time and ensure consistency.

### Available Templates

| ID | Name | Category | Best Times |
|----|------|----------|------------|
| `template_announcement` | Company Announcement | announcement | 09:00, 13:00 |
| `template_promotion` | Product/Service Promotion | promotion | 10:00, 15:00, 19:00 |
| `template_engagement` | Audience Engagement Question | engagement | 12:00, 18:00, 20:00 |
| `template_educational` | Educational/Tip Post | educational | 08:00, 14:00 |
| `template_behind_scenes` | Behind the Scenes | behind_scenes | 11:00, 17:00 |
| `template_testimonial` | Customer Testimonial | testimonial | 10:00, 16:00 |
| `template_event` | Event Announcement | event | 09:00, 18:00 |
| `template_motivation` | Motivational Quote | motivation | 07:00, 08:00, 20:00 |
| `template_product_launch` | Product Launch | launch | 09:00, 12:00 |
| `template_friday_fun` | Friday Fun Post | engagement | 15:00, 17:00 |

### Usage Examples

#### Use a Template Programmatically

```python
from social_content_calendar import PostTemplatesLibrary

templates = PostTemplatesLibrary()

# Render a template
message = templates.render_template(
    "template_promotion",
    {
        "product_name": "AI Employee Vault",
        "offer_details": "50% off first month!",
        "expiry_date": "March 31, 2026",
        "call_to_action": "Sign up now!"
    }
)

print(message)
```

Output:
```
🎉 Special Offer Alert!

AI Employee Vault: 50% off first month!

⏰ Valid until: March 31, 2026
👉 Sign up now!

#SpecialOffer #Promotion
```

#### Add Custom Template

```python
custom = {
    "name": "Welcome Post",
    "category": "engagement",
    "message_template": "👋 Welcome {new_member} to our community!",
    "suggested_hashtags": ["#Welcome", "#NewMember"],
    "best_posting_times": ["10:00", "15:00"],
    "platforms": ["facebook", "instagram"]
}

template_id = templates.add_custom_template(custom)
```

#### Get Templates by Category

```python
# Get all engagement templates
engagement_templates = templates.get_templates_by_category("engagement")
```

---

## Feature 2: Hashtag Suggestions

### Overview

AI-powered hashtag suggestions based on content analysis and category matching.

### Usage Examples

#### Suggest Hashtags from Content

```python
from social_content_calendar import HashtagSuggester

suggester = HashtagSuggester()

content = "Excited to announce our new AI-powered business automation tool!"
hashtags = suggester.suggest_hashtags(content, category="technology", count=10)

print(hashtags)
# ['#Technology', '#Tech', '#Innovation', '#AI', '#Automation', 
#  '#Business', '#Entrepreneur', '#Trending', '#Viral', '#2026']
```

#### Platform-Specific Suggestions

```python
# Instagram (more hashtags)
ig_tags = suggester.suggest_hashtags(content, platform="instagram", count=15)

# Facebook (fewer, more professional)
fb_tags = suggester.suggest_hashtags(content, platform="facebook", count=5)
```

#### Get Hashtags by Category

```python
business_tags = suggester.get_hashtags_by_category("business", count=5)
# ['#Business', '#Entrepreneur', '#BusinessOwner', '#SmallBusiness', '#BusinessTips']
```

### Available Categories

- `business`, `technology`, `marketing`, `lifestyle`
- `education`, `entertainment`, `food`, `travel`
- `fashion`, `health`, `announcement`, `promotion`, `event`

---

## Feature 3: Content Calendar

### Overview

Visualize and manage all your scheduled social media posts in one place.

### Usage Examples

#### Schedule a Post

```python
from social_content_calendar import ContentCalendarManager
from datetime import datetime, timedelta

calendar = ContentCalendarManager()

# Schedule for tomorrow at 10 AM
tomorrow = datetime.now() + timedelta(days=1)
scheduled_time = tomorrow.replace(hour=10, minute=0, second=0)

post = await calendar.schedule_post(
    message="🎉 Exciting announcement coming soon! #StayTuned",
    platforms=["facebook", "instagram"],
    scheduled_time=scheduled_time,
    image_url="https://example.com/teaser.jpg"
)

print(f"Post scheduled: {post.id}")
print(f"Time: {scheduled_time}")
print(f"Auto-suggested hashtags: {post.hashtags}")
```

#### Schedule from Template

```python
template_post = await calendar.schedule_from_template(
    template_id="template_engagement",
    variables={
        "engagement_question": "What's your favorite productivity tool?"
    },
    scheduled_time=scheduled_time,
    platforms=["facebook", "instagram"]
)
```

#### Get Pending Posts

```python
pending_posts = await calendar.get_pending_posts()

for post in pending_posts:
    print(f"{post.scheduled_time}: {post.message[:50]}...")
```

#### Generate Monthly Calendar View

```python
current_month = datetime.now().month
current_year = datetime.now().year

calendar_view = await calendar.generate_calendar_view(current_year, current_month)

print(f"Month: {current_year}-{current_month:02d}")
print(f"Total posts: {calendar_view.total_posts}")
print(f"By platform: {calendar_view.posts_by_platform}")
print(f"By category: {calendar_view.posts_by_category}")
```

#### Cancel a Scheduled Post

```python
await calendar.cancel_post(post_id)
```

---

## Feature 4: Scheduled Posting

### Overview

Set up recurring post schedules that automatically create and publish content.

### Recurrence Types

| Type | Description | Configuration |
|------|-------------|---------------|
| `daily` | Post every day | Set posting times |
| `weekly` | Post on specific days | Set days + times |
| `monthly` | Post on specific date | Set day of month + time |

### Usage Examples

#### Create Daily Recurring Schedule

```python
from social_scheduler import ScheduledPostManager

manager = ScheduledPostManager()

# Daily motivational quote (weekdays at 8 AM)
schedule_id = await manager.create_recurring_schedule(
    template_id="template_motivation",
    variables={
        "motivational_quote": "Success is not final, failure is not fatal.",
        "quote_author": "Winston Churchill"
    },
    platforms=["facebook", "instagram"],
    recurrence="daily",
    posting_times=["08:00"],
    days_of_week=[0, 1, 2, 3, 4]  # Mon-Fri
)
```

#### Create Weekly Recurring Schedule

```python
# Friday fun post (every Friday at 5 PM)
friday_id = await manager.create_recurring_schedule(
    template_id="template_friday_fun",
    variables={
        "friday_content": "Time to celebrate another week! 🎉"
    },
    platforms=["facebook", "instagram"],
    recurrence="weekly",
    posting_times=["17:00"],
    days_of_week=[4]  # Friday
)
```

#### Create Monthly Recurring Schedule

```python
# Monthly update (1st of every month at 10 AM)
monthly_id = await manager.create_recurring_schedule(
    template_id="template_announcement",
    variables={
        "announcement_title": "Monthly Update",
        "announcement_details": "Here's what we accomplished!"
    },
    platforms=["facebook", "instagram"],
    recurrence="monthly",
    posting_times=["10:00"],
    day_of_month=1
)
```

#### Run the Auto-Poster

```bash
# Run scheduler continuously (checks every minute)
python social_scheduler.py
```

Or run as background service on Windows:

```bash
start python social_scheduler.py
```

#### Manage Schedules

```python
# Get all schedules
schedules = await manager.get_all_schedules()

# Deactivate a schedule
await manager.deactivate_schedule(schedule_id)

# Activate a schedule
await manager.activate_schedule(schedule_id)

# Delete a schedule
await manager.delete_schedule(schedule_id)
```

---

## Feature 5: Analytics Dashboard

### Overview

Generate beautiful HTML analytics dashboards to visualize your social media performance.

### Usage Examples

#### Generate Dashboard

```python
from social_content_calendar import AnalyticsDashboardGenerator
from datetime import datetime, timedelta

generator = AnalyticsDashboardGenerator()

# Generate for last 30 days + next 30 days
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now() + timedelta(days=30)

dashboard_path = await generator.generate_dashboard(start_date, end_date)

print(f"Dashboard saved to: {dashboard_path}")
```

#### View Dashboard

Open the generated HTML file in your browser:

```bash
# Windows
start dashboards\social_analytics.html

# Or manually open the file
```

### Dashboard Features

- 📊 **Summary Statistics**: Total posts, posted, pending, cancelled
- 📱 **Platform Breakdown**: Facebook vs Instagram posts
- 📅 **Post Timeline**: Visual list of all scheduled posts
- 🎨 **Status Indicators**: Color-coded by status (posted, pending, cancelled)
- 📈 **Category Distribution**: Posts by content category

---

## 📖 API Reference

### Content Calendar Manager

```python
class ContentCalendarManager:
    async def schedule_post(message, platforms, scheduled_time, ...) -> ScheduledPost
    async def schedule_from_template(template_id, variables, scheduled_time, ...) -> ScheduledPost
    async def get_pending_posts() -> List[ScheduledPost]
    async def get_scheduled_posts(start_date, end_date) -> List[ScheduledPost]
    async def cancel_post(post_id) -> bool
    async def generate_calendar_view(year, month) -> ContentCalendar
```

### Scheduled Post Manager

```python
class ScheduledPostManager:
    async def create_recurring_schedule(template_id, variables, platforms, recurrence, ...) -> str
    async def get_all_schedules() -> List[RecurringPostSchedule]
    async def activate_schedule(schedule_id) -> bool
    async def deactivate_schedule(schedule_id) -> bool
    async def delete_schedule(schedule_id) -> bool
    async def process_schedules() -> List[Dict]  # Create posts for today
    async def post_due_content() -> List[Dict]   # Post content that's due
    async def run_scheduler(check_interval=60)   # Run continuously
```

### Post Templates Library

```python
class PostTemplatesLibrary:
    def get_all_templates() -> List[Dict]
    def get_templates_by_category(category) -> List[Dict]
    def get_template_by_id(template_id) -> Dict
    def add_custom_template(template) -> str
    def render_template(template_id, variables) -> str
```

### Hashtag Suggester

```python
class HashtagSuggester:
    def suggest_hashtags(content, category, platform, count) -> List[str]
    def get_hashtags_by_category(category, count) -> List[str]
```

### Analytics Dashboard Generator

```python
class AnalyticsDashboardGenerator:
    async def generate_dashboard(start_date, end_date) -> str  # Returns file path
```

---

## 💡 Usage Examples

### Example 1: Set Up Complete Automation

```python
import asyncio
from social_scheduler import ScheduledPostManager

async def setup_automation():
    manager = ScheduledPostManager()

    # Morning motivation (daily, 8 AM)
    await manager.create_recurring_schedule(
        template_id="template_motivation",
        variables={
            "motivational_quote": "The only limit is your mind.",
            "quote_author": "Unknown"
        },
        platforms=["facebook", "instagram"],
        recurrence="daily",
        posting_times=["08:00"],
        days_of_week=[0, 1, 2, 3, 4]
    )

    # Afternoon tip (daily, 2 PM)
    await manager.create_recurring_schedule(
        template_id="template_educational",
        variables={
            "tip_title": "Time Management",
            "tip_content": "Use time-blocking to maximize productivity."
        },
        platforms=["facebook", "instagram"],
        recurrence="daily",
        posting_times=["14:00"]
    )

    # Friday engagement (weekly, 5 PM)
    await manager.create_recurring_schedule(
        template_id="template_engagement",
        variables={
            "engagement_question": "What did you accomplish this week?"
        },
        platforms=["facebook", "instagram"],
        recurrence="weekly",
        posting_times=["17:00"],
        days_of_week=[4]
    )

    print("✅ Automation setup complete!")

asyncio.run(setup_automation())
```

### Example 2: Content Calendar for Week

```python
from social_content_calendar import ContentCalendarManager
from datetime import datetime, timedelta

async def plan_week():
    calendar = ContentCalendarManager()
    
    today = datetime.now()
    
    # Schedule posts for next 7 days
    for i in range(7):
        post_date = today + timedelta(days=i)
        
        # Morning post
        await calendar.schedule_from_template(
            template_id="template_motivation",
            variables={
                "motivational_quote": "Believe you can and you're halfway there.",
                "quote_author": "Theodore Roosevelt"
            },
            scheduled_time=post_date.replace(hour=8, minute=0),
            platforms=["facebook", "instagram"]
        )
        
        # Afternoon post
        await calendar.schedule_from_template(
            template_id="template_educational",
            variables={
                "tip_title": "Productivity Hack",
                "tip_content": "Batch similar tasks together."
            },
            scheduled_time=post_date.replace(hour=14, minute=0),
            platforms=["facebook", "instagram"]
        )
    
    print("✅ Week planned!")

asyncio.run(plan_week())
```

### Example 3: Generate Monthly Report

```python
from social_content_calendar import AnalyticsDashboardGenerator
from datetime import datetime, timedelta

async def monthly_report():
    generator = AnalyticsDashboardGenerator()
    
    # Last month
    end = datetime.now()
    start = end - timedelta(days=30)
    
    dashboard = await generator.generate_dashboard(start, end)
    
    print(f"📊 Monthly report generated: {dashboard}")
    print(f"Open in browser to view analytics")

asyncio.run(monthly_report())
```

---

## 🧪 Testing

### Run Full Test Suite

```bash
python test_advanced_social_features.py
```

### Test Individual Features

```bash
# Test content calendar
python -c "import asyncio; from social_content_calendar import ContentCalendarManager; asyncio.run(ContentCalendarManager().get_pending_posts())"

# Test scheduler demo
python social_scheduler.py --demo

# Test templates
python -c "from social_content_calendar import PostTemplatesLibrary; t = PostTemplatesLibrary(); print(t.get_all_templates()[0])"
```

---

## 🔧 Troubleshooting

### Problem: "Module not found" Error

**Solution:**
```bash
# Ensure all files are in the same directory
dir facebook_instagram_integration.py
dir social_content_calendar.py
dir social_scheduler.py
```

### Problem: Scheduler Not Posting

**Solution:**
1. Check if scheduler is running: `tasklist | findstr python`
2. Verify `SOCIAL_MOCK_MODE` setting
3. Check logs: `logs/scheduled_posts_log.md`
4. Ensure posts are scheduled for current time

### Problem: Templates Not Rendering

**Solution:**
```python
# Verify template exists
from social_content_calendar import PostTemplatesLibrary
templates = PostTemplatesLibrary()
print(templates.get_template_by_id("your_template_id"))
```

### Problem: Dashboard Not Generating

**Solution:**
```bash
# Check if dashboards directory exists
mkdir dashboards

# Check permissions
dir dashboards
```

### Problem: Recurring Schedule Not Working

**Solution:**
1. Verify schedule is active: `schedules.json`
2. Check `days_of_week` format (0=Monday, 6=Sunday)
3. Ensure `posting_times` format is "HH:MM"
4. Run scheduler: `python social_scheduler.py`

---

## 📁 Data Files Reference

### state/post_templates.json

Stores custom templates:
```json
[
  {
    "id": "custom_abc123",
    "name": "My Custom Template",
    "category": "engagement",
    "message_template": "Custom message {variable}",
    "suggested_hashtags": ["#Custom"],
    "best_posting_times": ["10:00"],
    "platforms": ["facebook", "instagram"]
  }
]
```

### state/content_calendar.json

Stores scheduled posts:
```json
[
  {
    "id": "scheduled_20260310100000_abc123",
    "message": "Post message here...",
    "platforms": ["facebook", "instagram"],
    "scheduled_time": "2026-03-11T10:00:00",
    "status": "pending",
    "hashtags": ["#Hashtag1", "#Hashtag2"],
    "created_at": "2026-03-10T12:00:00"
  }
]
```

### state/recurring_schedules.json

Stores recurring schedules:
```json
[
  {
    "id": "schedule_20260310100000",
    "template_id": "template_motivation",
    "variables": {"motivational_quote": "..."},
    "platforms": ["facebook", "instagram"],
    "recurrence": "daily",
    "posting_times": ["08:00"],
    "days_of_week": [0, 1, 2, 3, 4],
    "active": true
  }
]
```

---

## ✅ Verification Checklist

- [ ] All dependencies installed
- [ ] Basic FB/IG integration working
- [ ] Test suite passes
- [ ] Templates library loaded (10 templates)
- [ ] Can schedule posts
- [ ] Can create recurring schedules
- [ ] Scheduler runs without errors
- [ ] Dashboard generates successfully
- [ ] Logs are being written

---

## 🎉 Quick Start Commands

```bash
# 1. Test everything
python test_advanced_social_features.py

# 2. Set up default schedules
python -c "import asyncio; from social_scheduler import setup_default_schedules; asyncio.run(setup_default_schedules())"

# 3. Run scheduler
python social_scheduler.py

# 4. Generate dashboard
python -c "import asyncio; from social_content_calendar import AnalyticsDashboardGenerator; from datetime import datetime, timedelta; asyncio.run(AnalyticsDashboardGenerator().generate_dashboard(datetime.now()-timedelta(days=30), datetime.now()+timedelta(days=30)))"

# 5. View dashboard
start dashboards\social_analytics.html
```

---

## 📚 Additional Resources

- **Basic Integration Docs**: `FACEBOOK_INSTAGRAM_INTEGRATION.md`
- **MCP Server**: `social_mcp_server_v2.py`
- **Meta Graph API**: https://developers.facebook.com/docs/graph-api
- **Instagram API**: https://developers.facebook.com/docs/instagram-api

---

**🎊 Congratulations!** Your advanced social media automation is ready to use!
