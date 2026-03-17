"""
Find Your Correct Facebook Page ID

Uses your access token to fetch the actual Page ID.
"""

import httpx
import json
from dotenv import load_dotenv
import os

load_dotenv()

async def find_page_id():
    print("=" * 60)
    print("  FINDING YOUR FACEBOOK PAGE ID")
    print("=" * 60)
    
    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    
    if not access_token:
        print("\n❌ No access token found in .env")
        return
    
    print("\n🔑 Token found, fetching your pages...")
    
    async with httpx.AsyncClient() as client:
        try:
            # Get pages managed by this token
            url = "https://graph.facebook.com/v19.0/me/accounts"
            params = {"access_token": access_token}
            
            response = await client.get(url, params=params)
            data = response.json()
            
            if "error" in data:
                print(f"\n❌ API Error: {data['error']['message']}")
                return
            
            pages = data.get("data", [])
            
            if not pages:
                print("\n⚠️  No pages found. Check token permissions.")
                return
            
            print(f"\n✅ Found {len(pages)} page(s):\n")
            
            for i, page in enumerate(pages, 1):
                print(f"{i}. {page['name']}")
                print(f"   ID: {page['id']}")
                print(f"   Access Token: {page['access_token'][:50]}...")
                print()
            
            # Update .env with first page
            if len(pages) == 1:
                print("=" * 60)
                print("  RECOMMENDATION")
                print("=" * 60)
                print(f"\n📍 Update .env with:")
                print(f"   FACEBOOK_PAGE_ID={pages[0]['id']}")
                print()
                
                response = input("Auto-update .env? (y/n): ").strip().lower()
                if response == 'y':
                    update_env(pages[0]['id'], pages[0]['access_token'])
            else:
                print("Select a page to update .env (or 0 to skip):")
                choice = input("Page number: ").strip()
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(pages):
                        update_env(pages[idx]['id'], pages[idx]['access_token'])
                except:
                    pass
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

def update_env(page_id, page_token):
    """Update .env file with page ID and token"""
    env_file = ".env"
    
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Update page ID
        if "FACEBOOK_PAGE_ID=" in content:
            import re
            content = re.sub(r'FACEBOOK_PAGE_ID=.*', f'FACEBOOK_PAGE_ID={page_id}', content)
        else:
            content += f"\nFACEBOOK_PAGE_ID={page_id}"
        
        # Update token
        if "FACEBOOK_PAGE_ACCESS_TOKEN=" in content:
            import re
            content = re.sub(r'FACEBOOK_PAGE_ACCESS_TOKEN=.*', f'FACEBOOK_PAGE_ACCESS_TOKEN={page_token}', content)
        else:
            content += f"\nFACEBOOK_PAGE_ACCESS_TOKEN={page_token}"
        
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"\n✅ .env updated!")
        print(f"   FACEBOOK_PAGE_ID={page_id}")
        print(f"   FACEBOOK_PAGE_ACCESS_TOKEN={page_token[:50]}...")
        
    except Exception as e:
        print(f"\n⚠️  Could not update .env: {str(e)}")
        print(f"\nManual update required:")
        print(f"   FACEBOOK_PAGE_ID={page_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(find_page_id())
