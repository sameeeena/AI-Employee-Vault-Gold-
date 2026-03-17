"""
Script to check Facebook access token permissions
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_token_permissions():
    """Check permissions of the Facebook access token"""

    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not access_token:
        print("ERROR: No Facebook access token found in environment variables!")
        return

    try:
        # Check token information
        url = f"https://graph.facebook.com/v19.0/debug_token?input_token={access_token}&access_token={access_token}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            token_info = data.get('data', {})

            print("TOKEN INFORMATION:")
            print(f"Type: {token_info.get('type', 'N/A')}")
            print(f"Expires at: {token_info.get('expires_at', 'N/A')}")
            print(f"Is valid: {token_info.get('is_valid', 'N/A')}")
            print(f"App ID: {token_info.get('app_id', 'N/A')}")
            print(f"User ID: {token_info.get('user_id', 'N/A')}")

            permissions = token_info.get('scopes', [])
            print(f"\nPERMISSIONS: {permissions}")

            required_permissions = ['pages_manage_posts', 'pages_read_engagement']
            missing_permissions = [perm for perm in required_permissions if perm not in permissions]

            if missing_permissions:
                print(f"\nMISSING REQUIRED PERMISSIONS: {missing_permissions}")
                print("\nTo fix this, you need to:")
                print("1. Go to your Facebook App Dashboard")
                print("2. Navigate to your app's permissions")
                print("3. Request the missing permissions")
                print("4. Have an admin approve them")
            else:
                print("\nAll required permissions are present!")

        else:
            print(f"Error checking token: {response.status_code} - {response.text}")
            print("\nThe token might be expired or invalid.")

            # Try to get basic info about the page with the token
            page_id = os.getenv("FACEBOOK_PAGE_ID")
            if page_id:
                page_url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={access_token}"
                page_response = requests.get(page_url)

                if page_response.status_code == 200:
                    print(f"\nSuccessfully connected to page: {page_response.json().get('name', 'Unknown')}")
                    print("However, posting permissions seem to be missing.")
                else:
                    print(f"\nCould not access page {page_id} with current token.")

    except Exception as e:
        print(f"Error checking token permissions: {str(e)}")

if __name__ == "__main__":
    check_token_permissions()