"""Test Instagram Autopost in Mock Mode"""
import asyncio
import os

# Force mock mode
os.environ['SOCIAL_MOCK_MODE'] = 'true'

from facebook_instagram_integration import FacebookInstagramIntegration

async def test():
    print("=" * 80)
    print("  📷 INSTAGRAM AUTO-POST - MOCK MODE TEST")
    print("=" * 80)
    
    # Initialize with mock mode
    integration = FacebookInstagramIntegration(mock_mode=True)
    
    print(f"\n✅ Mock Mode: {integration.mock_mode}")
    
    # Test post
    message = """🎉 Exciting News from AI Employee Vault!

We're thrilled to announce our latest AI-powered automation features:

✨ Auto-posting to social media
✨ Smart content scheduling  
✨ Advanced analytics & insights

Boost your productivity today! 🚀

#AIAutomation #Productivity #TechInnovation #BusinessGrowth #AI #Instagram"""

    print(f"\n📝 Posting message...")
    
    result = await integration.post_to_instagram(
        message=message,
        image_url="https://picsum.photos/1080/1080?random=1"
    )
    
    print("\n" + "=" * 80)
    if result.get("success"):
        print("  ✅ INSTAGRAM POST SUCCESSFUL (MOCK)!")
        print(f"  📍 Post ID: {result.get('post_id')}")
        print(f"  📷 Media ID: {result.get('media_id')}")
        print(f"  ⏰ Timestamp: {result.get('timestamp')}")
    else:
        print("  ❌ INSTAGRAM POST FAILED")
        print(f"  ⚠️  Error: {result.get('error')}")
    print("=" * 80)
    
    return result

if __name__ == "__main__":
    asyncio.run(test())
