"""
Facebook Poster - Alternative Method

Tries different API endpoints to post without pages_manage_posts permission.

Usage:
    python post_with_alternative_method.py
"""

import httpx
import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv(override=True)


async def try_posting_methods():
    """Try multiple posting methods"""
    
    print("=" * 80)
    print(" 📘 FACEBOOK POST - ALTERNATIVE METHODS")
    print("=" * 80)
    
    page_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    page_id = os.getenv("FACEBOOK_PAGE_ID", "")
    
    message = """🎉 Exciting News from AI Employee Vault! 

We're revolutionizing business automation with our cutting-edge AI solutions. 

✨ What we offer:
• Intelligent process automation
• Smart document management
• Cross-platform integration
• Real-time analytics

Ready to transform your business? Let's connect! 💼

#AIEmployeeVault #BusinessAutomation #AI #Innovation"""
    
    print(f"\n📋 Page ID: {page_id}")
    print(f"📝 Message: {message[:80]}...\n")
    
    methods = [
        ("Published Posts", "published_posts"),
        ("Feed", "feed"),
        ("Photos", "photos"),
    ]
    
    for method_name, endpoint in methods:
        print(f"\n{'='*60}")
        print(f" Trying: {method_name}")
        print(f"{'='*60}")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if endpoint == "photos":
                    # Try posting with a placeholder image
                    url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
                    params = {
                        'message': message,
                        'url': 'https://via.placeholder.com/1200x630.png?text=AI+Employee+Vault',
                        'published': 'true',
                        'access_token': page_token
                    }
                else:
                    url = f"https://graph.facebook.com/v19.0/{page_id}/{endpoint}"
                    params = {
                        'message': message,
                        'access_token': page_token
                    }
                
                print(f"   URL: {url}")
                response = await client.post(url, params=params)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    post_id = result.get('id', 'unknown')
                    
                    print(f"\n{'='*80}")
                    print(f" ✅ SUCCESS via {method_name}!")
                    print(f"   Post ID: {post_id}")
                    print(f"   URL: https://facebook.com/{post_id}")
                    print(f"{'='*80}")
                    return True
                else:
                    error = response.json()
                    error_msg = error.get('error', {}).get('message', 'Unknown')
                    print(f"   ❌ Failed: {error_msg[:100]}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n{'='*80}")
    print(" ❌ All methods failed!")
    print(f"{'='*80}")
    print("\n💡 You NEED pages_manage_posts permission.")
    print("\n📋 Next Steps:")
    print("   1. Make your Facebook App LIVE (not Development)")
    print("   2. Add Instagram Graph API product to your app")
    print("   3. Go through App Review for pages_manage_posts")
    print("   4. Or get token directly from Facebook Page settings")
    print(f"{'='*80}")
    
    return False


if __name__ == "__main__":
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    success = asyncio.run(try_posting_methods())
    sys.exit(0 if success else 1)
