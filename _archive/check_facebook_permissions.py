"""Check Current Facebook Permissions"""
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Get token from .env
token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')

if not token:
    print("❌ No token found in .env file!")
    print("Please add FACEBOOK_PAGE_ACCESS_TOKEN to your .env file")
    exit(1)

print("=" * 70)
print("  CHECKING YOUR CURRENT FACEBOOK PERMISSIONS")
print("=" * 70)
print(f"\n📋 Token (first 50 chars): {token[:50]}...")

# Check permissions
url = "https://graph.facebook.com/me/permissions"
params = {"access_token": token}

print(f"\n⏳ Checking permissions...")
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    permissions = data.get('data', [])
    
    print("\n" + "=" * 70)
    print("  YOUR CURRENT PERMISSIONS:")
    print("=" * 70)
    
    required = [
        'pages_manage_posts',
        'pages_read_engagement', 
        'pages_show_list',
        'instagram_basic',
        'instagram_content_publish'
    ]
    
    granted = [p['permission'] for p in permissions if p.get('status') == 'granted']
    
    print(f"\n✅ Granted permissions ({len(granted)}):")
    for p in granted:
        mark = "✅" if p in required else "  "
        print(f"   {mark} {p}")
    
    print(f"\n❌ Missing permissions:")
    for p in required:
        if p not in granted:
            print(f"   ❌ {p}")
    
    missing = [p for p in required if p not in granted]
    
    if missing:
        print(f"\n⚠️  You need to add these permissions: {', '.join(missing)}")
    else:
        print("\n🎉 All required permissions are granted!")
else:
    print(f"\n❌ Error: {response.status_code}")
    print(f"Response: {response.text}")

print("\n" + "=" * 70)
