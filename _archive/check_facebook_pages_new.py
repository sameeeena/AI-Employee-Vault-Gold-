"""Check Facebook Pages from Token"""
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def check_pages():
    token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    
    print("=" * 70)
    print("  CHECKING YOUR FACEBOOK PAGES")
    print("=" * 70)
    print()
    
    async with httpx.AsyncClient() as client:
        # Get pages
        url = "https://graph.facebook.com/v19.0/me/accounts"
        params = {"access_token": token}
        
        print("📍 Fetching pages...")
        response = await client.get(url, params=params)
        data = response.json()
        
        if "error" in data:
            print(f"\n❌ Error: {data['error']['message']}")
            return
        
        pages = data.get("data", [])
        
        if not pages:
            print("\n⚠️  No pages found!")
            print("\nPossible reasons:")
            print("   1. Token expired")
            print("   2. You're not admin of any page")
            print("   3. Token doesn't have pages_show_list permission")
        else:
            print(f"\n✅ Found {len(pages)} page(s):\n")
            for i, page in enumerate(pages, 1):
                print(f"{i}. {page.get('name', 'Unknown')}")
                print(f"   ID: {page.get('id')}")
                print(f"   Token: {page.get('access_token', '')[:50]}...")
                print()
            
            print("=" * 70)
            print("  RECOMMENDATION")
            print("=" * 70)
            print()
            print("Update .env with the correct Page ID:")
            print(f"   FACEBOOK_PAGE_ID={pages[0]['id']}")
            print()
            
            # Auto-update option
            update = input("Auto-update .env? (y/n): ").strip().lower()
            if update == 'y':
                update_env(pages[0]['id'], pages[0].get('access_token', token))
                print("\n✅ .env updated! Run test again.")

def update_env(page_id, page_token):
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
    
    import re
    content = re.sub(r'FACEBOOK_PAGE_ID=.*', f'FACEBOOK_PAGE_ID={page_id}', content)
    content = re.sub(r'FACEBOOK_PAGE_ACCESS_TOKEN=.*', f'FACEBOOK_PAGE_ACCESS_TOKEN={page_token}', content)
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_pages())
