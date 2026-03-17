"""
Script to get a proper Facebook Page Access Token
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_page_access_token():
    """Get page-specific access token using the user token"""

    user_access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")

    if not user_access_token:
        print("ERROR: No Facebook access token found in environment variables!")
        return

    if not page_id:
        print("ERROR: No Facebook Page ID found in environment variables!")
        return

    try:
        # Get page access token using the user token
        url = f"https://graph.facebook.com/v19.0/{page_id}?fields=access_token&access_token={user_access_token}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if 'access_token' in data:
                page_token = data['access_token']
                print("SUCCESS: Got Page Access Token!")
                print(f"Page Access Token: {page_token}")
                print("\nTo use this token, update your .env file:")
                print("FACEBOOK_PAGE_ACCESS_TOKEN=NEW_PAGE_TOKEN_HERE")
                print("# Remove or comment out the old FACEBOOK_ACCESS_TOKEN")
                print("\nThen try running the auto-post script again.")

                # Also verify this token works for posting
                print(f"\nVerifying page token permissions...")
                verify_url = f"https://graph.facebook.com/v19.0/debug_token?input_token={page_token}&access_token={user_access_token}"
                verify_response = requests.get(verify_url)

                if verify_response.status_code == 200:
                    verify_data = verify_response.json()
                    token_info = verify_data.get('data', {})
                    scopes = token_info.get('scopes', [])
                    print(f"Page Token Permissions: {scopes}")

                    if 'pages_manage_posts' in scopes and 'pages_read_engagement' in scopes:
                        print("✓ Page token has required permissions for posting!")
                    else:
                        print("✗ Page token is missing required permissions")
                else:
                    print(f"Could not verify page token: {verify_response.text}")

                return page_token
            else:
                print("ERROR: Could not retrieve page access token from the API response.")
                print("This might mean the user doesn't have admin rights to this page.")
                print(f"Response: {data}")
        else:
            print(f"ERROR: Could not get page access token: {response.status_code} - {response.text}")
            print("\nThis could happen if:")
            print("1. The user token doesn't have the pages_manage_posts permission")
            print("2. The user is not an admin of the page")
            print("3. The page ID is incorrect")

    except Exception as e:
        print(f"Error getting page access token: {str(e)}")

if __name__ == "__main__":
    get_page_access_token()