"""Debug Facebook Token"""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def debug():
    token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    page_id = os.getenv("FACEBOOK_PAGE_ID", "")
    
    print("Token:", token[:50] + "..." if len(token) > 50 else token)
    print("Page ID:", page_id)
    print()
    
    async with httpx.AsyncClient() as client:
        # Try to get me/accounts
        url = "https://graph.facebook.com/v19.0/me/accounts"
        params = {"access_token": token}
        
        print(f"Requesting: {url}")
        try:
            response = await client.get(url, params=params)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(debug())
