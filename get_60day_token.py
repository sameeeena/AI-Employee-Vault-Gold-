"""
Get 60-Day Facebook Long-Lived Token

Simple script to exchange short-lived token for 60-day token.
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print(" 🔑 GET 60-DAY FACEBOOK TOKEN")
print("=" * 80)

# Current token
current_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
print(f"\n Current token (first 50 chars): {current_token[:50]}...")

print("\n" + "=" * 80)
print(" 📋 STEP 1: Get App Secret")
print("=" * 80)
print("""
1. Go to: https://developers.facebook.com/apps/
2. Select your app: AI Employee Vault (ID: 818482444607294)
3. Go to Settings → Basic
4. Click "Show" next to App Secret
5. Copy the App Secret
""")

app_secret_input = input("\nPaste your App Secret here: ").strip()

if not app_secret_input:
    print("\n❌ App Secret is required!")
    exit()

print("\n🔄 Exchanging for long-lived token...")

try:
    # Exchange for long-lived token
    response = httpx.get(
        "https://graph.facebook.com/v19.0/oauth/access_token",
        params={
            'grant_type': 'fb_exchange_token',
            'client_id': '818482444607294',  # Your App ID
            'client_secret': app_secret_input,
            'fb_exchange_token': current_token
        },
        timeout=30.0
    )

    data = response.json()

    if response.status_code == 200 and 'access_token' in data:
        long_token = data['access_token']
        expires_in = data.get('expires_in', 5184000)  # 60 days in seconds
        days = expires_in // 86400

        print("\n" + "=" * 80)
        print(" ✅ LONG-LIVED TOKEN GENERATED!")
        print("=" * 80)
        print(f" Token: {long_token[:60]}...")
        print(f" ⏰ Expires in: {days} days")
        print("=" * 80)

        # Save to .env
        save = input("\nSave to .env file? (y/n): ").strip().lower()
        if save == 'y':
            with open('.env', 'r', encoding='utf-8') as f:
                content = f.read()

            import re
            old_pattern = r'FACEBOOK_PAGE_ACCESS_TOKEN=.*'
            new_line = f'FACEBOOK_PAGE_ACCESS_TOKEN={long_token}'
            content = re.sub(old_pattern, new_line, content)

            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)

            print("\n✅ Token saved to .env!")
            print("\n🚀 Now you can autopost for 60 days without new token!")
            print("\nTest with:")
            print("   python facebook_autopost_now.py --template 1")
        else:
            print("\nToken not saved. Copy it manually:")
            print(long_token)

    else:
        error_msg = data.get('error', {}).get('message', 'Unknown error')
        print(f"\n❌ ERROR: {error_msg}")
        print("\nPossible issues:")
        print("  - App Secret is incorrect")
        print("  - Current token is invalid")
        print("  - App is not approved for pages_manage_posts")

except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 80)
