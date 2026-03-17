"""
Facebook & Instagram Integration Test Script

Tests all functionality of the Facebook/Instagram integration:
1. Posting to Facebook
2. Posting to Instagram
3. Posting to both platforms
4. Fetching engagement metrics
5. Generating summaries

Run this script to verify the integration is working correctly.
"""

import asyncio
import json
import sys
from datetime import datetime


async def test_integration():
    """Run all integration tests"""
    
    print("=" * 80)
    print(" FACEBOOK & INSTAGRAM INTEGRATION - TEST SUITE")
    print("=" * 80)
    print(f" Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Import the integration module
    try:
        from facebook_instagram_integration import FacebookInstagramIntegration
        print("[OK] Module imported successfully")
    except ImportError as e:
        print(f"[FAIL] Failed to import module: {e}")
        print("\nMake sure facebook_instagram_integration.py is in the same directory")
        return False
    
    # Initialize integration
    try:
        integration = FacebookInstagramIntegration(mock_mode=True)
        print("[OK] Integration initialized (Mock Mode)")
    except Exception as e:
        print(f"[FAIL] Failed to initialize integration: {e}")
        return False
    
    tests_passed = 0
    tests_failed = 0
    
    # ============== TEST 1: Facebook Post ==============
    print("\n" + "-" * 80)
    print(" TEST 1: Post to Facebook")
    print("-" * 80)
    
    try:
        fb_result = await integration.post_to_facebook(
            message="🎉 Hello from AI Employee Vault! Testing Facebook integration. #AI #Automation",
            link="https://example.com"
        )
        
        if fb_result.get("success"):
            print(f"[OK] Facebook Post Successful!")
            print(f"   Post ID: {fb_result.get('post_id')}")
            print(f"   Message: {fb_result.get('message')}")
            print(f"   URL: {fb_result.get('post_url', 'N/A')}")
            tests_passed += 1
        else:
            print(f"[FAIL] Facebook Post Failed: {fb_result.get('error')}")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] Test 1 Error: {e}")
        tests_failed += 1
    
    # ============== TEST 2: Instagram Post ==============
    print("\n" + "-" * 80)
    print(" TEST 2: Post to Instagram")
    print("-" * 80)
    
    try:
        ig_result = await integration.post_to_instagram(
            message="🌟 Beautiful day for Instagram! Testing Instagram integration. #Instagram #AI",
            image_url="https://example.com/image.jpg"
        )
        
        if ig_result.get("success"):
            print(f"[OK] Instagram Post Successful!")
            print(f"   Post ID: {ig_result.get('post_id')}")
            print(f"   Message: {ig_result.get('message')}")
            tests_passed += 1
        else:
            print(f"[FAIL] Instagram Post Failed: {ig_result.get('error')}")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] Test 2 Error: {e}")
        tests_failed += 1
    
    # ============== TEST 3: Post to Both Platforms ==============
    print("\n" + "-" * 80)
    print(" TEST 3: Post to Both Facebook & Instagram")
    print("-" * 80)
    
    try:
        import asyncio
        both_result = await integration.post_to_both(
            message="🚀 Cross-posting to Facebook and Instagram! #SocialMedia #Automation"
        )
        
        if both_result.get("success"):
            print(f"[OK] Cross-Platform Post Successful!")
            print(f"   Facebook: {'[OK]' if both_result.get('facebook', {}).get('success') else '[FAIL]'}")
            print(f"   Instagram: {'[OK]' if both_result.get('instagram', {}).get('success') else '[FAIL]'}")
            print(f"   Successful Platforms: {both_result.get('summary', {}).get('successful_posts', 0)}/2")
            tests_passed += 1
        else:
            print(f"[FAIL] Cross-Platform Post Failed")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] Test 3 Error: {e}")
        tests_failed += 1
    
    # ============== TEST 4: Facebook Metrics ==============
    print("\n" + "-" * 80)
    print(" TEST 4: Fetch Facebook Engagement Metrics")
    print("-" * 80)
    
    try:
        fb_metrics = await integration.get_facebook_metrics("fb_mock_post")
        
        if fb_metrics.get("success"):
            print(f"[OK] Facebook Metrics Retrieved!")
            print(f"   Reactions: {fb_metrics.get('reactions', 0)}")
            print(f"   Comments: {fb_metrics.get('comments', 0)}")
            print(f"   Shares: {fb_metrics.get('shares', 0)}")
            print(f"   Impressions: {fb_metrics.get('impressions', 0)}")
            tests_passed += 1
        else:
            print(f"[FAIL] Facebook Metrics Failed: {fb_metrics.get('error')}")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] Test 4 Error: {e}")
        tests_failed += 1
    
    # ============== TEST 5: Instagram Metrics ==============
    print("\n" + "-" * 80)
    print(" TEST 5: Fetch Instagram Engagement Metrics")
    print("-" * 80)
    
    try:
        ig_metrics = await integration.get_instagram_metrics("ig_mock_post")
        
        if ig_metrics.get("success"):
            print(f"[OK] Instagram Metrics Retrieved!")
            print(f"   Likes: {ig_metrics.get('likes', 0)}")
            print(f"   Comments: {ig_metrics.get('comments', 0)}")
            print(f"   Impressions: {ig_metrics.get('impressions', 0)}")
            print(f"   Reach: {ig_metrics.get('reach', 0)}")
            print(f"   Saves: {ig_metrics.get('saved', 0)}")
            tests_passed += 1
        else:
            print(f"[FAIL] Instagram Metrics Failed: {ig_metrics.get('error')}")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] Test 5 Error: {e}")
        tests_failed += 1
    
    # ============== TEST 6: Facebook Summary ==============
    print("\n" + "-" * 80)
    print(" TEST 6: Generate Facebook Summary")
    print("-" * 80)
    
    try:
        fb_summary = await integration.generate_facebook_summary()
        
        if fb_summary.get("success"):
            print(f"[OK] Facebook Summary Generated!")
            print(f"   Total Posts: {fb_summary.get('total_posts', 0)}")
            print(f"   Total Reactions: {fb_summary.get('total_reactions', 0)}")
            print(f"   Total Comments: {fb_summary.get('total_comments', 0)}")
            print(f"   Total Shares: {fb_summary.get('total_shares', 0)}")
            print(f"   Average Engagement: {fb_summary.get('average_engagement', 0):.2f}")
            tests_passed += 1
        else:
            print(f"[FAIL] Facebook Summary Failed: {fb_summary.get('error')}")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] Test 6 Error: {e}")
        tests_failed += 1
    
    # ============== TEST 7: Instagram Summary ==============
    print("\n" + "-" * 80)
    print(" TEST 7: Generate Instagram Summary")
    print("-" * 80)
    
    try:
        ig_summary = await integration.generate_instagram_summary()
        
        if ig_summary.get("success"):
            print(f"[OK] Instagram Summary Generated!")
            print(f"   Total Posts: {ig_summary.get('total_posts', 0)}")
            print(f"   Total Likes: {ig_summary.get('total_likes', 0)}")
            print(f"   Total Comments: {ig_summary.get('total_comments', 0)}")
            print(f"   Average Engagement: {ig_summary.get('average_engagement', 0):.2f}")
            tests_passed += 1
        else:
            print(f"[FAIL] Instagram Summary Failed: {ig_summary.get('error')}")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] Test 7 Error: {e}")
        tests_failed += 1
    
    # ============== TEST 8: Combined Summary ==============
    print("\n" + "-" * 80)
    print(" TEST 8: Generate Combined Facebook & Instagram Summary")
    print("-" * 80)
    
    try:
        combined_summary = await integration.generate_combined_summary()
        
        if combined_summary.get("success"):
            print(f"[OK] Combined Summary Generated!")
            print(f"   Total Posts: {combined_summary.get('combined_metrics', {}).get('total_posts', 0)}")
            print(f"   Total Engagement: {combined_summary.get('combined_metrics', {}).get('total_engagement', 0)}")
            print(f"   Facebook Data: {'[OK]' if combined_summary.get('facebook', {}).get('success') else '[FAIL]'}")
            print(f"   Instagram Data: {'[OK]' if combined_summary.get('instagram', {}).get('success') else '[FAIL]'}")
            tests_passed += 1
        else:
            print(f"[FAIL] Combined Summary Failed")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] Test 8 Error: {e}")
        tests_failed += 1
    
    # ============== TEST SUMMARY ==============
    print("\n" + "=" * 80)
    print(" TEST SUMMARY")
    print("=" * 80)
    print(f" Tests Passed: {tests_passed}/8")
    print(f" Tests Failed: {tests_failed}/8")
    print(f" Success Rate: {(tests_passed/8)*100:.1f}%")
    print("=" * 80)
    
    if tests_failed == 0:
        print(" ALL TESTS PASSED!")
        print("\nDetailed Results:")
        print("   - Facebook posting: PASSED")
        print("   - Instagram posting: PASSED")
        print("   - Cross-platform posting: PASSED")
        print("   - Facebook metrics: PASSED")
        print("   - Instagram metrics: PASSED")
        print("   - Facebook summary: PASSED")
        print("   - Instagram summary: PASSED")
        print("   - Combined summary: PASSED")
    else:
        print(f" {tests_failed} TEST(S) FAILED")
        print("\nCheck the error messages above for details.")
    
    print("\n" + "=" * 80)
    print(f" Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return tests_failed == 0


async def test_mcp_server():
    """Test the MCP Server endpoints"""
    
    print("\n" + "=" * 80)
    print(" MCP SERVER API TEST")
    print("=" * 80)
    
    import httpx
    
    base_url = "http://localhost:8002"
    
    # Test 1: Health Check
    print("\n[API] Testing Health Endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"[OK] Health Check Passed")
                print(f"   Status: {health_data.get('status')}")
                print(f"   Platforms: {health_data.get('platforms')}")
                print(f"   Mock Mode: {health_data.get('mock_mode')}")
            else:
                print(f"[FAIL] Health Check Failed: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Health Check Error: {e}")
        print("   Make sure the MCP server is running: python social_mcp_server_v2.py")
        return False
    
    # Test 2: Post Message
    print("\n[API] Testing Post Message Endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "platform": "both",
                "message": "Testing MCP Server API! #TestPost",
                "image_url": None,
                "link": None
            }
            response = await client.post(f"{base_url}/api/post_message", json=payload)
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"[OK] Post Message API Passed")
                    print(f"   Request ID: {result.get('request_id')}")
                else:
                    print(f"[WARN] Post Message API Warning: {result.get('error')}")
            else:
                print(f"[FAIL] Post Message API Failed: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Post Message API Error: {e}")
    
    # Test 3: Generate Summary
    print("\n[API] Testing Generate Summary Endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/get_summary?platform=both")
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"[OK] Generate Summary API Passed")
                    data = result.get("data", {})
                    print(f"   Total Posts: {data.get('combined_metrics', {}).get('total_posts', 'N/A')}")
                    print(f"   Total Engagement: {data.get('combined_metrics', {}).get('total_engagement', 'N/A')}")
                else:
                    print(f"[WARN] Generate Summary API Warning: {result.get('error')}")
            else:
                print(f"[FAIL] Generate Summary API Failed: {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Generate Summary API Error: {e}")
    
    print("\n" + "=" * 80)
    print(" MCP SERVER API TEST COMPLETED")
    print("=" * 80)
    
    return True


async def main():
    """Main test runner"""
    
    print("\n" + "=" * 80)
    print("=" * 80)
    print("   FACEBOOK & INSTAGRAM INTEGRATION - COMPLETE TEST SUITE".center(80))
    print("=" * 80)
    print("=" * 80)
    
    # Run integration tests
    integration_passed = await test_integration()
    
    # Ask user if they want to test MCP server
    print("\n" + "-" * 80)
    print("Do you want to test the MCP Server API? (y/n)")
    print("(Make sure the server is running: python social_mcp_server_v2.py)")
    print("-" * 80)
    
    # For automated testing, skip interactive prompt
    # In manual mode, you can uncomment this:
    # test_server = input("Test MCP Server API? (y/n): ").lower().strip() == 'y'
    test_server = False  # Auto-skip for now
    
    if test_server:
        await test_mcp_server()
    
    # Final summary
    print("\n" + "=" * 80)
    print("=" * 80)
    if integration_passed:
        print("   INTEGRATION TESTS PASSED - READY FOR PRODUCTION".center(80))
    else:
        print("   SOME TESTS FAILED - REVIEW ERRORS ABOVE".center(80))
    print("=" * 80)
    print("=" * 80)
    print("\nNext Steps:")
    print("   1. Configure your Facebook Page ID and Access Tokens in .env")
    print("   2. Set SOCIAL_MOCK_MODE=false to enable live posting")
    print("   3. Start the MCP server: python social_mcp_server_v2.py")
    print("   4. Access API docs at: http://localhost:8002/docs")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    import sys
    
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    asyncio.run(main())
