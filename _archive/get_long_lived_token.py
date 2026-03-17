"""
Facebook Long-Lived Token Generator

Converts a short-lived token (1-2 hours) to a long-lived token (60 days).

Steps:
1. Get your App ID and App Secret from Facebook Developers
2. Run this script
3. Update .env with the new long-lived token

Usage:
    python get_long_lived_token.py
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def get_long_lived_token():
    """Exchange short-lived token for long-lived token"""
    
    print("=" * 80)
    print(" 🔑 FACEBOOK LONG-LIVED TOKEN GENERATOR")
    print("=" * 80)
    
    # Get current token
    short_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    
    print(f"\n Current token length: {len(short_token)} chars")
    
    # You need App ID and App Secret
    print("\n⚠️  To get a long-lived token, you need your App ID and App Secret:")
    print("   1. Go to: https://developers.facebook.com/apps/")
    print("   2. Select your app")
    print("   3. Go to Settings → Basic")
    print("   4. Copy App ID and App Secret\n")
    
    app_id = input("Enter your App ID: ").strip()
    app_secret = input("Enter your App Secret: ").strip()
    
    if not app_id or not app_secret:
        print("\n❌ App ID and App Secret are required!")
        return None
    
    print("\n🔄 Exchanging token...")
    
    try:
        response = httpx.get(
            "https://graph.facebook.com/v19.0/oauth/access_token",
            params={
                'grant_type': 'fb_exchange_token',
                'client_id': app_id,
                'client_secret': app_secret,
                'fb_exchange_token': short_token
            },
            timeout=30.0
        )
        
        data = response.json()
        
        if response.status_code == 200:
            long_token = data.get('access_token', '')
            expires_in = data.get('expires_in', 0)
            
            print("\n" + "=" * 80)
            print(" ✅ LONG-LIVED TOKEN GENERATED!")
            print("=" * 80)
            print(f" Token: {long_token[:50]}...")
            print(f" Expires in: {expires_in} seconds ({expires_in // 86400} days)")
            print("=" * 80)
            
            # Ask to save
            save = input("\nSave to .env file? (y/n): ").strip().lower()
            if save == 'y':
                # Read current .env
                with open('.env', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace token
                import re
                old_token_pattern = r'FACEBOOK_PAGE_ACCESS_TOKEN=.*'
                new_line = f'FACEBOOK_PAGE_ACCESS_TOKEN={long_token}'
                content = re.sub(old_token_pattern, new_line, content)
                
                # Write back
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("\n✅ Token saved to .env!")
                print("Run 'python test_facebook_token.py' to verify")
            
            return long_token
        else:
            print("\n❌ ERROR:")
            print(f"   Status: {response.status_code}")
            print(f"   Message: {data.get('error', {}).get('message', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return None


def manual_instructions():
    """Show manual instructions for getting long-lived token"""
    
    print("\n" + "=" * 80)
    print(" 📖 MANUAL METHOD")
    print("=" * 80)
    print("""
If you prefer to get the long-lived token manually:

1. Go to Graph API Explorer:
   https://developers.facebook.com/tools/explorer/

2. Select your app and get a Page Access Token

3. Copy the token

4. Visit this URL in your browser (replace YOUR_TOKEN):
   https://graph.facebook.com/v19.0/oauth/access_token?
   grant_type=fb_exchange_token&
   client_id=YOUR_APP_ID&
   client_secret=YOUR_APP_SECRET&
   fb_exchange_token=YOUR_TOKEN

5. Copy the access_token from the response

6. Update your .env file:
   FACEBOOK_PAGE_ACCESS_TOKEN=YOUR_LONG_LIVED_TOKEN
""")
    print("=" * 80)


if __name__ == "__main__":
    import sys
    
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("\nChoose method:")
    print("  1. Automatic (enter App ID and Secret)")
    print("  2. Show manual instructions")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        get_long_lived_token()
    else:
        manual_instructions()
