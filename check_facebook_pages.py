"""
Check Connected Facebook Pages

Yeh script check karegi ki aapka Developer App kin Facebook Pages se connected hai.
"""

import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = "1275203508084665"

def main():
    print("=" * 70)
    print("  CHECK CONNECTED FACEBOOK PAGES")
    print("=" * 70)
    print()
    print("📋 Aapke paas:")
    print(f"   - Developer App ID: {APP_ID}")
    print(f"   - Facebook Page ID: 61585659193997")
    print()
    print("=" * 70)
    print("  STEP 1: Check Karein - App Page se Connected Hai?")
    print("=" * 70)
    print()
    
    # Graph API Explorer link
    explorer_url = f"https://developers.facebook.com/tools/explorer/{APP_ID}/"
    
    print("🔗 Graph API Explorer open karein:")
    print(f"   {explorer_url}")
    print()
    
    open_explorer = input("Graph API Explorer open karein? (y/n): ").strip().lower()
    if open_explorer == 'y':
        webbrowser.open(explorer_url)
    
    print()
    print("=" * 70)
    print("  STEP 2: Query Chalayein")
    print("=" * 70)
    print()
    print("Graph API Explorer mein:")
    print()
    print("   1. 'GET' dropdown select karein")
    print("   2. Query box mein likhein: /me/accounts")
    print("   3. 'Submit' button click karein")
    print()
    print("   Agar aapka Page dikha (61585659193997), toh ✅ Connected hai!")
    print("   Agar empty response aaya, toh ❌ Not Connected")
    print()
    
    print("=" * 70)
    print("  STEP 3: Agar NOT Connected Hai")
    print("=" * 70)
    print()
    print("Solution:")
    print()
    print("   1. Facebook pe jayein: https://www.facebook.com/")
    print("   2. Apne Page pe jayein: https://www.facebook.com/61585659193997")
    print("   3. Make sure aap Admin hain")
    print("   4. Phir Graph API Explorer mein /me/accounts try karein")
    print()
    
    print("=" * 70)
    print("  DIRECT TOKEN LINK")
    print("=" * 70)
    print()
    
    direct_link = f"https://www.facebook.com/v19.0/dialog/oauth?client_id={APP_ID}&scope=pages_manage_posts,pages_read_engagement,pages_show_list&response_type=token&display=page"
    
    print("🔗 Direct Token Link:")
    print(f"   {direct_link}")
    print()
    
    open_token = input("Token link open karein? (y/n): ").strip().lower()
    if open_token == 'y':
        webbrowser.open(direct_link)
    
    print()
    print("=" * 70)
    print("  NEXT")
    print("=" * 70)
    print()
    print("Token milne ke baad:")
    print("   1. .env file edit karein")
    print("   2. FACEBOOK_PAGE_ACCESS_TOKEN update karein")
    print("   3. FACEBOOK_PAGE_ID update karein")
    print("   4. Run: python test_facebook_connection.py")
    print()

if __name__ == "__main__":
    main()
