"""
Get New Facebook Page Access Token

This script helps you get a new Facebook Page Access Token.
It will open the Graph API Explorer in your browser.

Usage:
    python get_new_facebook_token.py
"""

import webbrowser
import sys


def main():
    print("=" * 80)
    print("  📘 FACEBOOK TOKEN GETTER")
    print("=" * 80)
    print()
    print("This will open Facebook Graph API Explorer in your browser.")
    print()
    print("=" * 80)
    print("  STEPS:")
    print("=" * 80)
    print()
    print("  1. Graph API Explorer will open")
    print("  2. Select app: 1275203508084665")
    print("  3. Click 'Get Token' → 'Get Page Access Token'")
    print("  4. Select your Facebook Page")
    print("  5. In the query box, type: GET /me/accounts")
    print("  6. Click 'Submit'")
    print("  7. Copy the 'access_token' and 'id' from results")
    print("  8. Update .env file with new values")
    print()
    print("=" * 80)
    
    confirm = input("Open Graph API Explorer now? (y/n): ")
    
    if confirm.lower() == 'y':
        # Open Graph API Explorer
        url = "https://developers.facebook.com/tools/explorer/"
        print(f"\nOpening: {url}")
        webbrowser.open(url)
        
        print("\n✅ Browser opened!")
        print("\nFollow the steps above to get your new token.")
        print("\nAfter getting the token, update .env file:")
        print("  FACEBOOK_PAGE_ACCESS_TOKEN=your_new_token")
        print("  FACEBOOK_PAGE_ID=your_page_id")
        print("\nThen test with:")
        print("  python facebook_autopost_now.py --template 1")
        
    else:
        print("\nCancelled. Run this script again when ready.")
    
    print("\n" + "=" * 80)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
