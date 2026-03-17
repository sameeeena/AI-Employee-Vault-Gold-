"""
Quick Auto-Post to Facebook (Fixed Version)

Simple script to post immediately to Facebook.
Uses your existing Facebook Page configuration from .env

Usage:
    python facebook_poster_fixed.py
"""

import asyncio
import sys
from facebook_instagram_integration import FacebookInstagramIntegration


async def autopost(message: str, image_url: str = None, link: str = None):
    """Post to Facebook immediately"""

    print("=" * 80)
    print("  FACEBOOK AUTO-POST")
    print("=" * 80)

    # Initialize integration
    integration = FacebookInstagramIntegration()

    if integration.mock_mode:
        print("\nWARNING: MOCK MODE is enabled - posts will be simulated, not published")
        print("   To post live, set SOCIAL_MOCK_MODE=false in .env\n")
    else:
        print("\nLIVE MODE - posts will be published to Facebook\n")

    # Post to Facebook
    print(f"Message: {message[:100]}{'...' if len(message) > 100 else ''}")

    if image_url:
        print(f"Image: {image_url}")

    if link:
        print(f"Link: {link}")

    print("\nPosting...")

    result = await integration.post_to_facebook(
        message=message,
        image_url=image_url,
        link=link
    )

    # Display result
    print("\n" + "=" * 80)

    if result.get("success"):
        print("  POST SUCCESSFUL!")
        print("=" * 80)
        print(f"  Post ID: {result.get('post_id')}")
        print(f"  View: {result.get('post_url', 'N/A')}")
        print(f"  Posted at: {result.get('timestamp', 'N/A')}")
    else:
        print("  POST FAILED")
        print("=" * 80)
        print(f"  Error: {result.get('error', 'Unknown error')}")
        if result.get("details"):
            print(f"  Details: {result.get('details')}")

    print("\n" + "=" * 80)

    return result


async def main():
    """Main function with example post"""

    # Example post - customize this!
    MESSAGE = """Exciting Update!

We're thrilled to share our latest AI-powered automation features with you!

What's new:
• Auto-posting to social media
• Smart content scheduling
• Advanced analytics

Try it out today and boost your productivity!

#AIAutomation #Productivity #TechInnovation #BusinessGrowth"""

    # Optional: Add image URL (must be publicly accessible)
    IMAGE_URL = None  # Example: "https://example.com/image.jpg"

    # Optional: Add link
    LINK = None  # Example: "https://yourwebsite.com"

    # Post to Facebook
    result = await autopost(MESSAGE, IMAGE_URL, LINK)

    # Exit with appropriate code
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    asyncio.run(main())