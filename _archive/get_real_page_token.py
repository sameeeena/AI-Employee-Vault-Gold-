"""
Script to get the proper page access token for your Facebook page
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_proper_page_token():
    """Get the proper page access token"""

    user_access_token = os.getenv("FACEBOOK_ACCESS_TOKEN") or os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    # Use the page ID that we confirmed we have access to
    page_id = "991032867435060"  # AI Employee Vault page

    print(f"Getting page access token for page ID: {page_id}")

    try:
        # The endpoint to get page access token is different
        url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={user_access_token}&fields=access_token"
        response = requests.get(url)

        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Response data: {data}")

            if 'access_token' in data:
                page_token = data['access_token']
                print(f"SUCCESS: Got page access token!")
                print(f"Page Token: {page_token[:50]}...")  # Show first 50 chars for security
                print("\nTo use this token:")
                print("1. Update your .env file:")
                print("   FACEBOOK_PAGE_ACCESS_TOKEN=THIS_NEW_TOKEN")
                print("2. Comment out or remove the old FACEBOOK_ACCESS_TOKEN")
                print("3. Try posting again")

                # Test if this token works
                print("\nTesting the new token...")
                test_url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={page_token}"
                test_response = requests.get(test_url)

                if test_response.status_code == 200:
                    print("✓ New token successfully accesses the page")
                else:
                    print(f"✗ New token failed to access page: {test_response.status_code}")

                return page_token
            else:
                print("ERROR: Response did not contain access_token")
                print("This could mean:")
                print("1. The user token doesn't have the right permissions")
                print("2. The user is not an admin of this page")
                print("3. The fields parameter is not supported for this page")
        else:
            print(f"ERROR: Could not get page access token: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error details: {response.text}")

    except Exception as e:
        print(f"Error getting page access token: {str(e)}")

if __name__ == "__main__":
    get_proper_page_token()