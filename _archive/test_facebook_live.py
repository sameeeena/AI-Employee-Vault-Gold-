"""
Test Facebook Live Posting

This script tests real Facebook posting using the Social MCP Server.
Make sure the server is running before executing this script.
"""

import httpx
import json
import sys
import os
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    sys.stdout.reconfigure(encoding='utf-8')

def test_facebook_post():
    print("=" * 70)
    print("FACEBOOK LIVE POSTING TEST")
    print("=" * 70)
    print()
    
    # Test message
    message = f"🎉 Hello from AI Employee Vault! Testing live Facebook post at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} #TestPost #FacebookIntegration"
    
    print(f"📝 Message: {message}")
    print()
    print("Posting to Facebook...")
    print("-" * 70)
    
    try:
        # Post to Facebook via MCP Server
        response = httpx.post(
            "http://localhost:8002/api/post_message",
            json={
                "platform": "facebook",
                "message": message
            },
            timeout=30.0
        )
        
        result = response.json()
        
        print()
        print("RESPONSE:")
        print(json.dumps(result, indent=2))
        print()
        
        if result.get("success"):
            print("✅ SUCCESS! Facebook post published!")
            print()
            data = result.get("data", {})
            print(f"   Post ID: {data.get('post_id')}")
            print(f"   Post URL: https://facebook.com/{data.get('post_id', '')}")
            print(f"   Timestamp: {data.get('timestamp')}")
            print()
            print("🔗 View your post:")
            print(f"   https://www.facebook.com/1496288429174042/posts/{data.get('post_id', '').split('_')[1] if '_' in data.get('post_id', '') else ''}")
            return True
        else:
            print("❌ FAILED! Post was not published.")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except httpx.TimeoutException:
        print("❌ TIMEOUT! Request timed out.")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_facebook_post_with_image():
    print()
    print("=" * 70)
    print("FACEBOOK POST WITH IMAGE TEST")
    print("=" * 70)
    print()
    
    message = f"📸 Testing Facebook post with image! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    image_url = "https://picsum.photos/800/600"  # Random image
    
    print(f"📝 Message: {message}")
    print(f"🖼️  Image URL: {image_url}")
    print()
    print("Posting to Facebook with image...")
    print("-" * 70)
    
    try:
        response = httpx.post(
            "http://localhost:8002/api/post_message",
            json={
                "platform": "facebook",
                "message": message,
                "image_url": image_url
            },
            timeout=30.0
        )
        
        result = response.json()
        
        print()
        print("RESPONSE:")
        print(json.dumps(result, indent=2))
        print()
        
        if result.get("success"):
            print("✅ SUCCESS! Facebook post with image published!")
            return True
        else:
            print("❌ FAILED!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_get_summary():
    print()
    print("=" * 70)
    print("FACEBOOK SUMMARY TEST")
    print("=" * 70)
    print()
    
    print("Fetching Facebook page summary...")
    print("-" * 70)
    
    try:
        response = httpx.get(
            "http://localhost:8002/api/get_summary?platform=facebook",
            timeout=30.0
        )
        
        result = response.json()
        
        print()
        print("RESPONSE:")
        print(json.dumps(result, indent=2))
        print()
        
        if result.get("success"):
            print("✅ SUCCESS! Summary retrieved!")
            data = result.get("data", {})
            print(f"   Total Posts: {data.get('total_posts', 'N/A')}")
            print(f"   Total Reactions: {data.get('total_reactions', 'N/A')}")
            print(f"   Total Comments: {data.get('total_comments', 'N/A')}")
            print(f"   Total Shares: {data.get('total_shares', 'N/A')}")
            print(f"   Average Engagement: {data.get('average_engagement', 'N/A')}")
            return True
        else:
            print("❌ FAILED!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


if __name__ == "__main__":
    print()
    print("Select test:")
    print("1. Post text to Facebook")
    print("2. Post text + image to Facebook")
    print("3. Get Facebook summary")
    print("4. Run all tests")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        test_facebook_post()
    elif choice == "2":
        test_facebook_post_with_image()
    elif choice == "3":
        test_get_summary()
    elif choice == "4":
        print("\n" + "=" * 70)
        print("RUNNING ALL TESTS")
        print("=" * 70)
        test_facebook_post()
        print()
        test_facebook_post_with_image()
        print()
        test_get_summary()
    else:
        print("Invalid choice!")
