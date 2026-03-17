"""
Facebook Scheduled Auto-Post

Schedule posts to be published at specific times.
Supports one-time scheduling and recurring schedules.

Usage:
    # Schedule a post for specific time
    python facebook_autopost_schedule.py --date "2026-03-12" --time "09:00" --template 1
    
    # Schedule recurring posts
    python facebook_autopost_schedule.py --recurring daily --time "09:00" --template 2
"""

import asyncio
import sys
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from facebook_instagram_integration import FacebookInstagramIntegration


# State directory for storing schedules
STATE_DIR = Path("state")
SCHEDULES_FILE = STATE_DIR / "facebook_schedules.json"


def ensure_state_dir():
    """Ensure state directory exists"""
    STATE_DIR.mkdir(exist_ok=True)


def load_schedules():
    """Load existing schedules"""
    if SCHEDULES_FILE.exists():
        with open(SCHEDULES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"scheduled_posts": [], "recurring_schedules": []}


def save_schedules(schedules):
    """Save schedules to file"""
    ensure_state_dir()
    with open(SCHEDULES_FILE, 'w', encoding='utf-8') as f:
        json.dump(schedules, f, indent=2, ensure_ascii=False)


# ============== PRE-DEFINED POST TEMPLATES ==============

TEMPLATES = {
    1: {
        "name": "🎉 Product Announcement",
        "message": """🎉 Exciting News from AI Employee Vault!

We're thrilled to announce our latest AI-powered automation features:

✨ Auto-posting to social media
✨ Smart content scheduling  
✨ Advanced analytics & insights

Boost your productivity today! 🚀

#AIAutomation #Productivity #TechInnovation #BusinessGrowth #AI""",
        "link": "https://example.com"
    },
    
    2: {
        "name": "💼 Business Tips",
        "message": """💡 Business Tip of the Day!

Did you know? Automating repetitive tasks can save up to 40% of your work time!

Start automating today and focus on what matters! 📈

#BusinessTips #Automation #AI #Entrepreneurship #Growth""",
        "link": None
    },
    
    3: {
        "name": "🌟 Motivational Post",
        "message": """🌟 Monday Motivation!

"The best way to predict the future is to create it." - Peter Drucker

Make today count! What's your goal for this week?

#Motivation #MondayMotivation #Success #Goals #AI""",
        "link": None
    },
    
    4: {
        "name": "📊 Industry Insights",
        "message": """📊 Industry Insight 2026!

📈 73% of businesses now use some form of automation
💰 Average ROI: 300% in first year
⏰ Time saved: 15-20 hours/week per employee

Is your business ready for the AI revolution?

#IndustryInsights #AI #BusinessTrends #Automation""",
        "link": "https://example.com"
    },
    
    5: {
        "name": "🎯 Customer Success",
        "message": """🎯 Customer Success Story!

"Since implementing AI Employee Vault, we've reduced manual work by 60% and increased engagement by 250%!"

Ready to transform your business?

#CustomerSuccess #CaseStudy #AI #BusinessGrowth""",
        "link": None
    },
    
    6: {
        "name": "🔧 Feature Highlight",
        "message": """🔧 Feature Spotlight!

AI Employee Vault can:
✅ Auto-post to Facebook, Instagram & LinkedIn
✅ Generate performance summaries
✅ Schedule posts at optimal times

One tool, endless possibilities! 🚀

#Features #AITools #Productivity #SocialMedia""",
        "link": "https://example.com"
    },
    
    7: {
        "name": "📚 Educational Content",
        "message": """📚 Learn Something New!

5 Ways AI Can Transform Your Business:

1️⃣ Automate customer support
2️⃣ Analyze data instantly
3️⃣ Personalize marketing
4️⃣ Streamline operations
5️⃣ Predict trends

Which one will you implement first?

#Education #AI #Business #Learning""",
        "link": None
    },
    
    8: {
        "name": "🎊 Special Offer",
        "message": """🎊 Limited Time Offer!

Get started with AI Employee Vault today!

🎁 Full access to all features
🎁 Priority support
🎁 Free setup assistance

Don't miss out! ⏰

#SpecialOffer #Deal #AI #Business""",
        "link": "https://example.com"
    }
}


async def schedule_post(date_str: str, time_str: str, template_id: int, 
                        custom_message: str = None, image_url: str = None, 
                        link: str = None):
    """Schedule a post for specific date and time"""
    
    print("=" * 80)
    print("  📘 FACEBOOK POST SCHEDULER")
    print("=" * 80)
    
    # Parse date and time
    try:
        scheduled_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError as e:
        print(f"❌ Invalid date/time format. Use YYYY-MM-DD and HH:MM")
        return None
    
    # Check if date is in the past
    if scheduled_datetime < datetime.now():
        print(f"❌ Scheduled time is in the past! Please choose a future time.")
        return None
    
    # Get template
    if custom_message:
        message = custom_message
        template_name = "Custom Message"
    elif template_id in TEMPLATES:
        template = TEMPLATES[template_id]
        message = template["message"]
        template_name = template["name"]
        if link is None:
            link = template["link"]
    else:
        print(f"❌ Invalid template ID. Use 1-8")
        return None
    
    # Create schedule entry
    schedule_entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "scheduled_time": scheduled_datetime.isoformat(),
        "template_id": template_id,
        "template_name": template_name,
        "message": message,
        "image_url": image_url,
        "link": link,
        "status": "scheduled",
        "created_at": datetime.now().isoformat()
    }
    
    # Load existing schedules and add new one
    schedules = load_schedules()
    schedules["scheduled_posts"].append(schedule_entry)
    save_schedules(schedules)
    
    print(f"\n✅ POST SCHEDULED SUCCESSFULLY!")
    print("=" * 80)
    print(f"  📅 Scheduled Date: {scheduled_datetime.strftime('%Y-%m-%d')}")
    print(f"  ⏰ Scheduled Time: {scheduled_datetime.strftime('%H:%M')}")
    print(f"  📝 Template: {template_name}")
    print(f"  🆔 Schedule ID: {schedule_entry['id']}")
    print("=" * 80)
    
    print(f"\n📄 Message Preview:")
    print("-" * 80)
    print(message[:200] + "..." if len(message) > 200 else message)
    print("-" * 80)
    
    print(f"\n💡 To execute scheduled posts, run:")
    print(f"   python social_scheduler.py")
    print(f"\n📋 View all scheduled posts:")
    print(f"   python facebook_autopost_schedule.py --list")
    
    return schedule_entry


async def schedule_recurring(frequency: str, time_str: str, template_id: int,
                             custom_message: str = None, link: str = None):
    """Schedule recurring posts"""
    
    print("=" * 80)
    print("  📘 FACEBOOK RECURRING POST SCHEDULER")
    print("=" * 80)
    
    # Get template
    if custom_message:
        message = custom_message
        template_name = "Custom Message"
    elif template_id in TEMPLATES:
        template = TEMPLATES[template_id]
        message = template["message"]
        template_name = template["name"]
        if link is None:
            link = template["link"]
    else:
        print(f"❌ Invalid template ID. Use 1-8")
        return None
    
    # Create recurring schedule
    recurring_schedule = {
        "id": f"recurring_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "frequency": frequency,
        "time": time_str,
        "template_id": template_id,
        "template_name": template_name,
        "message": message,
        "link": link,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "last_posted": None,
        "next_post": None
    }
    
    # Calculate next post time
    now = datetime.now()
    hour, minute = map(int, time_str.split(':'))
    
    if frequency == "daily":
        next_post = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_post <= now:
            next_post += timedelta(days=1)
    elif frequency == "weekly":
        # Post every Monday
        days_until_monday = (7 - now.weekday()) % 7
        if days_until_monday == 0 and now.hour > hour:
            days_until_monday = 7
        next_post = now + timedelta(days=days_until_monday)
        next_post = next_post.replace(hour=hour, minute=minute, second=0, microsecond=0)
    elif frequency == "biweekly":
        # Post every 2 weeks on Monday
        days_until_monday = (7 - now.weekday()) % 7
        next_post = now + timedelta(days=days_until_monday)
        next_post = next_post.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    recurring_schedule["next_post"] = next_post.isoformat()
    
    # Load existing schedules and add new one
    schedules = load_schedules()
    schedules["recurring_schedules"].append(recurring_schedule)
    save_schedules(schedules)
    
    print(f"\n✅ RECURRING SCHEDULE CREATED!")
    print("=" * 80)
    print(f"  📅 Frequency: {frequency.capitalize()}")
    print(f"  ⏰ Time: {time_str}")
    print(f"  📝 Template: {template_name}")
    print(f"  🆔 Schedule ID: {recurring_schedule['id']}")
    print(f"  📅 Next Post: {next_post.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 80)
    
    print(f"\n💡 To execute scheduled posts, run:")
    print(f"   python social_scheduler.py")
    
    return recurring_schedule


def list_schedules():
    """List all scheduled posts"""
    
    print("=" * 80)
    print("  📘 SCHEDULED FACEBOOK POSTS")
    print("=" * 80)
    
    schedules = load_schedules()
    
    # Show one-time scheduled posts
    print(f"\n📅 ONE-TIME SCHEDULED POSTS ({len(schedules['scheduled_posts'])})")
    print("-" * 80)
    
    if schedules["scheduled_posts"]:
        for post in schedules["scheduled_posts"]:
            status_icon = "✅" if post["status"] == "scheduled" else "⏸️"
            print(f"  {status_icon} ID: {post['id']}")
            print(f"     📅 Time: {post['scheduled_time']}")
            print(f"     📝 Template: {post['template_name']}")
            print(f"     📊 Status: {post['status']}")
            print()
    else:
        print("  No one-time scheduled posts")
    
    # Show recurring schedules
    print(f"\n🔄 RECURRING SCHEDULES ({len(schedules['recurring_schedules'])})")
    print("-" * 80)
    
    if schedules["recurring_schedules"]:
        for schedule in schedules["recurring_schedules"]:
            status_icon = "✅" if schedule["status"] == "active" else "⏸️"
            print(f"  {status_icon} ID: {schedule['id']}")
            print(f"     📅 Frequency: {schedule['frequency']}")
            print(f"     ⏰ Time: {schedule['time']}")
            print(f"     📝 Template: {schedule['template_name']}")
            print(f"     📅 Next Post: {schedule['next_post']}")
            print()
    else:
        print("  No recurring schedules")
    
    print("=" * 80)


async def main():
    """Main function with argument parsing"""
    
    parser = argparse.ArgumentParser(description='Facebook Scheduled Auto-Post')
    parser.add_argument('--date', '-d', type=str, help='Date (YYYY-MM-DD)')
    parser.add_argument('--time', '-t', type=str, help='Time (HH:MM)')
    parser.add_argument('--template', type=int, choices=range(1, 9), help='Template ID (1-8)')
    parser.add_argument('--message', '-m', type=str, help='Custom message')
    parser.add_argument('--image', '-i', type=str, help='Image URL')
    parser.add_argument('--link', '-l', type=str, help='Link URL')
    parser.add_argument('--recurring', '-r', type=str, choices=['daily', 'weekly', 'biweekly'],
                        help='Recurring frequency')
    parser.add_argument('--list', action='store_true', help='List all scheduled posts')
    
    args = parser.parse_args()
    
    # List schedules
    if args.list:
        list_schedules()
        sys.exit(0)
    
    # Schedule recurring post
    if args.recurring:
        if not args.time or not args.template:
            print("❌ Recurring posts require --time and --template")
            sys.exit(1)
        
        result = await schedule_recurring(
            frequency=args.recurring,
            time_str=args.time,
            template_id=args.template,
            custom_message=args.message,
            link=args.link
        )
        sys.exit(0 if result else 1)
    
    # Schedule one-time post
    if args.date and args.time and args.template:
        result = await schedule_post(
            date_str=args.date,
            time_str=args.time,
            template_id=args.template,
            custom_message=args.message,
            image_url=args.image,
            link=args.link
        )
        sys.exit(0 if result else 1)
    
    # If no arguments, show help
    parser.print_help()
    
    print("\n" + "=" * 80)
    print("  EXAMPLES:")
    print("=" * 80)
    print("  # Schedule for specific time")
    print("  python facebook_autopost_schedule.py -d 2026-03-12 -t 09:00 -t 1")
    print()
    print("  # Schedule daily recurring post")
    print("  python facebook_autopost_schedule.py --recurring daily -t 09:00 -t 2")
    print()
    print("  # List all scheduled posts")
    print("  python facebook_autopost_schedule.py --list")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
