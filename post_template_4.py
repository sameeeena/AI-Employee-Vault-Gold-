"""
Facebook Post - Template 4 (Industry Insights)
"""
from dotenv import load_dotenv
import os
import httpx

load_dotenv(override=True)

token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
page_id = os.getenv("FACEBOOK_PAGE_ID")

print("=" * 80)
print("  📘 FACEBOOK POST - TEMPLATE 4")
print("=" * 80)

message = """📊 Industry Insight 2026!

AI automation is transforming how businesses operate:

📈 73% of companies report increased productivity
⏰ Average 40% time savings on repetitive tasks
💰 ROI improves by 2-3x within first year
🎯 Customer satisfaction up by 55%

Stay ahead of the curve with AI Employee Vault!

#AI #BusinessIntelligence #Automation #DigitalTransformation #FutureOfWork"""

print(f"\n📝 Posting to Page: {page_id}")
print(f"\n📄 Message:")
print("-" * 80)
print(message)
print("-" * 80)

response = httpx.post(
    f"https://graph.facebook.com/v19.0/{page_id}/feed",
    params={
        'message': message,
        'access_token': token
    },
    timeout=30
)

print(f"\n📊 Response: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print("\n✅ POST SUCCESSFUL!")
    print(f"   Post ID: {result.get('id')}")
    print(f"\n🔗 View Post:")
    print(f"   https://www.facebook.com/{result.get('id')}")
else:
    print("\n❌ POST FAILED")
    print(f"   Error: {response.json()}")

print("\n" + "=" * 80)
