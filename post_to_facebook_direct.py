"""
Facebook Live Poster - Direct API Call

Posts directly to Facebook using Page Access Token.
Bypasses permission checks - works for page admins.

Usage:
    python post_to_facebook_direct.py
"""

import httpx
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Force reload environment
load_dotenv(override=True)

async def post_to_facebook():
    """Post to Facebook directly"""
    
    print("=" * 80)
    print(" 📘 FACEBOOK LIVE POSTER")
    print("=" * 80)
    print(f" Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Get config
    page_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    page_id = os.getenv("FACEBOOK_PAGE_ID", "")
    
    print(f"\n📋 Configuration:")
    print(f"   Page ID: {page_id}")
    print(f"   Token Length: {len(page_token)} chars")
    
    if not page_token or not page_id:
        print("\n❌ ERROR: Missing credentials in .env!")
        return False
    
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
    
    print(f"\n📝 Message:\n{message[:100]}...\n")
    print("-" * 80)
    print("🚀 Posting to Facebook LIVE...\n")
    
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            # Try posting to page feed
            url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            params = {
                'message': message,
                'access_token': page_token
            }
            
            print(f"   Sending POST request...")
            response = await client.post(url, params=params)
            
            print(f"   Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                post_id = result.get('id', 'unknown')
                
                print(f"\n{'='*80}")
                print(f" ✅ SUCCESS! POSTED TO FACEBOOK!")
                print(f"{'='*80}")
                print(f"   Post ID: {post_id}")
                print(f"   View Post: https://facebook.com/{post_id}")
                print(f"{'='*80}")
                
                return True
                
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                error_code = error_data.get('error', {}).get('code', 'Unknown')
                
                print(f"\n❌ POST FAILED!")
                print(f"   Error Code: {error_code}")
                print(f"   Message: {error_msg}")
                
                # Show specific solutions
                print(f"\n💡 SOLUTION:")
                if "permission" in error_msg.lower():
                    print(f"   You need posting permissions.")
                    print(f"   Try: Get token from Facebook Page directly (not Graph API)")
                    print(f"   Go to: https://www.facebook.com/{page_id}/settings/?tab=page_access")
                elif "expired" in error_msg.lower():
                    print(f"   Token expired! Generate new token.")
                    print(f"   Go to: https://developers.facebook.com/tools/explorer/")
                else:
                    print(f"   Check your Page ID and Token in .env file")
                
                return False
                
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    import asyncio
    success = asyncio.run(post_to_facebook())
    sys.exit(0 if success else 1)
