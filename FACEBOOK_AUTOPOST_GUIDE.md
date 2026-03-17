# 📘 Facebook Auto-Post - Quick Start Guide

**Status:** ✅ Ready to Use | **Created:** 2026-03-11

---

## 🎯 Overview

Your Facebook auto-posting system is now ready! You have three options:

1. **Post Immediately** - Publish a post right now
2. **Schedule Recurring Posts** - Set up automation (daily/weekly/monthly)
3. **Run Scheduler** - Execute scheduled posts automatically

---

## 🚀 Quick Start

### Option 1: Using the Batch File (Easiest)

Double-click `facebook_autopost.bat` and select your action:
- **1** - Post to Facebook NOW
- **2** - Setup auto-post schedules
- **3** - Start scheduler (background)
- **4** - Check scheduled posts
- **5** - Test connection

### Option 2: Using Python Commands

#### Post Immediately
```bash
python autopost_facebook.py
```

#### Setup Recurring Schedules
```bash
python setup_autopost_schedules.py
```

#### Start Auto-Scheduler
```bash
python social_scheduler.py
```

Or run as background service:
```bash
start python social_scheduler.py
```

---

## 📋 What's Configured

### Facebook Page Details
- **Page ID:** 61585659193997
- **Access Token:** ✅ Configured
- **Mock Mode:** ❌ Disabled (LIVE posting)

### Available Templates
1. **Company Announcement** - For news and updates
2. **Product Promotion** - For special offers
3. **Engagement Question** - For audience interaction
4. **Educational Tip** - For sharing knowledge
5. **Behind the Scenes** - For authentic content
6. **Customer Testimonial** - For social proof
7. **Event Announcement** - For upcoming events
8. **Motivational Quote** - For inspiration
9. **Product Launch** - For new releases
10. **Friday Fun** - For weekend engagement

---

## 📅 Default Auto-Post Schedule

When you run `setup_autopost_schedules.py`, these schedules are created:

| Frequency | Time | Content Type |
|-----------|------|--------------|
| Mon-Fri | 8:00 AM | Motivational Quote |
| Daily | 2:00 PM | Educational Tip |
| Friday | 5:00 PM | Engagement Question |
| Saturday | 11:00 AM | Weekend Fun |
| 1st of Month | 10:00 AM | Monthly Update |

---

## 🔧 Customization

### Edit Auto-Post Messages

Open `state/recurring_schedules.json` and modify the `variables` section:

```json
{
  "template_id": "template_motivation",
  "variables": {
    "motivational_quote": "Your custom quote here",
    "quote_author": "Author name"
  }
}
```

### Change Posting Times

Edit the `posting_times` array in `state/recurring_schedules.json`:

```json
{
  "posting_times": ["09:00", "15:00"]  // 9 AM and 3 PM
}
```

### Customize Immediate Posts

Edit `autopost_facebook.py` and change the `MESSAGE` variable:

```python
MESSAGE = """Your custom message here!

#YourHashtags"""
```

---

## 📊 Monitoring

### View Scheduled Posts
```bash
python -c "import asyncio; from social_content_calendar import ContentCalendarManager; posts = asyncio.run(ContentCalendarManager().get_pending_posts()); print(f'Pending: {len(posts)}')"
```

### View Logs
- **Scheduler Log:** `logs/scheduled_posts_log.md`
- **State Files:** `state/recurring_schedules.json`

### Check Facebook
Visit your Facebook Page to see published posts:
https://www.facebook.com/61585659193997

---

## 🎨 Example: Custom Post Right Now

Edit `autopost_facebook.py`:

```python
MESSAGE = """🎉 Special Announcement!

We're excited to share our latest updates with you!

✨ New features:
• Auto-posting automation
• Smart scheduling
• Advanced analytics

Try it now! 🚀

#AI #Automation #Productivity"""

IMAGE_URL = "https://example.com/your-image.jpg"  # Optional
LINK = "https://yourwebsite.com"  # Optional
```

Then run:
```bash
python autopost_facebook.py
```

---

## 🔍 Troubleshooting

### Post Not Appearing on Facebook

**Check:**
1. Is `SOCIAL_MOCK_MODE=false` in `.env`?
2. Is Facebook Page Access Token valid?
3. Does token have `pages_manage_posts` permission?

**Test connection:**
```bash
python -c "import asyncio; from facebook_instagram_integration import FacebookInstagramIntegration; int = FacebookInstagramIntegration(mock_mode=False); result = asyncio.run(int.post_to_facebook('Test')); print(result)"
```

### Scheduler Not Posting

**Check:**
1. Is scheduler running? `tasklist | findstr python`
2. Are schedules active? Check `state/recurring_schedules.json`
3. Review logs: `logs/scheduled_posts_log.md`

**Restart scheduler:**
```bash
taskkill /F /IM python.exe
start python social_scheduler.py
```

### Token Expired

**Get new token:**
1. Go to https://developers.facebook.com/tools/explorer/
2. Select your app
3. Generate Page Access Token
4. Update `.env`: `FACEBOOK_PAGE_ACCESS_TOKEN=new_token`

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `autopost_facebook.py` | Immediate posting script |
| `setup_autopost_schedules.py` | Schedule setup wizard |
| `facebook_autopost.bat` | Windows quick-start menu |
| `FACEBOOK_AUTOPOST_GUIDE.md` | This documentation |

### Existing Files Used

| File | Purpose |
|------|---------|
| `facebook_instagram_integration.py` | Core Facebook API |
| `social_scheduler.py` | Auto-posting engine |
| `social_content_calendar.py` | Content management |
| `state/recurring_schedules.json` | Schedule storage |
| `state/content_calendar.json` | Pending posts |

---

## ✅ Verification Checklist

Before posting live:

- [ ] Facebook Page Access Token is valid
- [ ] `SOCIAL_MOCK_MODE=false` in `.env`
- [ ] Token has `pages_manage_posts` permission
- [ ] Facebook Page ID is correct (61585659193997)
- [ ] Test post successful (use option 5 in batch file)

---

## 🎯 Next Steps

### 1. Test Connection (Recommended First)
```bash
facebook_autopost.bat
# Select option 5
```

### 2. Post Something Simple
```bash
facebook_autopost.bat
# Select option 1
```

### 3. Set Up Automation
```bash
facebook_autopost.bat
# Select option 2
```

### 4. Start Scheduler
```bash
facebook_autopost.bat
# Select option 3
```

---

## 💡 Pro Tips

1. **Best Posting Times:**
   - Morning: 8-9 AM (commute time)
   - Lunch: 12-2 PM (break time)
   - Evening: 5-7 PM (after work)

2. **Content Mix:**
   - 40% Educational/Value
   - 30% Engagement/Questions
   - 20% Entertainment/Fun
   - 10% Promotional

3. **Hashtag Strategy:**
   - Use 3-5 hashtags on Facebook
   - Mix popular and niche tags
   - Create branded hashtags

4. **Monitor Performance:**
   - Check Facebook Insights weekly
   - Adjust posting times based on engagement
   - Track which content types perform best

---

## 📞 Support

**Documentation:**
- `ADVANCED_SOCIAL_FEATURES.md` - Full feature guide
- `FACEBOOK_INSTAGRAM_INTEGRATION.md` - API details

**Meta Developer Resources:**
- Graph API: https://developers.facebook.com/docs/graph-api
- Facebook Login: https://developers.facebook.com/docs/facebook-login

---

**🎊 Ready to start auto-posting!** Run `facebook_autopost.bat` to begin.
