"""
Direct Facebook Live Poster - Bypasses mock mode

Usage:
    python post_facebook_live_now.py
"""

import asyncio
import sys
import os
from datetime import datetime

# Force reload of environment
from dotenv import load_dotenv
load_dotenv(override=True)

import httpx

async def post_to_facebook_live(message: str):
    """Post directly to Facebook using Graph API"""
    
    print("=" * 80)
    print(" 🚀 FACEBOOK LIVE POST")
    print("=" * 80)
    print(f" Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Get configuration
    page_access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    page_id = os.getenv("FACEBOOK_PAGE_ID", "")
    graph_api_version = os.getenv("GRAPH_API_VERSION", "v19.0")
    
    print(f"\n📋 Configuration:")
    print(f"   Page ID: {page_id}")
    print(f"   Token length: {len(page_access_token)} chars")
    print(f"   API Version: {graph_api_version}")
    print(f"   Mock Mode: FALSE (Forced live)")
    
    print(f"\n📝 Message:\n{message}\n")
    print("-" * 80)
    
    if not page_access_token or not page_id:
        print("❌ ERROR: Missing Facebook credentials in .env file!")
        return {"success": False, "error": "Missing credentials"}
    
    # Post to Facebook
    print("📘 Posting to Facebook LIVE...")
    
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            # Text-only post
            post_url = f"https://graph.facebook.com/{graph_api_version}/{page_id}/feed"
            params = {
                'message': message,
                'access_token': page_access_token
            }
            
            print(f"   API URL: {post_url}")
            print(f"   Sending request...")
            
            response = await client.post(post_url, params=params)
            
            print(f"   Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                post_id = result.get('id', 'unknown')
                
                print(f"\n✅ FACEBOOK POST SUCCESSFUL!")
                print(f"   Post ID: {post_id}")
                print(f"   URL: https://facebook.com/{post_id}")
                
                return {
                    "success": True,
                    "post_id": post_id,
                    "url": f"https://facebook.com/{post_id}"
                }
            else:
                error_msg = response.text
                print(f"\n❌ FACEBOOK POST FAILED!")
                print(f"   Status: {response.status_code}")
                print(f"   Error: {error_msg[:200]}")
                
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {error_msg[:200]}"
                }
                
    except httpx.HTTPStatusError as e:
        print(f"\n❌ HTTP ERROR: {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    # Message to post
    message = """🎉 Exciting News from AI Employee Vault! 

We're revolutionizing business automation with our cutting-edge AI solutions. 

✨ What we offer:
• Intelligent process automation
• Smart document management
• Cross-platform integration
• Real-time analytics

Ready to transform your business? Let's connect! 💼

#AIEmployeeVault #BusinessAutomation #AI #Innovation #DigitalTransformation #Productivity #TechSolutions #Entrepreneur #BusinessGrowth #Automation"""
    
    # Check for custom message
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        print(f"\n📝 Using custom message\n")
    
    # Post
    result = asyncio.run(post_to_facebook_live(message))
    
    print("\n" + "=" * 80)
    print(" SUMMARY")
    print("=" * 80)
    print(f" Status: {'✅ SUCCESS' if result.get('success') else '❌ FAILED'}")
    print("=" * 80)
    
    sys.exit(0 if result.get("success") else 1)
