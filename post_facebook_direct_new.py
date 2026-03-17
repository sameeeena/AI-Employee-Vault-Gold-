"""
Direct Facebook Post - Fresh Token Load
"""
from dotenv import load_dotenv
import os
import httpx

# Force reload .env
load_dotenv(override=True)

token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
page_id = os.getenv("FACEBOOK_PAGE_ID")

print("=" * 80)
print("  📘 DIRECT FACEBOOK POST")
print("=" * 80)
print(f"\n Token (first 50 chars): {token[:50]}...")
print(f" Page ID: {page_id}")
print(f"\n📝 Posting message...")

message = """🎉 Exciting News from AI Employee Vault!

We're thrilled to announce our latest AI-powered automation features:

✨ Auto-posting to social media
✨ Smart content scheduling
✨ Advanced analytics & insights
✨ Multi-platform support (Facebook, Instagram, LinkedIn)

Boost your productivity today! 🚀

#AIAutomation #Productivity #TechInnovation #BusinessGrowth #AI"""

response = httpx.post(
    f"https://graph.facebook.com/v19.0/{page_id}/feed",
    params={
        'message': message,
        'access_token': token,
        'link': 'https://example.com'
    },
    timeout=30
)

print(f"\n📊 Response Status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("\n✅ POST SUCCESSFUL!")
    print(f"   Post ID: {result.get('id')}")
    print(f"   URL: https://facebook.com/{result.get('id')}")
else:
    print("\n❌ POST FAILED")
    print(f"   Error: {response.json()}")

print("\n" + "=" * 80)
