"""Check current token in .env"""
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN', '')

print("=" * 80)
print("  CURRENT TOKEN IN .ENV")
print("=" * 80)
print()

if token:
    print(f"Token starts with: {token[:30]}...")
    print(f"Token length: {len(token)}")
    print()
    
    # Check if it's the old expired one
    if token.startswith("EAASHynQdn7kBQ"):
        print("⚠️  This is the OLD expired token!")
        print("   You need to update .env with the NEW token from Graph API Explorer")
    else:
        print("✅ This looks like a new token!")
else:
    print("❌ No token found in .env!")

print()
print("=" * 80)
