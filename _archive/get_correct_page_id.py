"""
Script to fetch your Facebook Page ID using the access token
"""

import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def get_facebook_pages():
    """Get list of Facebook pages associated with the access token"""

    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")

    if not access_token:
        print("❌ No Facebook access token found in environment variables!")
        print("Please make sure FACEBOOK_PAGE_ACCESS_TOKEN or FACEBOOK_ACCESS_TOKEN is set in your .env file")
        return

    try:
        async with httpx.AsyncClient() as client:
            # Get pages associated with the user token
            url = "https://graph.facebook.com/v19.0/me/accounts"
            params = {
                'access_token': access_token,
                'fields': 'name,id,category,perms'
            }

            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            print("📋 Facebook Pages Associated with Your Token:")
            print("=" * 60)

            if 'data' in data and len(data['data']) > 0:
                for i, page in enumerate(data['data'], 1):
                    print(f"{i}. Page Name: {page.get('name', 'N/A')}")
                    print(f"   Page ID: {page.get('id', 'N/A')}")
                    print(f"   Category: {page.get('category', 'N/A')}")
                    print(f"   Permissions: {', '.join(page.get('perms', []))}")
                    print("-" * 40)

                print("\n💡 Update your .env file with the correct Page ID")
                print("Set: FACEBOOK_PAGE_ID=correct_page_id_here")
            else:
                print("❌ No pages found associated with this access token.")
                print("\nPossible reasons:")
                print("1. The access token is not a Page token but a User token")
                print("2. The user doesn't have admin rights to any Facebook pages")
                print("3. The page hasn't been properly connected to the app")

    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error: {e.response.status_code}")
        print(f"Response: {e.response.text}")
    except Exception as e:
        print(f"❌ Error fetching pages: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(get_facebook_pages())