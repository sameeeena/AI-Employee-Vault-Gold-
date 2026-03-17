"""
Facebook Token Tester

Tests if your Facebook access token is valid and has the right permissions.

Usage:
    python test_facebook_token.py
"""

import httpx
import os
from datetime import datetime as dt
from dotenv import load_dotenv

load_dotenv()

def test_token():
    """Test Facebook access token"""
    
    print("=" * 80)
    print(" 🔍 FACEBOOK TOKEN VALIDITY TEST")
    print("=" * 80)
    print(f" Time: {dt.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Get configuration
    page_access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    page_id = os.getenv("FACEBOOK_PAGE_ID", "")
    graph_api_version = os.getenv("GRAPH_API_VERSION", "v19.0")
    
    print(f"\n📋 Configuration:")
    print(f"   Page ID: {page_id}")
    print(f"   Token length: {len(page_access_token)} chars")
    print(f"   API Version: {graph_api_version}")
    
    if not page_access_token:
        print("\n❌ ERROR: FACEBOOK_PAGE_ACCESS_TOKEN not found in .env!")
        return False
    
    if not page_id:
        print("\n❌ ERROR: FACEBOOK_PAGE_ID not found in .env!")
        return False
    
    # Test 1: Check token validity
    print("\n" + "-" * 80)
    print(" TEST 1: Token Validity")
    print("-" * 80)
    
    try:
        response = httpx.get(
            f"https://graph.facebook.com/{graph_api_version}/me",
            params={'access_token': page_access_token}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Token is VALID!")
            print(f"     Name: {data.get('name', 'Unknown')}")
            print(f"     ID: {data.get('id', 'Unknown')}")
        else:
            error = response.json()
            print(f"  ❌ Token is INVALID or EXPIRED!")
            print(f"     Error: {error.get('error', {}).get('message', 'Unknown error')}")
            print(f"\n  🔧 SOLUTION: Generate new token at:")
            print(f"     https://developers.facebook.com/tools/explorer/")
            return False
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return False
    
    # Test 2: Check permissions
    print("\n" + "-" * 80)
    print(" TEST 2: Check Permissions")
    print("-" * 80)
    
    try:
        response = httpx.get(
            f"https://graph.facebook.com/{graph_api_version}/me/permissions",
            params={'access_token': page_access_token}
        )
        
        if response.status_code == 200:
            data = response.json()
            permissions = data.get('data', [])
            
            print("  Your permissions:")
            required = ['pages_manage_posts', 'pages_read_engagement', 'pages_show_list']
            
            for perm in permissions:
                status = "✅" if perm.get('status') == 'granted' else "❌"
                print(f"    {status} {perm.get('permission', 'unknown')}")
            
            # Check required permissions
            granted_perms = [p['permission'] for p in permissions if p.get('status') == 'granted']
            missing = [p for p in required if p not in granted_perms]
            
            if missing:
                print(f"\n  ⚠️  Missing permissions: {missing}")
                print(f"     Please grant these permissions when generating token")
            else:
                print(f"\n  ✅ All required permissions granted!")
        else:
            print(f"  ⚠️  Could not check permissions: {response.status_code}")
    except Exception as e:
        print(f"  ⚠️  Error checking permissions: {e}")
    
    # Test 3: Check page access
    print("\n" + "-" * 80)
    print(" TEST 3: Page Access")
    print("-" * 80)
    
    try:
        response = httpx.get(
            f"https://graph.facebook.com/{graph_api_version}/{page_id}",
            params={
                'access_token': page_access_token,
                'fields': 'name,link'
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Page access confirmed!")
            print(f"     Page Name: {data.get('name', 'Unknown')}")
            print(f"     Page URL: {data.get('link', 'Unknown')}")
        else:
            error = response.json()
            print(f"  ❌ Cannot access page!")
            print(f"     Error: {error.get('error', {}).get('message', 'Unknown error')}")
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
    
    # Test 4: Token expiry info
    print("\n" + "-" * 80)
    print(" TEST 4: Token Expiry")
    print("-" * 80)
    
    try:
        response = httpx.get(
            "https://graph.facebook.com/v19.0/debug_token",
            params={
                'input_token': page_access_token,
                'access_token': page_access_token
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            token_info = data.get('data', {})
            
            is_valid = token_info.get('is_valid', False)
            expires_at = token_info.get('expires_at', 'Unknown')
            
            print(f"  Token Valid: {is_valid}")
            print(f"  Expires At: {expires_at}")
            
            if expires_at != 'Unknown':
                try:
                    expiry_date = dt.fromtimestamp(int(expires_at))
                    days_left = (expiry_date - dt.now()).days
                    print(f"  Days Left: {days_left}")
                    
                    if days_left < 7:
                        print(f"\n  ⚠️  WARNING: Token expires in less than 7 days!")
                        print(f"     Please generate a new token soon")
                except:
                    pass
        else:
            print(f"  ⚠️  Could not check token expiry")
    except Exception as e:
        print(f"  ⚠️  Error checking token expiry: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print(" SUMMARY")
    print("=" * 80)
    print("  ✅ Token is valid and ready to use!")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    import sys
    
    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    success = test_token()
    sys.exit(0 if success else 1)
