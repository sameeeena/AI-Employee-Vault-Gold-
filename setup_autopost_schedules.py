"""
Setup Auto-Post Schedules for Facebook

Creates recurring posting schedules for automated content.
Run this once to set up your automation, then run social_scheduler.py to execute.

Usage:
    python setup_autopost_schedules.py
"""

import asyncio
import json
import os
from datetime import datetime
from social_scheduler import ScheduledPostManager


async def setup_schedules():
    """Set up recurring auto-post schedules"""
    
    print("=" * 80)
    print("  📅 SETTING UP FACEBOOK AUTO-POST SCHEDULES")
    print("=" * 80)
    
    manager = ScheduledPostManager()
    
    # Check existing schedules
    existing = await manager.get_all_schedules()
    if existing:
        print(f"\n⚠️  Found {len(existing)} existing schedule(s)")
        for schedule in existing:
            status = "✅ Active" if schedule.active else "⏸️ Inactive"
            print(f"   - {schedule.id}: {status}")
        
        response = input("\nDo you want to add more schedules? (y/n): ").strip().lower()
        if response != 'y':
            print("\n👍 Existing schedules kept. Run social_scheduler.py to start auto-posting.")
            return
    
    print("\n📋 Creating default auto-post schedules...\n")
    
    # Schedule 1: Daily Motivation (Monday-Friday at 8 AM)
    print("1️⃣  Creating: Daily Motivation Post (Mon-Fri, 8:00 AM)")
    motivation_id = await manager.create_recurring_schedule(
        template_id="template_motivation",
        variables={
            "motivational_quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "quote_author": "Winston Churchill"
        },
        platforms=["facebook"],
        recurrence="daily",
        posting_times=["08:00"],
        days_of_week=[0, 1, 2, 3, 4]  # Monday-Friday
    )
    print(f"   ✅ Created: {motivation_id}")
    
    # Schedule 2: Daily Tip (Every day at 2 PM)
    print("\n2️⃣  Creating: Daily Educational Tip (Daily, 2:00 PM)")
    tip_id = await manager.create_recurring_schedule(
        template_id="template_educational",
        variables={
            "tip_title": "Productivity Hack",
            "tip_content": "Use the 2-minute rule: If something takes less than 2 minutes, do it immediately!"
        },
        platforms=["facebook"],
        recurrence="daily",
        posting_times=["14:00"]
    )
    print(f"   ✅ Created: {tip_id}")
    
    # Schedule 3: Friday Engagement (Friday at 5 PM)
    print("\n3️⃣  Creating: Friday Engagement Post (Friday, 5:00 PM)")
    friday_id = await manager.create_recurring_schedule(
        template_id="template_engagement",
        variables={
            "engagement_question": "What was your biggest win this week? Share below! 👇"
        },
        platforms=["facebook"],
        recurrence="weekly",
        posting_times=["17:00"],
        days_of_week=[4]  # Friday
    )
    print(f"   ✅ Created: {friday_id}")
    
    # Schedule 4: Weekend Fun (Saturday at 11 AM)
    print("\n4️⃣  Creating: Weekend Fun Post (Saturday, 11:00 AM)")
    weekend_id = await manager.create_recurring_schedule(
        template_id="template_friday_fun",
        variables={
            "friday_content": "Weekend vibes! Time to relax and recharge. What are your plans? 🎉"
        },
        platforms=["facebook"],
        recurrence="weekly",
        posting_times=["11:00"],
        days_of_week=[5]  # Saturday
    )
    print(f"   ✅ Created: {weekend_id}")
    
    # Schedule 5: Monthly Update (1st of every month at 10 AM)
    print("\n5️⃣  Creating: Monthly Update (1st of month, 10:00 AM)")
    monthly_id = await manager.create_recurring_schedule(
        template_id="template_announcement",
        variables={
            "announcement_title": "Monthly Update",
            "announcement_details": "Check out what we accomplished this month! Stay tuned for more updates.",
            "call_to_action": "Follow us for more!"
        },
        platforms=["facebook"],
        recurrence="monthly",
        posting_times=["10:00"],
        day_of_month=1
    )
    print(f"   ✅ Created: {monthly_id}")
    
    # Display summary
    print("\n" + "=" * 80)
    print("  ✅ SCHEDULE SETUP COMPLETE!")
    print("=" * 80)
    print("\n📊 Your Auto-Post Schedule:")
    print("   • Mon-Fri 8:00 AM  - Motivation Quote")
    print("   • Daily 2:00 PM    - Educational Tip")
    print("   • Friday 5:00 PM   - Engagement Question")
    print("   • Saturday 11:00 AM - Weekend Fun")
    print("   • 1st of Month 10:00 AM - Monthly Update")
    
    print("\n📝 Next Steps:")
    print("   1. Review schedules in: state/recurring_schedules.json")
    print("   2. Start the scheduler: python social_scheduler.py")
    print("   3. Or run as background: start python social_scheduler.py")
    
    print("\n💡 Tip: Edit variables in state/recurring_schedules.json to customize messages")
    print("=" * 80)


async def custom_schedule():
    """Create a custom schedule based on user input"""
    
    print("\n" + "=" * 80)
    print("  🎨 CREATE CUSTOM AUTO-POST SCHEDULE")
    print("=" * 80)
    
    manager = ScheduledPostManager()
    
    # Get template choice
    templates_lib = manager.templates_library
    
    print("\nAvailable templates:")
    all_templates = templates_lib.get_all_templates()
    for i, template in enumerate(all_templates, 1):
        print(f"   {i}. {template['name']} ({template['category']})")
    
    try:
        choice = input("\nSelect template number (or 0 to skip): ").strip()
        if choice == "0":
            print("⏭️  Skipping custom schedule creation")
            return
        
        template_index = int(choice) - 1
        if 0 <= template_index < len(all_templates):
            selected_template = all_templates[template_index]
        else:
            print("❌ Invalid selection")
            return
    except ValueError:
        print("❌ Invalid input")
        return
    
    # Get posting frequency
    print("\nPosting frequency:")
    print("   1. Daily")
    print("   2. Weekly (specific days)")
    print("   3. Monthly (specific date)")
    
    freq = input("Select frequency (1-3): ").strip()
    
    if freq == "1":
        recurrence = "daily"
        days_of_week = None
        day_of_month = None
        times = input("Posting time (HH:MM, e.g., 09:00): ").strip() or "09:00"
        posting_times = [times]
        
    elif freq == "2":
        recurrence = "weekly"
        day_of_month = None
        print("Select days (comma-separated, 0=Mon, 6=Sun): ")
        print("   Example: 0,1,2,3,4 for weekdays")
        days_input = input("Days: ").strip() or "0,1,2,3,4"
        days_of_week = [int(d.strip()) for d in days_input.split(",")]
        times = input("Posting time (HH:MM): ").strip() or "09:00"
        posting_times = [times]
        
    elif freq == "3":
        recurrence = "monthly"
        days_of_week = None
        day_input = input("Day of month (1-31): ").strip() or "1"
        day_of_month = int(day_input)
        times = input("Posting time (HH:MM): ").strip() or "10:00"
        posting_times = [times]
    else:
        print("❌ Invalid frequency")
        return
    
    # Get platforms
    print("\nPlatforms:")
    print("   1. Facebook only")
    print("   2. Instagram only")
    print("   3. Both")
    
    platform_choice = input("Select (1-3): ").strip() or "1"
    if platform_choice == "1":
        platforms = ["facebook"]
    elif platform_choice == "2":
        platforms = ["instagram"]
    else:
        platforms = ["facebook", "instagram"]
    
    # Get custom variables
    print("\nCustomize message variables:")
    variables = {}
    template_vars = selected_template.get("message_template", "").split("{")[1:]
    
    for var in template_vars:
        var_name = var.split("}")[0]
        value = input(f"  {var_name}: ").strip()
        if value:
            variables[var_name] = value
    
    # Create schedule
    print("\n⏳ Creating schedule...")
    
    schedule_id = await manager.create_recurring_schedule(
        template_id=selected_template["id"],
        variables=variables or selected_template.get("default_variables", {}),
        platforms=platforms,
        recurrence=recurrence,
        posting_times=posting_times,
        days_of_week=days_of_week,
        day_of_month=day_of_month
    )
    
    print(f"\n✅ Schedule created: {schedule_id}")
    print("\n💡 Run 'python social_scheduler.py' to start auto-posting")


async def main():
    """Main function"""
    
    print("\nSelect mode:")
    print("   1. Setup default schedules (recommended for first time)")
    print("   2. Create custom schedule")
    
    choice = input("\nYour choice (1-2): ").strip()
    
    if choice == "1":
        await setup_schedules()
    elif choice == "2":
        await custom_schedule()
    else:
        print("❌ Invalid choice. Run again and select 1 or 2.")


if __name__ == "__main__":
    asyncio.run(main())
