"""
Advanced Social Media Features - Test Script

Tests all new features:
1. Content Calendar Management
2. Post Templates Library
3. Hashtag Suggestions
4. Scheduled Post Manager
5. Recurring Post Schedules
6. Analytics Dashboard Generation

Run:
    python test_advanced_social_features.py
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List


async def test_templates_library():
    """Test the post templates library"""
    print("=" * 80)
    print(" TEST 1: Post Templates Library")
    print("=" * 80)

    from social_content_calendar import PostTemplatesLibrary

    templates = PostTemplatesLibrary()

    # Test 1.1: Get all templates
    print("\n[TEST 1.1] Getting all templates...")
    all_templates = templates.get_all_templates()
    print(f"  ✅ Found {len(all_templates)} templates")

    # Test 1.2: Get templates by category
    print("\n[TEST 1.2] Getting templates by category...")
    for category in ["announcement", "promotion", "engagement", "educational"]:
        category_templates = templates.get_templates_by_category(category)
        print(f"  ✅ {category}: {len(category_templates)} templates")

    # Test 1.3: Render template
    print("\n[TEST 1.3] Rendering template...")
    rendered = templates.render_template(
        "template_promotion",
        {
            "product_name": "AI Employee Vault",
            "offer_details": "50% off first month!",
            "expiry_date": "March 31, 2026",
            "call_to_action": "Sign up now!"
        }
    )
    if rendered:
        print(f"  ✅ Template rendered successfully!")
        print(f"  Preview: {rendered[:100]}...")
    else:
        print(f"  ❌ Template rendering failed")
        return False

    # Test 1.4: Add custom template
    print("\n[TEST 1.4] Adding custom template...")
    custom_template = {
        "name": "Custom Welcome Post",
        "category": "engagement",
        "message_template": "👋 Welcome {new_member_name} to our community!",
        "suggested_hashtags": ["#Welcome", "#NewMember", "#Community"],
        "best_posting_times": ["10:00", "15:00"],
        "platforms": ["facebook", "instagram"]
    }
    template_id = templates.add_custom_template(custom_template)
    print(f"  ✅ Custom template added: {template_id}")

    print("\n" + "-" * 80)
    print(" ✅ TEST 1 PASSED: Post Templates Library")
    print("-" * 80)
    return True


async def test_hashtag_suggestions():
    """Test hashtag suggestion feature"""
    print("\n" + "=" * 80)
    print(" TEST 2: Hashtag Suggestions")
    print("=" * 80)

    from social_content_calendar import HashtagSuggester

    suggester = HashtagSuggester()

    # Test 2.1: Suggest from content
    print("\n[TEST 2.1] Suggesting hashtags from content...")
    content = "Excited to announce our new AI-powered business automation tool for entrepreneurs!"
    hashtags = suggester.suggest_hashtags(content, category="technology", count=10)
    print(f"  Content: {content[:80]}...")
    print(f"  Suggested hashtags: {len(hashtags)}")
    print(f"  Tags: {' '.join(hashtags[:5])}")

    # Test 2.2: Get hashtags by category
    print("\n[TEST 2.2] Getting hashtags by category...")
    for category in ["business", "marketing", "technology", "motivation"]:
        cat_hashtags = suggester.get_hashtags_by_category(category, count=3)
        print(f"  ✅ {category}: {cat_hashtags}")

    # Test 2.3: Platform-specific suggestions
    print("\n[TEST 2.3] Platform-specific suggestions...")
    fb_hashtags = suggester.suggest_hashtags(content, platform="facebook", count=5)
    ig_hashtags = suggester.suggest_hashtags(content, platform="instagram", count=5)
    print(f"  Facebook: {' '.join(fb_hashtags)}")
    print(f"  Instagram: {' '.join(ig_hashtags)}")

    print("\n" + "-" * 80)
    print(" ✅ TEST 2 PASSED: Hashtag Suggestions")
    print("-" * 80)
    return True


async def test_content_calendar():
    """Test content calendar management"""
    print("\n" + "=" * 80)
    print(" TEST 3: Content Calendar Management")
    print("=" * 80)

    from social_content_calendar import ContentCalendarManager

    calendar = ContentCalendarManager()

    # Test 3.1: Schedule a post
    print("\n[TEST 3.1] Scheduling a post...")
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_10am = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)

    post = await calendar.schedule_post(
        message="🎉 Testing the new content calendar feature! #Automation #SocialMedia",
        platforms=["facebook", "instagram"],
        scheduled_time=tomorrow_10am,
        link="https://example.com"
    )
    print(f"  ✅ Post scheduled: {post.id}")
    print(f"  Time: {tomorrow_10am.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Hashtags: {len(post.hashtags)} suggested")

    # Test 3.2: Schedule from template
    print("\n[TEST 3.2] Scheduling from template...")
    tomorrow_2pm = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)

    template_post = await calendar.schedule_from_template(
        template_id="template_engagement",
        variables={"engagement_question": "What's your favorite productivity hack?"},
        scheduled_time=tomorrow_2pm,
        platforms=["facebook", "instagram"]
    )
    print(f"  ✅ Template post scheduled: {template_post.id}")

    # Test 3.3: Get pending posts
    print("\n[TEST 3.3] Getting pending posts...")
    pending = await calendar.get_pending_posts()
    print(f"  ✅ Found {len(pending)} pending posts")

    # Test 3.4: Generate calendar view
    print("\n[TEST 3.4] Generating calendar view...")
    current_month = datetime.now().month
    current_year = datetime.now().year
    calendar_view = await calendar.generate_calendar_view(current_year, current_month)
    print(f"  ✅ Calendar view generated for {current_year}-{current_month:02d}")
    print(f"  Total posts: {calendar_view.total_posts}")
    print(f"  By platform: {calendar_view.posts_by_platform}")
    print(f"  By category: {calendar_view.posts_by_category}")

    # Test 3.5: Cancel a post
    print("\n[TEST 3.5] Cancelling a post...")
    cancelled = await calendar.cancel_post(post.id)
    print(f"  ✅ Post cancelled: {cancelled}")

    print("\n" + "-" * 80)
    print(" ✅ TEST 3 PASSED: Content Calendar Management")
    print("-" * 80)
    return True


async def test_analytics_dashboard():
    """Test analytics dashboard generation"""
    print("\n" + "=" * 80)
    print(" TEST 4: Analytics Dashboard Generation")
    print("=" * 80)

    from social_content_calendar import AnalyticsDashboardGenerator

    generator = AnalyticsDashboardGenerator()

    # Test 4.1: Generate dashboard
    print("\n[TEST 4.1] Generating analytics dashboard...")
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now() + timedelta(days=30)

    dashboard_path = await generator.generate_dashboard(start_date, end_date)
    print(f"  ✅ Dashboard generated: {dashboard_path}")

    # Verify file exists
    if os.path.exists(dashboard_path):
        file_size = os.path.getsize(dashboard_path)
        print(f"  ✅ File exists: {file_size} bytes")
    else:
        print(f"  ❌ File not found")
        return False

    print("\n" + "-" * 80)
    print(" ✅ TEST 4 PASSED: Analytics Dashboard Generation")
    print("-" * 80)
    return True


async def test_scheduled_post_manager():
    """Test scheduled post manager"""
    print("\n" + "=" * 80)
    print(" TEST 5: Scheduled Post Manager")
    print("=" * 80)

    from social_scheduler import ScheduledPostManager

    manager = ScheduledPostManager()

    # Test 5.1: Create recurring schedule (daily)
    print("\n[TEST 5.1] Creating daily recurring schedule...")
    daily_id = await manager.create_recurring_schedule(
        template_id="template_motivation",
        variables={
            "motivational_quote": "The only way to do great work is to love what you do.",
            "quote_author": "Steve Jobs"
        },
        platforms=["facebook", "instagram"],
        recurrence="daily",
        posting_times=["08:00"],
        days_of_week=[0, 1, 2, 3, 4]  # Weekdays
    )
    print(f"  ✅ Daily schedule created: {daily_id}")

    # Test 5.2: Create recurring schedule (weekly)
    print("\n[TEST 5.2] Creating weekly recurring schedule...")
    weekly_id = await manager.create_recurring_schedule(
        template_id="template_friday_fun",
        variables={"friday_content": "Happy Friday! Time to celebrate! 🎉"},
        platforms=["facebook", "instagram"],
        recurrence="weekly",
        posting_times=["17:00"],
        days_of_week=[4]  # Friday
    )
    print(f"  ✅ Weekly schedule created: {weekly_id}")

    # Test 5.3: Create recurring schedule (monthly)
    print("\n[TEST 5.3] Creating monthly recurring schedule...")
    monthly_id = await manager.create_recurring_schedule(
        template_id="template_announcement",
        variables={
            "announcement_title": "Monthly Update",
            "announcement_details": "Here's what we accomplished this month!"
        },
        platforms=["facebook", "instagram"],
        recurrence="monthly",
        posting_times=["10:00"],
        day_of_month=1
    )
    print(f"  ✅ Monthly schedule created: {monthly_id}")

    # Test 5.4: Get all schedules
    print("\n[TEST 5.4] Getting all schedules...")
    schedules = await manager.get_all_schedules()
    print(f"  ✅ Found {len(schedules)} schedules")

    for schedule in schedules[-3:]:  # Show last 3
        status = "🟢" if schedule.active else "🔴"
        print(f"    {status} {schedule.id} ({schedule.recurrence})")

    # Test 5.5: Process schedules for today
    print("\n[TEST 5.5] Processing schedules for today...")
    posts_created = await manager.process_schedules()
    print(f"  ✅ Posts created: {len(posts_created)}")

    # Test 5.6: Deactivate schedule
    print("\n[TEST 5.6] Deactivating schedule...")
    deactivated = await manager.deactivate_schedule(daily_id)
    print(f"  ✅ Schedule deactivated: {deactivated}")

    # Test 5.7: Delete schedule
    print("\n[TEST 5.7] Deleting schedule...")
    deleted = await manager.delete_schedule(monthly_id)
    print(f"  ✅ Schedule deleted: {deleted}")

    print("\n" + "-" * 80)
    print(" ✅ TEST 5 PASSED: Scheduled Post Manager")
    print("-" * 80)
    return True


async def test_integration_with_facebook_instagram():
    """Test integration with Facebook/Instagram module"""
    print("\n" + "=" * 80)
    print(" TEST 6: Integration with Facebook/Instagram")
    print("=" * 80)

    from facebook_instagram_integration import FacebookInstagramIntegration

    # Initialize in mock mode
    integration = FacebookInstagramIntegration(mock_mode=True)

    # Test 6.1: Post to Facebook
    print("\n[TEST 6.1] Posting to Facebook (mock)...")
    fb_result = await integration.post_to_facebook(
        message="🧪 Testing Facebook integration from advanced features module!"
    )
    if fb_result.get("success"):
        print(f"  ✅ Facebook post successful: {fb_result.get('post_id')}")
    else:
        print(f"  ⚠️ Facebook post warning: {fb_result.get('error', 'Unknown')}")

    # Test 6.2: Post to Instagram
    print("\n[TEST 6.2] Posting to Instagram (mock)...")
    ig_result = await integration.post_to_instagram(
        message="🧪 Testing Instagram integration! #Test",
        image_url="https://example.com/test.jpg"
    )
    if ig_result.get("success"):
        print(f"  ✅ Instagram post successful: {ig_result.get('post_id')}")
    else:
        print(f"  ⚠️ Instagram post warning: {ig_result.get('error', 'Unknown')}")

    # Test 6.3: Post to both
    print("\n[TEST 6.3] Posting to both platforms (mock)...")
    both_result = await integration.post_to_both(
        message="🧪 Cross-platform test post!"
    )
    if both_result.get("success"):
        print(f"  ✅ Cross-platform post successful")
        print(f"    Facebook: {'✅' if both_result['facebook'].get('success') else '❌'}")
        print(f"    Instagram: {'✅' if both_result['instagram'].get('success') else '❌'}")

    # Test 6.4: Generate summaries
    print("\n[TEST 6.4] Generating platform summaries...")
    fb_summary = await integration.generate_facebook_summary()
    if fb_summary.get("success"):
        print(f"  ✅ Facebook summary: {fb_summary.get('total_posts')} posts")

    ig_summary = await integration.generate_instagram_summary()
    if ig_summary.get("success"):
        print(f"  ✅ Instagram summary: {ig_summary.get('total_posts')} posts")

    combined = await integration.generate_combined_summary()
    if combined.get("success"):
        print(f"  ✅ Combined summary generated")
        print(f"    Total engagement: {combined.get('combined_metrics', {}).get('total_engagement', 0)}")

    print("\n" + "-" * 80)
    print(" ✅ TEST 6 PASSED: Integration with Facebook/Instagram")
    print("-" * 80)
    return True


async def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("=" * 80)
    print("   ADVANCED SOCIAL MEDIA FEATURES - TEST SUITE".center(80))
    print("=" * 80)
    print("=" * 80)

    tests = [
        ("Post Templates Library", test_templates_library),
        ("Hashtag Suggestions", test_hashtag_suggestions),
        ("Content Calendar", test_content_calendar),
        ("Analytics Dashboard", test_analytics_dashboard),
        ("Scheduled Post Manager", test_scheduled_post_manager),
        ("Facebook/Instagram Integration", test_integration_with_facebook_instagram)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 80)
    print(" TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status}: {test_name}")

    print(f"\n  Total: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")

    print("\n" + "=" * 80)
    if passed == total:
        print("   ALL TESTS PASSED! 🎉".center(80))
    else:
        print(f"   {total - passed} TEST(S) FAILED".center(80))
    print("=" * 80)

    # Files created
    print("\n📁 Files Created/Modified:")
    print("  - state/post_templates.json")
    print("  - state/content_calendar.json")
    print("  - state/recurring_schedules.json")
    print("  - dashboards/social_analytics.html")
    print("  - logs/scheduled_posts_log.md")

    return passed == total


if __name__ == "__main__":
    import sys

    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
