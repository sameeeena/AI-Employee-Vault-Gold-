"""
Simple script to fetch your Facebook Page ID using the access token
"""

import os
import httpx
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_facebook_pages():
    """Get list of Facebook pages associated with the access token"""

    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not access_token:
        print("ERROR: No Facebook access token found in environment variables!")
        print("Please make sure FACEBOOK_PAGE_ACCESS_TOKEN or FACEBOOK_ACCESS_TOKEN is set in your .env file")
        return

    try:
        import urllib.parse
        # Build the URL manually to avoid encoding issues
        base_url = "https://graph.facebook.com/v19.0/me/accounts"
        params = {
            'access_token': access_token,
            'fields': 'name,id,category,perms'
        }

        # Manually construct query string to avoid encoding issues
        query_string = urllib.parse.urlencode(params)
        url = f"{base_url}?{query_string}"

        import requests  # Using requests instead of httpx to avoid async issues
        response = requests.get(url)

        if response.status_code != 200:
            print(f"ERROR: HTTP {response.status_code}")
            print(f"Response: {response.text}")

            # Try with the page token directly if the user token doesn't work
            print("\nTrying to access page directly with your PAGE access token...")
            page_id_url = f"https://graph.facebook.com/v19.0/me?access_token={access_token}"
            page_response = requests.get(page_id_url)

            if page_response.status_code == 200:
                page_data = page_response.json()
                if 'id' in page_data:
                    print(f"SUCCESS: Found page with ID: {page_data['id']}")
                    print("This is likely your page ID, update your .env file with:")
                    print(f"FACEBOOK_PAGE_ID={page_data['id']}")
                else:
                    print("Could not get page ID from token")
            else:
                print(f"Direct page access also failed: {page_response.text}")
            return

        data = response.json()

        print("Facebook Pages Associated with Your Token:")
        print("=" * 50)

        if 'data' in data and len(data['data']) > 0:
            for i, page in enumerate(data['data'], 1):
                print(f"{i}. Page Name: {page.get('name', 'N/A')}")
                print(f"   Page ID: {page.get('id', 'N/A')}")
                print(f"   Category: {page.get('category', 'N/A')}")
                print(f"   Permissions: {', '.join(page.get('perms', []))}")
                print("-" * 30)

            print("\nUpdate your .env file with the correct Page ID")
            print("Set: FACEBOOK_PAGE_ID=correct_page_id_here")
        else:
            print("No pages found associated with this access token.")
            print("\nPossible reasons:")
            print("1. The access token is not a Page token but a User token")
            print("2. The user doesn't have admin rights to any Facebook pages")
            print("3. The page hasn't been properly connected to the app")

    except Exception as e:
        print(f"Error fetching pages: {str(e)}")

if __name__ == "__main__":
    get_facebook_pages()