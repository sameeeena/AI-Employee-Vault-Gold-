"""
Get Instagram Business ID - Helper Script

This script helps you get your Instagram Business ID.
It will open Graph API Explorer and guide you through the process.

Usage:
    python get_instagram_id.py
"""

import webbrowser
import json
from dotenv import load_dotenv
import os

load_dotenv()


def print_step(step_num, title):
    """Print formatted step header"""
    print(f"\n{'=' * 80}")
    print(f"  STEP {step_num}: {title}")
    print(f"{'=' * 80}")


def main():
    print("=" * 80)
    print("  📷 INSTAGRAM BUSINESS ID GETTER")
    print("=" * 80)
    print()
    print("This script will help you get your Instagram Business ID.")
    print()
    
    # Check prerequisites
    print_step(0, "Prerequisites Check")
    
    facebook_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    facebook_page_id = os.getenv("FACEBOOK_PAGE_ID", "")
    
    print(f"✓ Facebook Page Access Token: {'✅ Found' if facebook_token else '❌ Missing'}")
    print(f"✓ Facebook Page ID: {'✅ Found' if facebook_page_id else '❌ Missing'}")
    
    if not facebook_token or not facebook_page_id:
        print("\n⚠️  WARNING: Facebook credentials missing in .env file!")
        print("   Please configure Facebook first before getting Instagram ID.")
    
    print()
    input("Press Enter to continue...")
    
    # Step 1: Open Graph API Explorer
    print_step(1, "Open Graph API Explorer")
    
    print("\nOpening Facebook Graph API Explorer...")
    url = "https://developers.facebook.com/tools/explorer/"
    print(f"URL: {url}")
    
    confirm = input("Open in browser? (y/n): ")
    
    if confirm.lower() == 'y':
        webbrowser.open(url)
        print("\n✅ Browser opened!")
    else:
        print("\n⚠️  Please open Graph API Explorer manually.")
    
    # Step 2: Instructions
    print_step(2, "Get Page Access Token")
    
    print("""
In Graph API Explorer:

1. Select App: 1275203508084665

2. Click "Get Token" → "Get Page Access Token"

3. Select your Facebook Page

4. Check these permissions:
   ✅ pages_manage_posts
   ✅ pages_read_engagement
   ✅ pages_show_list
   ✅ instagram_basic
   ✅ instagram_content_publish

5. Click "Get Access Token"
""")
    
    input("Press Enter when done...")
    
    # Step 3: Get Page ID
    print_step(3, "Get Your Page ID")
    
    print("""
In the query box, type:

   GET /me/accounts

Then click "Submit"
""")
    
    input("Press Enter when done...")
    
    print("""
You should see a response like:

{
  "data": [
    {
      "access_token": "EAASHynQdn7kBQ...",
      "id": "61585659193997",
      "name": "Your Page Name"
    }
  ]
}

📋 Copy the "id" value (this is your Facebook Page ID)
""")
    
    facebook_id = input("Enter your Facebook Page ID (or press Enter to skip): ").strip()
    
    if facebook_id:
        print(f"✓ Facebook Page ID: {facebook_id}")
    else:
        facebook_id = facebook_page_id
        print(f"✓ Using existing Facebook Page ID: {facebook_id}")
    
    input("Press Enter to continue...")
    
    # Step 4: Get Instagram Business ID
    print_step(4, "Get Instagram Business ID")
    
    print(f"""
In the query box, type:

   GET /{facebook_id}?fields=instagram_business_account

Then click "Submit"
""")
    
    input("Press Enter when done...")
    
    print("""
You should see a response like:

{
  "instagram_business_account": {
    "id": "17841405822304915"
  }
}

📋 Copy the "id" value (this is your Instagram Business ID!)
""")
    
    instagram_id = input("Enter your Instagram Business ID: ").strip()
    
    if instagram_id:
        print(f"\n✅ Instagram Business ID: {instagram_id}")
    else:
        print("\n⚠️  Instagram Business ID not entered.")
        print("   Make sure Instagram is connected to your Facebook Page.")
    
    # Step 5: Update .env
    print_step(5, "Update .env File")
    
    print("""
Open .env file and add/update these lines:

# Instagram Configuration
INSTAGRAM_USER_ID={instagram_id}
INSTAGRAM_ACCESS_TOKEN={facebook_token}

# Change Mock Mode to false
SOCIAL_MOCK_MODE=false
""".replace("{instagram_id}", instagram_id if instagram_id else "YOUR_INSTAGRAM_ID")
   .replace("{facebook_token}", "YOUR_FACEBOOK_TOKEN (already in .env)"))
    
    if instagram_id:
        print(f"\n💡 Quick Update:")
        print(f"   INSTAGRAM_USER_ID={instagram_id}")
        print(f"   INSTAGRAM_ACCESS_TOKEN=(same as FACEBOOK_PAGE_ACCESS_TOKEN)")
        print(f"   SOCIAL_MOCK_MODE=false")
    
    input("Press Enter to continue...")
    
    # Step 6: Test
    print_step(6, "Test Instagram Autopost")
    
    print("""
Run this command to test:

   python instagram_autopost_now.py --template 1

If successful, you'll see:
   ✅ INSTAGRAM POST SUCCESSFUL!
""")
    
    # Final Summary
    print("=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"""
✅ Facebook Page ID: {facebook_id}
✅ Instagram Business ID: {instagram_id if instagram_id else 'Not entered'}
✅ Access Token: (same as Facebook Page Access Token)

Next Steps:
1. Update .env file with Instagram Business ID
2. Set SOCIAL_MOCK_MODE=false
3. Run: python instagram_autopost_now.py --template 1
""")
    
    print("=" * 80)
    print("\n📖 Full Guide: INSTAGRAM_ID_TOKEN_GUIDE.md")
    print("\n🎉 You're all set!")
    print("=" * 80)
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
