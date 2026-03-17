# 🚀 SOCIAL MEDIA ADVANCED FEATURES - QUICK START

**Complete Facebook & Instagram Integration with Automation**

---

## ⚡ 1-Minute Setup

```bash
# 1. Test everything works
python test_advanced_social_features.py

# 2. Set up default automation schedules
python -c "import asyncio; from social_scheduler import setup_default_schedules; asyncio.run(setup_default_schedules())"

# 3. Start auto-posting scheduler
python social_scheduler.py
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `facebook_instagram_integration.py` | Core FB/IG posting & analytics |
| `social_content_calendar.py` | Templates, calendar, hashtags |
| `social_scheduler.py` | Auto-posting scheduler |
| `social_mcp_server_v2.py` | API server (http://localhost:8002) |
| `test_advanced_social_features.py` | Test suite |
| `ADVANCED_SOCIAL_FEATURES.md` | Full documentation |

---

## 🎯 Key Features

### 1. **10 Pre-built Post Templates**
- Company announcements
- Promotions & offers
- Engagement questions
- Educational tips
- Behind the scenes
- Customer testimonials
- Event announcements
- Motivational quotes
- Product launches
- Friday fun posts

### 2. **Smart Hashtag Suggestions**
Auto-suggests relevant hashtags based on content analysis.

### 3. **Content Calendar**
Schedule and visualize all posts in one place.

### 4. **Recurring Post Schedules**
- **Daily**: Post every day at specific times
- **Weekly**: Post on specific days (e.g., Mon/Wed/Fri)
- **Monthly**: Post on specific dates (e.g., 1st of month)

### 5. **Auto-Posting**
Set it and forget it - posts automatically at scheduled times.

### 6. **Analytics Dashboard**
Beautiful HTML reports with engagement metrics.

---

## 💻 Quick Commands

### Post to Facebook & Instagram

```bash
# Via API (server must be running)
curl -X POST "http://localhost:8002/api/post_message" ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"both\", \"message\": \"Hello World! 🚀\"}"
```

### Schedule a Post

```python
from social_content_calendar import ContentCalendarManager
from datetime import datetime, timedelta

async def schedule():
    calendar = ContentCalendarManager()
    tomorrow = datetime.now() + timedelta(days=1)
    
    await calendar.schedule_post(
        message="🎉 Exciting news coming soon!",
        platforms=["facebook", "instagram"],
        scheduled_time=tomorrow.replace(hour=10, minute=0)
    )

# Run: python -c "import asyncio; asyncio.run(schedule())"
```

### Create Recurring Schedule

```python
from social_scheduler import ScheduledPostManager

async def create_schedule():
    manager = ScheduledPostManager()
    
    # Daily motivation (weekdays at 8 AM)
    await manager.create_recurring_schedule(
        template_id="template_motivation",
        variables={
            "motivational_quote": "Believe you can!",
            "quote_author": "Unknown"
        },
        platforms=["facebook", "instagram"],
        recurrence="daily",
        posting_times=["08:00"],
        days_of_week=[0, 1, 2, 3, 4]
    )

# Run: python -c "import asyncio; asyncio.run(create_schedule())"
```

### Generate Analytics Dashboard

```bash
python -c "import asyncio; from social_content_calendar import AnalyticsDashboardGenerator; from datetime import datetime, timedelta; asyncio.run(AnalyticsDashboardGenerator().generate_dashboard(datetime.now()-timedelta(days=30), datetime.now()+timedelta(days=30)))"
```

Then open: `dashboards\social_analytics.html`

---

## 🔧 Configuration (.env)

```bash
# Facebook
FACEBOOK_PAGE_ACCESS_TOKEN=your_token_here
FACEBOOK_PAGE_ID=1496288429174042

# Instagram
INSTAGRAM_USER_ID=your_ig_id
INSTAGRAM_ACCESS_TOKEN=your_ig_token

# Mock Mode (true=test, false=live)
SOCIAL_MOCK_MODE=true
```

---

## 📊 API Endpoints

Start server: `python social_mcp_server_v2.py`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/post_message` | POST | Post to FB/IG |
| `/api/get_metrics` | POST | Get engagement metrics |
| `/api/generate_summary` | POST | Generate performance summary |
| `/api/get_summary` | GET | Get summary (query param) |

**API Docs:** http://localhost:8002/docs

---

## 🧪 Testing

```bash
# Full test suite
python test_advanced_social_features.py

# Test basic FB/IG integration
python test_facebook_instagram.py

# Scheduler demo
python social_scheduler.py --demo
```

---

## 📈 Usage Workflow

### Option 1: Manual Posting

```bash
# 1. Start API server
python social_mcp_server_v2.py

# 2. Post via API
curl -X POST "http://localhost:8002/api/post_message" ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"both\", \"message\": \"My post!\"}"

# 3. View analytics
curl "http://localhost:8002/api/get_summary?platform=both"
```

### Option 2: Automated Posting

```bash
# 1. Set up schedules (one-time)
python -c "import asyncio; from social_scheduler import setup_default_schedules; asyncio.run(setup_default_schedules())"

# 2. Run scheduler continuously
python social_scheduler.py

# Or run in background (Windows)
start python social_scheduler.py
```

---

## 🎨 Template Variables

When using templates, replace variables like `{variable_name}`:

```python
# Template: template_promotion
{
    "product_name": "AI Employee Vault",
    "offer_details": "50% off first month",
    "expiry_date": "March 31, 2026",
    "call_to_action": "Sign up now!"
}

# Template: template_motivation
{
    "motivational_quote": "Success is not final...",
    "quote_author": "Winston Churchill"
}

# Template: template_engagement
{
    "engagement_question": "What's your favorite tool?"
}
```

---

## 🔍 Monitoring

### Check Scheduled Posts
```bash
# View pending posts
python -c "import asyncio; from social_content_calendar import ContentCalendarManager; posts = asyncio.run(ContentCalendarManager().get_pending_posts()); print(f'{len(posts)} pending posts')"
```

### View Logs
- **Scheduled posts**: `logs/scheduled_posts_log.md`
- **API requests**: `social_log.md`

### View Dashboard
```bash
start dashboards\social_analytics.html
```

---

## ⚠️ Important Notes

1. **Mock Mode**: By default `SOCIAL_MOCK_MODE=true` - no real posts are made
2. **Live Posting**: Set `SOCIAL_MOCK_MODE=false` in `.env` for real posts
3. **Instagram**: Requires Business Account + Facebook Page connection
4. **Rate Limits**: Facebook/Instagram have API rate limits (200 requests/hour)
5. **Scheduler**: Keep `social_scheduler.py` running for auto-posting

---

## 🆘 Troubleshooting

**Problem**: Tests fail
```bash
# Install dependencies
pip install fastapi uvicorn httpx python-dotenv pydantic aiofiles
```

**Problem**: Instagram not working
- Convert to Business Account in Instagram Settings
- Connect to Facebook Page
- Get Instagram User ID: `python get_instagram_id.py`

**Problem**: Scheduler not posting
- Ensure scheduler is running: `tasklist | findstr python`
- Check schedule is active in `state/recurring_schedules.json`
- Verify post times match current time

---

## 📚 Documentation

- **Full Guide**: `ADVANCED_SOCIAL_FEATURES.md`
- **Basic Integration**: `FACEBOOK_INSTAGRAM_INTEGRATION.md`
- **API Docs**: http://localhost:8002/docs

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Tests passing (`python test_advanced_social_features.py`)
- [ ] Templates loaded (10 templates)
- [ ] Schedules created
- [ ] Scheduler running
- [ ] Dashboard generated
- [ ] Can post manually
- [ ] Auto-posting working

---

**🎉 You're ready to automate your social media!**

For detailed documentation, see `ADVANCED_SOCIAL_FEATURES.md`
