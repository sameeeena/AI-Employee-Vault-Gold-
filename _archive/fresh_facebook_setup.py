"""
FRESH FACEBOOK SETUP GUIDE
===========================

Follow these steps EXACTLY with your NEW Facebook account.
"""

print("=" * 80)
print("  FRESH FACEBOOK SETUP - CLEAN START")
print("=" * 80)
print()

print("STEP 1: Log in to Facebook")
print("-" * 80)
print("  1. Go to: https://www.facebook.com/")
print("  2. Log in with your NEW Facebook account")
print("  3. Make sure this account is ADMIN of your Facebook Page")
print()

input("  Press Enter after logging in...")

print()
print("STEP 2: Create New Facebook App")
print("-" * 80)
print("  1. Go to: https://developers.facebook.com/apps/")
print("  2. Click 'Create App' button (top right)")
print("  3. Select 'Business' as app type")
print("  4. Click 'Next'")
print()
print("  Fill in:")
print("    - App Name: AI Employee Vault")
print("    - App Contact Email: your email")
print("    - (Optional) Business Account: Select if you have one")
print()
print("  5. Click 'Create App'")
print()

input("  Press Enter after creating app...")

print()
print("STEP 3: Add Facebook Login Product")
print("-" * 80)
print("  1. On your App Dashboard, scroll to 'Add Products'")
print("  2. Find 'Facebook Login for Business'")
print("  3. Click 'Set Up'")
print()

input("  Press Enter after adding Facebook Login...")

print()
print("STEP 4: Add Instagram Product (if needed)")
print("-" * 80)
print("  1. In left sidebar, click 'Add Products'")
print("  2. Find 'Instagram Basic Display'")
print("  3. Click 'Set Up'")
print()

input("  Press Enter after adding Instagram...")

print()
print("STEP 5: Get Access Token")
print("-" * 80)
print("  1. Go to: https://developers.facebook.com/tools/explorer/")
print("  2. Select YOUR NEW APP from the dropdown (top)")
print("  3. Click 'Generate Access Token' button")
print()
print("  In the popup, check these permissions:")
print("    Facebook Pages section:")
print("      ✅ pages_manage_posts")
print("      ✅ pages_read_engagement")
print("      ✅ pages_show_list")
print()
print("    Instagram section:")
print("      ✅ instagram_basic")
print("      ✅ instagram_content_publish")
print()
print("  4. Click 'Continue' or 'Generate Token'")
print("  5. Facebook popup → Select your Page → Click 'Done'")
print("  6. COPY the token that appears")
print()

input("  Press Enter after copying token...")

print()
print("STEP 6: Get Your Page ID")
print("-" * 80)
print("  1. Go to your Facebook Page")
print("  2. Look at the URL, or")
print("  3. Go to: https://developers.facebook.com/tools/explorer/")
print("  4. Run query: /me/accounts")
print("  5. Copy your Page ID from results")
print()

input("  Press Enter after getting Page ID...")

print()
print("STEP 7: Update .env File")
print("-" * 80)
print("  Open your .env file and update:")
print()
print("    FACEBOOK_PAGE_ACCESS_TOKEN=<paste your new token here>")
print("    FACEBOOK_PAGE_ID=<your page id>")
print("    FACEBOOK_APP_ID=<your new app id>")
print("    SOCIAL_MOCK_MODE=false  (to post live)")
print()

input("  Press Enter after updating .env...")

print()
print("STEP 8: Test Connection")
print("-" * 80)
print("  Run: python check_facebook_permissions.py")
print()

print("=" * 80)
print("  DONE! Your fresh setup is complete.")
print("=" * 80)
print()

input("Press Enter to exit...")
