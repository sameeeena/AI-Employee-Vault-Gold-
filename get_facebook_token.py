"""
Facebook Page Access Token Generator

Direct OAuth link generate karta hai token ke liye.
"""

import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()

# App configuration
APP_ID = os.getenv("FACEBOOK_APP_ID", "1275203508084665")

# Required permissions
PERMISSIONS = "pages_manage_posts,pages_read_engagement,pages_show_list,pages_manage_metadata"

def generate_oauth_link():
    """OAuth link generate karein"""
    
    redirect_uri = "https://developers.facebook.com/tools/explorer"
    
    oauth_url = (
        f"https://www.facebook.com/v19.0/dialog/oauth?"
        f"client_id={APP_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={PERMISSIONS}"
        f"&response_type=token"
    )
    
    return oauth_url

def main():
    print("=" * 70)
    print("  FACEBOOK PAGE ACCESS TOKEN GENERATOR")
    print("=" * 70)
    print()
    print("📋 Instructions:")
    print()
    print("1. Neeche diya gaya link open karein")
    print("2. Facebook login karein (agar nahi kiya)")
    print("3. Permissions approve karein")
    print("4. Graph API Explorer pe redirect hoga")
    print("5. Query box mein likhein: /me/accounts")
    print("6. Submit click karein")
    print("7. Response mein se 'access_token' copy karein")
    print("8. .env file mein update karein")
    print()
    print("=" * 70)
    
    oauth_link = generate_oauth_link()
    
    print("\n🔗 OAuth Link:")
    print(oauth_link)
    print()
    
    # Browser open karein
    open_browser = input("Link browser mein open karein? (y/n): ").strip().lower()
    if open_browser == 'y':
        print("\n🌐 Browser open ho raha hai...")
        webbrowser.open(oauth_link)
    
    print("\n" + "=" * 70)
    print("  NEXT STEPS")
    print("=" * 70)
    print()
    print("Token milne ke baad:")
    print()
    print("1. .env file edit karein")
    print("2. Ye lines update karein:")
    print()
    print(f"   FACEBOOK_PAGE_ACCESS_TOKEN=YOUR_TOKEN_HERE")
    print(f"   FACEBOOK_PAGE_ID=YOUR_PAGE_ID_HERE")
    print()
    print("3. Test karein:")
    print("   python test_facebook_connection.py")
    print()
    print("=" * 70)
    
    # .env update karne ka option
    print("\nKya aap .env file update karna chahte hain? (y/n): ")
    update_env = input().strip().lower()
    
    if update_env == 'y':
        token = input("\nAccess token paste karein: ").strip()
        page_id = input("Page ID paste karein: ").strip()
        
        if token and page_id:
            update_env_file(token, page_id)
            print("\n✅ .env updated!")
            print("\nAb test karein: python test_facebook_connection.py")
        else:
            print("\n⚠️  Token ya Page ID khali hai")

def update_env_file(token, page_id):
    """.env file mein token update karein"""
    env_file = ".env"
    
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        import re
        
        # Update Page Access Token
        if "FACEBOOK_PAGE_ACCESS_TOKEN=" in content:
            content = re.sub(
                r'FACEBOOK_PAGE_ACCESS_TOKEN=.*',
                f'FACEBOOK_PAGE_ACCESS_TOKEN={token}',
                content
            )
        else:
            content += f"\nFACEBOOK_PAGE_ACCESS_TOKEN={token}"
        
        # Update Page ID
        if "FACEBOOK_PAGE_ID=" in content:
            content = re.sub(
                r'FACEBOOK_PAGE_ID=.*',
                f'FACEBOOK_PAGE_ID={page_id}',
                content
            )
        else:
            content += f"\nFACEBOOK_PAGE_ID={page_id}"
        
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(content)
        
    except Exception as e:
        print(f"\n❌ Error updating .env: {str(e)}")
        print("\nManual update required:")
        print(f"   FACEBOOK_PAGE_ACCESS_TOKEN={token}")
        print(f"   FACEBOOK_PAGE_ID={page_id}")

if __name__ == "__main__":
    main()
