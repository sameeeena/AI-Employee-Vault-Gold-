"""
Facebook Token Troubleshooting Guide
"""

print("=" * 80)
print("  FACEBOOK TOKEN TROUBLESHOOTING")
print("=" * 80)
print()

print("❓ WHAT HAPPENS WHEN YOU TRY TO GET A TOKEN?")
print()
print("Choose what you see:")
print()
print("  1. No 'Get User Access Token' button visible")
print("  2. Popup appears but no permission tabs")
print("  3. Error when clicking Generate Token")
print("  4. Facebook login page keeps looping")
print("  5. 'App not in Live mode' error")
print("  6. Permission request gets rejected")
print("  7. Something else")
print()

choice = input("Enter number (1-7): ").strip()

print()
print("=" * 80)
print("  SOLUTION:")
print("=" * 80)
print()

if choice == "1":
    print("📍 NO BUTTON VISIBLE")
    print()
    print("Try this:")
    print("  1. Make sure you selected your APP from the top dropdown")
    print("  2. Look for a button that says 'Generate Access Token' (not 'Get User')")
    print("  3. Try clicking the '+' icon or 'Add Permission' button")
    print()
    print("Alternative: Use this direct link:")
    print("  https://developers.facebook.com/tools/explorer/permissions/")
    print()

elif choice == "2":
    print("📍 POPUP BUT NO TABS")
    print()
    print("The popup may show a SCROLLABLE list instead of tabs:")
    print("  - Scroll DOWN in the popup")
    print("  - Look for 'pages_manage_posts' in the list")
    print("  - Check the boxes next to each permission")
    print()

elif choice == "3":
    print("📍 ERROR ON GENERATE")
    print()
    print("Common errors:")
    print("  - 'App not configured for Facebook Login'")
    print("    → Go to App Dashboard → Add Product → Facebook Login → Set Up")
    print()
    print("  - 'Domain not whitelisted'")
    print("    → Go to App Settings → Basic → Add your domain")
    print()

elif choice == "4":
    print("📍 LOGIN LOOP")
    print()
    print("Fix:")
    print("  1. Log out of Facebook completely")
    print("  2. Clear browser cache/cookies")
    print("  3. Open Incognito/Private window")
    print("  4. Go to Graph API Explorer")
    print("  5. Log in fresh")
    print()

elif choice == "5":
    print("📍 APP NOT IN LIVE MODE")
    print()
    print("Fix:")
    print("  1. Go to: https://developers.facebook.com/apps/")
    print("  2. Select your app")
    print("  3. Look for toggle at top: 'Development Mode' → Switch to 'Live'")
    print("  4. You may need to complete App Review first")
    print()

elif choice == "6":
    print("📍 PERMISSIONS REJECTED")
    print()
    print("Some permissions need Facebook approval:")
    print("  - For TESTING, you can use them in Development mode")
    print("  - For PRODUCTION, submit for App Review")
    print()
    print("For now, just make sure App is in Development mode for testing")
    print()

else:
    print("📍 DESCRIBE YOUR ISSUE:")
    print()
    print("Tell me exactly:")
    print("  - What page do you see?")
    print("  - What error message appears?")
    print("  - What happens when you click buttons?")
    print()

print()
print("=" * 80)
input("Press Enter to exit...")
