"""
Live Social Media Poster

Posts live to Facebook and Instagram.

Usage:
    python post_live.py
    
Or with custom message:
    python post_live.py "Your custom message here"
"""

import asyncio
import sys
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from facebook_instagram_integration import FacebookInstagramIntegration


async def post_live(message: str = None):
    """Post live to Facebook and Instagram"""
    
    print("=" * 80)
    print(" 🚀 LIVE SOCIAL MEDIA POST")
    print("=" * 80)
    print(f" Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Default message if none provided
    if not message:
        message = """🎉 Exciting News from AI Employee Vault! 

We're revolutionizing business automation with our cutting-edge AI solutions. 

✨ What we offer:
• Intelligent process automation
• Smart document management
• Cross-platform integration
• Real-time analytics

Ready to transform your business? Let's connect! 💼

#AIEmployeeVault #BusinessAutomation #AI #Innovation #DigitalTransformation #Productivity #TechSolutions #Entrepreneur #BusinessGrowth #Automation"""

    print(f"\n📝 Message:\n{message}\n")
    print("-" * 80)
    
    # Initialize integration (will use live mode since SOCIAL_MOCK_MODE=false)
    integration = FacebookInstagramIntegration(mock_mode=False)
    
    print("⚠️  POSTING LIVE TO SOCIAL MEDIA...")
    print("-" * 80)
    
    # Post to Facebook
    print("\n📘 Posting to Facebook...")
    try:
        fb_result = await integration.post_to_facebook(
            message=message,
            link="https://example.com"  # Optional: Add your website
        )
        
        if fb_result.get("success"):
            print(f"  ✅ FACEBOOK POST SUCCESSFUL!")
            print(f"     Post ID: {fb_result.get('post_id')}")
            print(f"     URL: https://facebook.com/{fb_result.get('post_id', '')}")
        else:
            print(f"  ❌ FACEBOOK POST FAILED!")
            print(f"     Error: {fb_result.get('error')}")
    except Exception as e:
        print(f"  ❌ FACEBOOK POST ERROR: {e}")
        fb_result = {"success": False, "error": str(e)}
    
    # Post to Instagram (only if configured)
    print("\n📷 Posting to Instagram...")
    if not integration.instagram_user_id or not integration.instagram_access_token:
        print(f"  ⚠️  INSTAGRAM NOT CONFIGURED")
        print(f"     Please add INSTAGRAM_USER_ID and INSTAGRAM_ACCESS_TOKEN to .env")
        ig_result = {"success": False, "error": "Instagram not configured"}
    else:
        try:
            ig_result = await integration.post_to_instagram(
                message=message,
                image_url="https://images.unsplash.com/photo-1551434678-e076c223a692?w=800"  # Optional: Add image
            )
            
            if ig_result.get("success"):
                print(f"  ✅ INSTAGRAM POST SUCCESSFUL!")
                print(f"     Post ID: {ig_result.get('post_id')}")
            else:
                print(f"  ❌ INSTAGRAM POST FAILED!")
                print(f"     Error: {ig_result.get('error')}")
        except Exception as e:
            print(f"  ❌ INSTAGRAM POST ERROR: {e}")
            ig_result = {"success": False, "error": str(e)}
    
    # Summary
    print("\n" + "=" * 80)
    print(" 📊 POSTING SUMMARY")
    print("=" * 80)
    print(f"  Facebook:  {'✅ SUCCESS' if fb_result.get('success') else '❌ FAILED'}")
    print(f"  Instagram: {'✅ SUCCESS' if ig_result.get('success') else '⚠️  NOT CONFIGURED' if 'not configured' in ig_result.get('error', '').lower() else '❌ FAILED'}")
    print("=" * 80)
    
    # Return results
    return {
        "facebook": fb_result,
        "instagram": ig_result,
        "success": fb_result.get("success") or ig_result.get("success")
    }


async def post_to_both_with_image():
    """Post to both platforms with an image"""
    
    print("=" * 80)
    print(" 🚀 LIVE POST WITH IMAGE")
    print("=" * 80)
    
    message = """🌟 Transform Your Business with AI! 

Discover how AI Employee Vault can automate your workflows and boost productivity.

#AI #Automation #Business #Innovation #Technology"""
    
    integration = FacebookInstagramIntegration(mock_mode=False)
    
    print("\n📱 Posting to BOTH platforms with image...")
    
    result = await integration.post_to_both(
        message=message,
        image_url="https://images.unsplash.com/photo-1551434678-e076c223a692?w=800",
        link="https://example.com"
    )
    
    print("\n" + "=" * 80)
    print(" RESULTS")
    print("=" * 80)
    print(f"  Facebook:  {'✅ SUCCESS' if result.get('facebook', {}).get('success') else '❌ FAILED'}")
    print(f"  Instagram: {'✅ SUCCESS' if result.get('instagram', {}).get('success') else '❌ FAILED'}")
    print("=" * 80)
    
    return result


if __name__ == "__main__":
    # Get custom message from command line if provided
    if len(sys.argv) > 1:
        custom_message = " ".join(sys.argv[1:])
        print(f"\n📝 Using custom message: {custom_message[:50]}...\n")
    else:
        custom_message = None
    
    # Run the poster
    success = asyncio.run(post_live(custom_message))
    
    # Exit with appropriate code
    sys.exit(0 if success.get("success") else 1)
