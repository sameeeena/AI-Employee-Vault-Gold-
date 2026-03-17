"""
Instagram Auto-Post with Multiple Templates

Post to Instagram with pre-defined message templates.
Supports image posts and text posts.

Usage:
    python instagram_autopost_now.py
    
    Or with template selection:
    python instagram_autopost_now.py --template 2
"""

import asyncio
import sys
import argparse
from datetime import datetime
from facebook_instagram_integration import FacebookInstagramIntegration


# ============== PRE-DEFINED POST TEMPLATES ==============

TEMPLATES = {
    1: {
        "name": "🎉 Product Announcement",
        "message": """🎉 Exciting News from AI Employee Vault!

We're thrilled to announce our latest AI-powered automation features:

✨ Auto-posting to social media
✨ Smart content scheduling  
✨ Advanced analytics & insights
✨ Multi-platform support

Boost your productivity today! 🚀

#AIAutomation #Productivity #TechInnovation #BusinessGrowth #AI #Instagram #NewProduct""",
        "image_url": "https://picsum.photos/1080/1080?random=1"  # Placeholder image
    },
    
    2: {
        "name": "💼 Business Tips",
        "message": """💡 Business Tip of the Day!

Did you know? Automating repetitive tasks can save up to 40% of your work time!

Here's how AI can help:
✅ Auto-respond to customer queries
✅ Schedule social media posts
✅ Generate reports automatically
✅ Track business metrics in real-time

Start automating today and focus on what matters! 📈

#BusinessTips #Automation #AI #Entrepreneurship #Growth #Success #Motivation""",
        "image_url": "https://picsum.photos/1080/1080?random=2"
    },
    
    3: {
        "name": "🌟 Motivational Post",
        "message": """🌟 Monday Motivation!

"The best way to predict the future is to create it." - Peter Drucker

Every day is a new opportunity to:
🎯 Set goals
💪 Work smarter
🚀 Embrace technology
📊 Measure progress

Make today count! What's your goal for this week?

#Motivation #MondayMotivation #Success #Goals #AI #Inspiration #Mindset""",
        "image_url": "https://picsum.photos/1080/1080?random=3"
    },
    
    4: {
        "name": "📊 Industry Insights",
        "message": """📊 Industry Insight 2026!

AI Automation Market Trends:

📈 73% of businesses now use some form of automation
💰 Average ROI: 300% in first year
⏰ Time saved: 15-20 hours/week per employee
🎯 Customer satisfaction up by 45%

Is your business ready for the AI revolution?

#IndustryInsights #AI #BusinessTrends #Automation #DigitalTransformation #Tech2026""",
        "image_url": "https://picsum.photos/1080/1080?random=4"
    },
    
    5: {
        "name": "🎯 Customer Success",
        "message": """🎯 Customer Success Story!

"Since implementing AI Employee Vault, we've:
• Reduced manual work by 60%
• Increased social media engagement by 250%
• Saved 25 hours per week
• Grown our customer base by 40%"

- Happy Customer, CEO at TechCorp

Ready to transform your business? Let's talk! 💼

#CustomerSuccess #CaseStudy #AI #BusinessGrowth #Testimonial #Results""",
        "image_url": "https://picsum.photos/1080/1080?random=5"
    },
    
    6: {
        "name": "🔧 Feature Highlight",
        "message": """🔧 Feature Spotlight!

Did you know AI Employee Vault can:

✅ Auto-post to Facebook, Instagram & LinkedIn
✅ Generate performance summaries
✅ Schedule posts at optimal times
✅ Create content calendars
✅ Track engagement metrics
✅ Support multiple accounts

One tool, endless possibilities! 🚀

#Features #AITools #Productivity #SocialMedia #Automation #TechTools""",
        "image_url": "https://picsum.photos/1080/1080?random=6"
    },
    
    7: {
        "name": "📚 Educational Content",
        "message": """📚 Learn Something New!

5 Ways AI Can Transform Your Business:

1️⃣ Automate customer support (24/7 availability)
2️⃣ Analyze data instantly (real-time insights)
3️⃣ Personalize marketing (better engagement)
4️⃣ Streamline operations (reduce costs)
5️⃣ Predict trends (stay ahead of competition)

Which one will you implement first?

#Education #AI #Business #Learning #Innovation #AITools #DigitalMarketing""",
        "image_url": "https://picsum.photos/1080/1080?random=7"
    },
    
    8: {
        "name": "🎊 Special Offer",
        "message": """🎊 Limited Time Offer!

Get started with AI Employee Vault today!

🎁 What's included:
• Full access to all automation features
• Priority support
• Free setup assistance
• 30-day money-back guarantee

Don't miss out! Offer ends soon! ⏰

DM us or visit our website to learn more!

#SpecialOffer #Deal #AI #Business #LimitedTime #Promotion #Sale""",
        "image_url": "https://picsum.photos/1080/1080?random=8"
    },
    
    9: {
        "name": "📸 Behind The Scenes",
        "message": """📸 Behind The Scenes at AI Employee Vault!

Our team working hard to bring you the best automation tools. 💼

✨ Innovation never stops
✨ Teamwork makes the dream work
✨ Building the future of AI

Stay tuned for exciting updates! 🚀

#BehindTheScenes #TeamLife #OfficeVibes #AI #Startup #TeamWork #CompanyCulture""",
        "image_url": "https://picsum.photos/1080/1080?random=9"
    },
    
    10: {
        "name": "🎨 Inspirational Quote",
        "message": """🎨 Daily Inspiration!

"Technology is best when it brings people together." - Matt Mullenweg

At AI Employee Vault, we believe in:
🤝 Connection through automation
💡 Innovation with purpose
🚀 Growth through technology

What inspires you today?

#Inspiration #Quote #Technology #AI #Innovation #DigitalTransformation #Leadership""",
        "image_url": "https://picsum.photos/1080/1080?random=10"
    }
}


async def autopost(template_id: int = None, custom_message: str = None, 
                   image_url: str = None, is_reel: bool = False):
    """
    Post to Instagram immediately
    
    Args:
        template_id: Template ID (1-10) to use
        custom_message: Custom message (overrides template)
        image_url: Image URL (required for most posts)
        is_reel: If True, create a Reel instead of regular post
    """
    
    print("=" * 80)
    print("  📷 INSTAGRAM AUTO-POST")
    print("=" * 80)
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Initialize integration
    integration = FacebookInstagramIntegration()
    
    if integration.mock_mode:
        print("\n⚠️  MOCK MODE is enabled - posts will be simulated, not published")
        print("   To post live, set SOCIAL_MOCK_MODE=false and configure Instagram tokens in .env\n")
    else:
        print("\n✅ LIVE MODE - posts will be published to Instagram\n")
    
    # Get message from template or custom
    if custom_message:
        message = custom_message
        template_name = "Custom Message"
        final_image_url = image_url
    elif template_id and template_id in TEMPLATES:
        template = TEMPLATES[template_id]
        message = template["message"]
        template_name = template["name"]
        final_image_url = image_url or template["image_url"]
    else:
        # Show available templates
        print("\n📋 Available Templates:")
        print("-" * 80)
        for tid, template in TEMPLATES.items():
            print(f"  {tid}. {template['name']}")
        print("-" * 80)
        print("\n⚠️  No template selected. Use --template <id> or select from above.\n")
        return None
    
    post_type = "Reel" if is_reel else "Post"
    print(f"📝 Template: {template_name} ({post_type})")
    print(f"\n📄 Message Preview:")
    print("-" * 80)
    print(message[:500] + "..." if len(message) > 500 else message)
    print("-" * 80)
    
    if final_image_url:
        print(f"🖼️  Image: {final_image_url}")
    
    print(f"\n⏳ Posting to Instagram...")
    
    # Post to Instagram
    result = await integration.post_to_instagram(
        message=message,
        image_url=final_image_url,
        is_reel=is_reel
    )
    
    # Display result
    print("\n" + "=" * 80)
    
    if result.get("success"):
        print("  ✅ INSTAGRAM POST SUCCESSFUL!")
        print("=" * 80)
        print(f"  📍 Post ID: {result.get('post_id', 'N/A')}")
        print(f"  📷 Media ID: {result.get('media_id', 'N/A')}")
        print(f"  ⏰ Posted at: {result.get('timestamp', 'N/A')}")
        print(f"  🎬 Type: {'Reel' if is_reel else 'Post'}")
        print("=" * 80)
    else:
        print("  ❌ INSTAGRAM POST FAILED")
        print("=" * 80)
        print(f"  ⚠️  Error: {result.get('error', 'Unknown error')}")
        if result.get("details"):
            print(f"  📋 Details: {result.get('details')}")
        print("=" * 80)
    
    return result


async def main():
    """Main function with argument parsing"""
    
    parser = argparse.ArgumentParser(description='Instagram Auto-Post')
    parser.add_argument('--template', '-t', type=int, choices=range(1, 11),
                        help='Template ID (1-10)')
    parser.add_argument('--message', '-m', type=str, help='Custom message')
    parser.add_argument('--image', '-i', type=str, help='Image URL')
    parser.add_argument('--reel', '-r', action='store_true', help='Create a Reel instead of post')
    
    args = parser.parse_args()
    
    # Post to Instagram
    result = await autopost(
        template_id=args.template,
        custom_message=args.message,
        image_url=args.image,
        is_reel=args.reel
    )
    
    # Exit with appropriate code
    if result:
        sys.exit(0 if result.get("success") else 1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
