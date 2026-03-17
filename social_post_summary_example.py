"""
Facebook & Instagram - Post Messages and Generate Summary
Complete Example Script

Usage:
    python social_post_summary_example.py
"""

import asyncio
from facebook_instagram_integration import FacebookInstagramIntegration


async def main():
    """Main function to demonstrate posting and summary generation"""
    
    print("=" * 80)
    print("  FACEBOOK & INSTAGRAM - POST AND SUMMARY EXAMPLE")
    print("=" * 80)
    
    # Initialize integration
    integration = FacebookInstagramIntegration()
    
    if integration.mock_mode:
        print("\n⚠️  MOCK MODE is enabled")
        print("   To post live, set SOCIAL_MOCK_MODE=false in .env\n")
    else:
        print("\n✅ LIVE MODE\n")
    
    # ============== STEP 1: Post to Facebook ==============
    print("\n" + "=" * 80)
    print("  STEP 1: Posting to Facebook")
    print("=" * 80)
    
    facebook_message = """🎉 Exciting Update from AI Employee Vault!

We're thrilled to announce our latest AI-powered automation features:
✨ Auto-posting to social media
✨ Smart content scheduling  
✨ Advanced analytics

Try it out today and boost your productivity! 🚀

#AIAutomation #Productivity #TechInnovation #BusinessGrowth"""
    
    fb_result = await integration.post_to_facebook(
        message=facebook_message,
        link="https://example.com"  # Optional link
    )
    
    print(f"\n✅ Facebook Result:")
    print(f"   Success: {fb_result.get('success')}")
    print(f"   Post ID: {fb_result.get('post_id', 'N/A')}")
    print(f"   URL: {fb_result.get('post_url', 'N/A')}")
    
    # ============== STEP 2: Post to Instagram ==============
    print("\n" + "=" * 80)
    print("  STEP 2: Posting to Instagram")
    print("=" * 80)
    
    instagram_message = """🌟 Beautiful day for innovation!

Behind the scenes at AI Employee Vault HQ. 
Working on amazing features for you! 💼

#TeamLife #AI #Innovation #WorkCulture #TechLife"""
    
    ig_result = await integration.post_to_instagram(
        message=instagram_message,
        image_url="https://example.com/office-photo.jpg"  # Required for Instagram
    )
    
    print(f"\n✅ Instagram Result:")
    print(f"   Success: {ig_result.get('success')}")
    print(f"   Post ID: {ig_result.get('post_id', 'N/A')}")
    
    # ============== STEP 3: Generate Facebook Summary ==============
    print("\n" + "=" * 80)
    print("  STEP 3: Generating Facebook Summary")
    print("=" * 80)
    
    fb_summary = await integration.generate_facebook_summary()
    
    if fb_summary.get('success'):
        print(f"\n📊 Facebook Summary:")
        print(f"   Total Posts: {fb_summary.get('total_posts', 0)}")
        print(f"   Total Reactions: {fb_summary.get('total_reactions', 0)}")
        print(f"   Total Comments: {fb_summary.get('total_comments', 0)}")
        print(f"   Total Shares: {fb_summary.get('total_shares', 0)}")
        print(f"   Average Engagement: {fb_summary.get('average_engagement', 0):.2f}")
        
        print(f"\n   Recent Posts:")
        for i, post in enumerate(fb_summary.get('posts', [])[:3], 1):
            print(f"   {i}. {post.get('message', 'No text')}")
            print(f"      Reactions: {post.get('reactions', 0)} | Comments: {post.get('comments', 0)}")
    else:
        print(f"\n❌ Failed to generate Facebook summary: {fb_summary.get('error')}")
    
    # ============== STEP 4: Generate Instagram Summary ==============
    print("\n" + "=" * 80)
    print("  STEP 4: Generating Instagram Summary")
    print("=" * 80)
    
    ig_summary = await integration.generate_instagram_summary()
    
    if ig_summary.get('success'):
        print(f"\n📊 Instagram Summary:")
        print(f"   Total Posts: {ig_summary.get('total_posts', 0)}")
        print(f"   Total Likes: {ig_summary.get('total_likes', 0)}")
        print(f"   Total Comments: {ig_summary.get('total_comments', 0)}")
        print(f"   Average Engagement: {ig_summary.get('average_engagement', 0):.2f}")
        
        print(f"\n   Recent Posts:")
        for i, post in enumerate(ig_summary.get('posts', [])[:3], 1):
            print(f"   {i}. {post.get('caption', 'No caption')}")
            print(f"      Likes: {post.get('likes', 0)} | Comments: {post.get('comments', 0)}")
    else:
        print(f"\n❌ Failed to generate Instagram summary: {ig_summary.get('error')}")
    
    # ============== STEP 5: Generate Combined Summary ==============
    print("\n" + "=" * 80)
    print("  STEP 5: Generating Combined Summary")
    print("=" * 80)
    
    combined_summary = await integration.generate_combined_summary()
    
    if combined_summary.get('success'):
        print(f"\n📊 Combined Summary:")
        print(f"   Total Platforms: 2")
        print(f"   Total Posts: {combined_summary.get('combined_metrics', {}).get('total_posts', 0)}")
        print(f"   Total Engagement: {combined_summary.get('combined_metrics', {}).get('total_engagement', 0)}")
        
        print(f"\n   Platform Breakdown:")
        print(f"   Facebook - Posts: {combined_summary.get('facebook', {}).get('total_posts', 0)}")
        print(f"   Instagram - Posts: {combined_summary.get('instagram', {}).get('total_posts', 0)}")
    else:
        print(f"\n❌ Failed to generate combined summary: {combined_summary.get('error')}")
    
    # ============== FINAL SUMMARY ==============
    print("\n" + "=" * 80)
    print("  FINAL SUMMARY")
    print("=" * 80)
    print(f"  ✅ Facebook Post: {'Success' if fb_result.get('success') else 'Failed'}")
    print(f"  ✅ Instagram Post: {'Success' if ig_result.get('success') else 'Failed'}")
    print(f"  ✅ Facebook Summary: {'Generated' if fb_summary.get('success') else 'Failed'}")
    print(f"  ✅ Instagram Summary: {'Generated' if ig_summary.get('success') else 'Failed'}")
    print(f"  ✅ Combined Summary: {'Generated' if combined_summary.get('success') else 'Failed'}")
    print("=" * 80)
    
    return {
        "facebook_post": fb_result,
        "instagram_post": ig_result,
        "facebook_summary": fb_summary,
        "instagram_summary": ig_summary,
        "combined_summary": combined_summary
    }


if __name__ == "__main__":
    result = asyncio.run(main())
