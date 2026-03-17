"""
Script to verify the relationship between your access token and Facebook page
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_page_and_token():
    """Verify if the token and page ID are correctly matched"""

    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")

    if not access_token:
        print("ERROR: No Facebook access token found in environment variables!")
        return

    if not page_id:
        print("ERROR: No Facebook Page ID found in environment variables!")
        return

    print(f"Testing connection between token and page ID {page_id}...")

    try:
        # First, try to get page info directly
        page_url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={access_token}"
        page_response = requests.get(page_url)

        if page_response.status_code == 200:
            page_data = page_response.json()
            print(f"✓ Successfully accessed page: {page_data.get('name', 'Unknown Page')}")
            print(f"  Page ID: {page_data.get('id', 'Unknown')}")
            print(f"  Category: {page_data.get('category', 'Unknown')}")
        else:
            print(f"✗ Could not access page with provided ID and token: {page_response.status_code}")
            print(f"  Response: {page_response.json()}")
            return

        # Try to get the user's pages to see if the current page ID is in the list
        accounts_url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={access_token}"
        accounts_response = requests.get(accounts_url)

        if accounts_response.status_code == 200:
            accounts_data = accounts_response.json()
            if 'data' in accounts_data:
                print(f"\nPages accessible with your token: {len(accounts_data['data'])}")
                found_page = False
                for i, page in enumerate(accounts_data['data'], 1):
                    print(f"  {i}. {page.get('name', 'Unknown')} (ID: {page.get('id', 'Unknown')})")
                    if str(page.get('id')) == str(page_id):
                        found_page = True
                        print(f"     ✓ This is your configured page!")
                        print(f"     Permissions: {', '.join(page.get('perms', []))}")

                if not found_page:
                    print(f"\n⚠️  WARNING: The page ID in your .env ({page_id}) was NOT found in the list of pages accessible with your token.")
                    print("   This explains why posting is failing.")
                    print("   You need to either:")
                    print("   1. Update your .env with a page ID from the list above, OR")
                    print("   2. Get a token that has access to your intended page")
            else:
                print("✗ No pages found accessible with your token.")
        else:
            print(f"✗ Could not fetch user's pages: {accounts_response.status_code}")
            print(f"  Response: {accounts_response.json()}")

    except Exception as e:
        print(f"Error verifying page and token: {str(e)}")

if __name__ == "__main__":
    verify_page_and_token()