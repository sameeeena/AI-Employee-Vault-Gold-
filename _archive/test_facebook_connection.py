"""Test Facebook Connection"""
from facebook_instagram_integration import FacebookInstagramIntegration
import asyncio

async def test():
    print("=" * 60)
    print("  FACEBOOK CONNECTION TEST")
    print("=" * 60)
    
    # Initialize (live mode)
    integration = FacebookInstagramIntegration(mock_mode=False)
    
    print(f"\n✅ Mock Mode: {integration.mock_mode}")
    print(f"📍 Page ID: {integration.facebook_page_id}")
    print(f"🔑 Token Present: {bool(integration.facebook_page_access_token)}")
    
    # Test post
    print("\n📝 Posting test message...")
    result = await integration.post_to_facebook(
        message="Test post from AI Employee Vault! #AutoPost #Test"
    )
    
    print("\n" + "=" * 60)
    if result.get("success"):
        print("  ✅ TEST SUCCESSFUL!")
        print(f"  📍 Post ID: {result.get('post_id')}")
        print(f"  🔗 URL: {result.get('post_url')}")
    else:
        print("  ❌ TEST FAILED")
        print(f"  ⚠️  Error: {result.get('error')}")
    print("=" * 60)
    
    return result

if __name__ == "__main__":
    asyncio.run(test())
