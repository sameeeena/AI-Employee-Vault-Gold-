"""
Facebook Token Refresh - Quick Guide

Ye script aapko naya Facebook Page Access Token lene mein madad karegi.
"""

import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("FACEBOOK_APP_ID", "818482444607294")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "991032867435060")

print("=" * 80)
print("  🔄 FACEBOOK ACCESS TOKEN REFRESH")
print("=" * 80)
print()
print("⚠️  Aapka Facebook access token expire ho gaya hai.")
print()
print("=" * 80)
print("  📋 STEP-BY-STEP INSTRUCTIONS")
print("=" * 80)
print()
print("STEP 1: Facebook Graph API Explorer open karein")
print("-" * 80)
print("URL: https://developers.facebook.com/tools/explorer/")
print()

# Open the URL
open_browser = input("Open karein? (y/n): ").strip().lower()
if open_browser == 'y':
    webbrowser.open("https://developers.facebook.com/tools/explorer/")
    print("✅ Browser open ho gaya!")

print()
print("STEP 2: Access Token generate karein")
print("-" * 80)
print("1. 'Get Token' button par click karein")
print("2. 'Get User Access Token' select karein")
print("3. Neeche diye gaye permissions select karein:")
print("   ✓ pages_manage_posts")
print("   ✓ pages_read_engagement")
print("   ✓ pages_show_list")
print("4. 'Generate Token' par click karein")
print("5. Facebook login karein (agar needed)")
print("6. Apni Page select karein aur permissions approve karein")
print()

print("STEP 3: Page Access Token lein")
print("-" * 80)
print("1. Graph API Explorer mein query box mein likhein:")
print(f"   /{PAGE_ID}?fields=access_token")
print()
print("2. 'Submit' par click karein")
print()
print("3. Response mein 'access_token' dikhega:")
print("   {")
print("     \"access_token\": \"EAALoZA... (long token)\",")
print("     \"id\": \"991032867435060\"")
print("   }")
print()
print("4. Is access_token ko COPY karein")
print()

print("STEP 4: .env file update karein")
print("-" * 80)
print("1. .env file open karein")
print("2. FACEBOOK_PAGE_ACCESS_TOKEN line dhundhein")
print("3. Purana token hatakar naya token paste karein")
print()
print("   FACEBOOK_PAGE_ACCESS_TOKEN=EAALoZA... (naya token)")
print()

print("STEP 5: Test karein")
print("-" * 80)
print("Command run karein:")
print("   python facebook_autopost_now.py --template 1")
print()

print("=" * 80)
print("  QUICK LINKS")
print("=" * 80)
print()
print(f"Graph API Explorer: https://developers.facebook.com/tools/explorer/")
print(f"Your Page ID: {PAGE_ID}")
print(f"Your App ID: {APP_ID}")
print()
print("=" * 80)
