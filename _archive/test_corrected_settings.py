"""
Test Facebook Post Script
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_facebook_post():
    """Test posting to Facebook with the corrected settings"""

    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")

    print(f"Using Page ID: {page_id}")
    print(f"Access token length: {len(access_token) if access_token else 0} characters")

    # Test if we can access the page
    try:
        page_url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={access_token}"
        page_response = requests.get(page_url)

        if page_response.status_code == 200:
            page_data = page_response.json()
            print(f"✓ Successfully connected to page: {page_data.get('name', 'Unknown Page')}")
        else:
            print(f"✗ Failed to connect to page: {page_response.status_code}")
            print(f"  Response: {page_response.text}")
            return

        # Now try to post
        message = "Test post from AI Employee Vault - Corrected settings!"

        post_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
        post_data = {
            'message': message,
            'access_token': access_token
        }

        print("Attempting to post...")
        post_response = requests.post(post_url, data=post_data)

        if post_response.status_code == 200:
            result = post_response.json()
            print(f"✓ SUCCESS! Post created with ID: {result.get('id')}")
            print(f"  Post URL: https://facebook.com/{result.get('id')}")
        else:
            print(f"✗ FAILED to post: {post_response.status_code}")
            print(f"  Response: {post_response.text}")

    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_facebook_post()