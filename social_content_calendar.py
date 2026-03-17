"""
Social Media Content Calendar & Scheduler

Advanced features for Facebook and Instagram:
- Content calendar management
- Post templates library
- Automated scheduling
- Hashtag suggestions
- Analytics dashboard generation
- Recurring post management

Usage:
    python social_content_calendar.py
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import hashlib
from dataclasses import dataclass, asdict
import aiofiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============== Data Models ==============

@dataclass
class ScheduledPost:
    """Represents a scheduled social media post"""
    id: str
    message: str
    platforms: List[str]  # ['facebook', 'instagram', 'both']
    scheduled_time: str  # ISO format
    image_url: Optional[str] = None
    link: Optional[str] = None
    is_reel: bool = False
    status: str = "pending"  # pending, posted, failed, cancelled
    hashtags: Optional[List[str]] = None
    template_id: Optional[str] = None
    created_at: str = ""
    posted_at: Optional[str] = None
    post_ids: Optional[Dict[str, str]] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.id:
            self.id = f"scheduled_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(self.message.encode()).hexdigest()[:8]}"


@dataclass
class PostTemplate:
    """Template for common post types"""
    id: str
    name: str
    category: str  # announcement, promotion, engagement, educational, behind_scenes
    message_template: str
    suggested_hashtags: List[str]
    best_posting_times: List[str]  # ["09:00", "13:00", "18:00"]
    platforms: List[str]
    image_suggested: bool = True


@dataclass
class ContentCalendar:
    """Monthly content calendar"""
    month: int
    year: int
    posts: List[ScheduledPost]
    total_posts: int = 0
    posts_by_platform: Dict[str, int] = None
    posts_by_category: Dict[str, int] = None

    def __post_init__(self):
        if not self.posts_by_platform:
            self.posts_by_platform = {"facebook": 0, "instagram": 0, "both": 0}
        if not self.posts_by_category:
            self.posts_by_category = {}
        self.total_posts = len(self.posts)


# ============== Post Templates Library ==============

class PostTemplatesLibrary:
    """Library of pre-defined post templates"""

    def __init__(self):
        self.templates_file = "state/post_templates.json"
        self._ensure_templates_file()
        self.templates = self._load_templates()

    def _ensure_templates_file(self):
        """Ensure templates file exists with default templates"""
        os.makedirs("state", exist_ok=True)
        if not os.path.exists(self.templates_file):
            default_templates = self._get_default_templates()
            self._save_templates(default_templates)

    def _get_default_templates(self) -> List[Dict[str, Any]]:
        """Get default post templates"""
        return [
            {
                "id": "template_announcement",
                "name": "Company Announcement",
                "category": "announcement",
                "message_template": "📢 {announcement_title}\n\n{announcement_details}\n\n#CompanyNews #Announcement",
                "suggested_hashtags": ["#CompanyNews", "#Announcement", "#Business", "#Update"],
                "best_posting_times": ["09:00", "13:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": True
            },
            {
                "id": "template_promotion",
                "name": "Product/Service Promotion",
                "category": "promotion",
                "message_template": "🎉 Special Offer Alert!\n\n{product_name}: {offer_details}\n\n⏰ Valid until: {expiry_date}\n👉 {call_to_action}\n\n#SpecialOffer #Promotion",
                "suggested_hashtags": ["#Sale", "#Promotion", "#SpecialOffer", "#Deal", "#Shopping"],
                "best_posting_times": ["10:00", "15:00", "19:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": True
            },
            {
                "id": "template_engagement",
                "name": "Audience Engagement Question",
                "category": "engagement",
                "message_template": "💭 Quick Question for You!\n\n{engagement_question}\n\nDrop your answer in the comments! 👇\n\n#Community #Engagement",
                "suggested_hashtags": ["#Question", "#Community", "#Engagement", "#Discussion", "#Feedback"],
                "best_posting_times": ["12:00", "18:00", "20:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": False
            },
            {
                "id": "template_educational",
                "name": "Educational/Tip Post",
                "category": "educational",
                "message_template": "💡 Pro Tip: {tip_title}\n\n{tip_content}\n\nSave this for later! 🔖\n\n#Tips #Education",
                "suggested_hashtags": ["#Tips", "#Education", "#Learning", "#HowTo", "#Advice", "#Knowledge"],
                "best_posting_times": ["08:00", "14:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": True
            },
            {
                "id": "template_behind_scenes",
                "name": "Behind the Scenes",
                "category": "behind_scenes",
                "message_template": "🎬 Behind the Scenes at {company_name}!\n\n{behind_scenes_content}\n\n#BehindTheScenes #TeamLife",
                "suggested_hashtags": ["#BehindTheScenes", "#TeamLife", "#CompanyCulture", "#WorkLife", "#Office"],
                "best_posting_times": ["11:00", "17:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": True
            },
            {
                "id": "template_testimonial",
                "name": "Customer Testimonial",
                "category": "testimonial",
                "message_template": "⭐ Customer Love!\n\n\"{testimonial_text}\"\n\n- {customer_name}\n\nThank you for your trust! 🙏\n\n#Testimonial #CustomerReview",
                "suggested_hashtags": ["#Testimonial", "#Review", "#CustomerLove", "#Feedback", "#Happy"],
                "best_posting_times": ["10:00", "16:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": True
            },
            {
                "id": "template_event",
                "name": "Event Announcement",
                "category": "event",
                "message_template": "📅 You're Invited!\n\nEvent: {event_name}\n🗓️ Date: {event_date}\n⏰ Time: {event_time}\n📍 Location: {event_location}\n\n{event_details}\n\nRSVP: {rsvp_link}\n\n#Event #Invitation",
                "suggested_hashtags": ["#Event", "#Invitation", "#SaveTheDate", "#ComingSoon"],
                "best_posting_times": ["09:00", "18:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": True
            },
            {
                "id": "template_motivation",
                "name": "Motivational Quote",
                "category": "motivation",
                "message_template": "✨ Daily Inspiration ✨\n\n\"{motivational_quote}\"\n\n- {quote_author}\n\n#Motivation #Inspiration",
                "suggested_hashtags": ["#Motivation", "#Inspiration", "#Quote", "#DailyMotivation", "#Success"],
                "best_posting_times": ["07:00", "08:00", "20:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": True
            },
            {
                "id": "template_product_launch",
                "name": "Product Launch",
                "category": "launch",
                "message_template": "🚀 BIG NEWS! Introducing {product_name}!\n\n{product_description}\n\nKey Features:\n✨ {feature_1}\n✨ {feature_2}\n✨ {feature_3}\n\nLearn more: {product_link}\n\n#ProductLaunch #New",
                "suggested_hashtags": ["#ProductLaunch", "#New", "#Innovation", "#Launch", "#Exciting"],
                "best_posting_times": ["09:00", "12:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": True
            },
            {
                "id": "template_friday_fun",
                "name": "Friday Fun Post",
                "category": "engagement",
                "message_template": "🎉 It's Friday!\n\n{friday_content}\n\nWhat are your weekend plans? Tell us below! 👇\n\n#Friday #Weekend",
                "suggested_hashtags": ["#Friday", "#Weekend", "#FridayFeeling", "#TGIF", "#WeekendVibes"],
                "best_posting_times": ["15:00", "17:00"],
                "platforms": ["facebook", "instagram"],
                "image_suggested": False
            }
        ]

    def _load_templates(self) -> List[Dict[str, Any]]:
        """Load templates from file"""
        try:
            with open(self.templates_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self._get_default_templates()

    def _save_templates(self, templates: List[Dict[str, Any]]):
        """Save templates to file"""
        with open(self.templates_file, "w", encoding="utf-8") as f:
            json.dump(templates, f, indent=2)

    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Get all templates"""
        return self.templates

    def get_template_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific template by ID"""
        for template in self.templates:
            if template["id"] == template_id:
                return template
        return None

    def get_templates_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get templates by category"""
        return [t for t in self.templates if t["category"] == category]

    def add_custom_template(self, template: Dict[str, Any]) -> str:
        """Add a custom template"""
        template["id"] = f"custom_{hashlib.md5(template['name'].encode()).hexdigest()[:8]}"
        self.templates.append(template)
        self._save_templates(self.templates)
        return template["id"]

    def render_template(self, template_id: str, variables: Dict[str, str]) -> Optional[str]:
        """Render a template with variables"""
        template = self.get_template_by_id(template_id)
        if not template:
            return None

        message = template["message_template"]
        for key, value in variables.items():
            message = message.replace(f"{{{key}}}", value)

        return message


# ============== Hashtag Suggestions ==============

class HashtagSuggester:
    """Generates hashtag suggestions based on content"""

    def __init__(self):
        self.hashtag_categories = {
            "business": ["#Business", "#Entrepreneur", "#BusinessOwner", "#SmallBusiness", "#BusinessTips"],
            "technology": ["#Technology", "#Tech", "#Innovation", "#Digital", "#AI", "#Automation"],
            "marketing": ["#Marketing", "#DigitalMarketing", "#SocialMedia", "#ContentMarketing", "#Brand"],
            "lifestyle": ["#Lifestyle", "#Life", "#Daily", "#Inspiration", "#Motivation"],
            "education": ["#Education", "#Learning", "#Knowledge", "#Tips", "#HowTo"],
            "entertainment": ["#Entertainment", "#Fun", "#Enjoy", "#Happy", "#Good"],
            "food": ["#Food", "#Foodie", "#Delicious", "#Yummy", "#FoodPorn"],
            "travel": ["#Travel", "#Wanderlust", "#Adventure", "#Explore", "#Vacation"],
            "fashion": ["#Fashion", "#Style", "#OOTD", "#Fashionista", "#Trend"],
            "health": ["#Health", "#Fitness", "#Wellness", "#Healthy", "#Workout"],
            "announcement": ["#Announcement", "#News", "#Update", "#New", "#Important"],
            "promotion": ["#Sale", "#Promotion", "#Discount", "#Offer", "#Deal"],
            "event": ["#Event", "#Live", "#Conference", "#Meetup", "#Gathering"]
        }

        self.trending_hashtags = [
            "#Trending", "#Viral", "#Explore", "#FYP", "#Popular",
            "#2026", "#NewYear", "#Goals", "#Success", "#Growth"
        ]

    def suggest_hashtags(self, content: str, category: Optional[str] = None,
                        platform: str = "both", count: int = 10) -> List[str]:
        """
        Suggest hashtags based on content analysis

        Args:
            content: The post content
            category: Optional content category
            platform: Target platform (facebook, instagram, both)
            count: Number of hashtags to suggest

        Returns:
            List of suggested hashtags
        """
        content_lower = content.lower()
        suggested = []

        # Match category-based hashtags
        if category and category in self.hashtag_categories:
            suggested.extend(self.hashtag_categories[category][:5])

        # Match keywords in content
        for cat, hashtags in self.hashtag_categories.items():
            if cat in content_lower:
                suggested.extend(hashtags[:3])

        # Add platform-specific hashtags
        if platform == "instagram":
            suggested.extend(["#InstaDaily", "#Instagram", "#InstaGood"][:2])
        elif platform == "facebook":
            suggested.extend(["#Facebook", "#FB"][:1])

        # Add trending hashtags
        suggested.extend(self.trending_hashtags[:3])

        # Remove duplicates and limit count
        unique_hashtags = list(dict.fromkeys(suggested))
        return unique_hashtags[:count]

    def get_hashtags_by_category(self, category: str, count: int = 5) -> List[str]:
        """Get hashtags for a specific category"""
        if category in self.hashtag_categories:
            return self.hashtag_categories[category][:count]
        return []


# ============== Content Calendar Manager ==============

class ContentCalendarManager:
    """Manages content calendar and scheduled posts"""

    def __init__(self):
        self.calendar_file = "state/content_calendar.json"
        self._ensure_calendar_file()
        self.templates = PostTemplatesLibrary()
        self.hashtag_suggester = HashtagSuggester()

    def _ensure_calendar_file(self):
        """Ensure calendar file exists"""
        os.makedirs("state", exist_ok=True)
        if not os.path.exists(self.calendar_file):
            self._save_calendar([])

    def _load_calendar(self) -> List[Dict[str, Any]]:
        """Load calendar from file"""
        try:
            with open(self.calendar_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_calendar(self, posts: List[Dict[str, Any]]):
        """Save calendar to file"""
        with open(self.calendar_file, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, default=str)

    async def schedule_post(self, message: str, platforms: List[str],
                           scheduled_time: datetime, image_url: Optional[str] = None,
                           link: Optional[str] = None, is_reel: bool = False,
                           template_id: Optional[str] = None) -> ScheduledPost:
        """
        Schedule a new post

        Args:
            message: Post message
            platforms: Target platforms ['facebook', 'instagram']
            scheduled_time: When to post
            image_url: Optional image URL
            link: Optional link
            is_reel: Whether it's a reel (Instagram)
            template_id: Template used (if any)

        Returns:
            ScheduledPost object
        """
        # Auto-suggest hashtags
        hashtags = self.hashtag_suggester.suggest_hashtags(
            message,
            platform=platforms[0] if len(platforms) == 1 else "both"
        )

        post = ScheduledPost(
            id="",
            message=message,
            platforms=platforms,
            scheduled_time=scheduled_time.isoformat(),
            image_url=image_url,
            link=link,
            is_reel=is_reel,
            status="pending",
            hashtags=hashtags,
            template_id=template_id
        )

        # Add to calendar
        calendar = self._load_calendar()
        calendar.append(asdict(post))
        self._save_calendar(calendar)

        logger.info(f"✅ Post scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        return post

    async def schedule_from_template(self, template_id: str, variables: Dict[str, str],
                                    scheduled_time: datetime, platforms: List[str],
                                    image_url: Optional[str] = None) -> ScheduledPost:
        """
        Schedule a post using a template

        Args:
            template_id: Template to use
            variables: Variables to fill in template
            scheduled_time: When to post
            platforms: Target platforms
            image_url: Optional image URL

        Returns:
            ScheduledPost object
        """
        message = self.templates.render_template(template_id, variables)
        if not message:
            raise ValueError(f"Template {template_id} not found")

        return await self.schedule_post(
            message=message,
            platforms=platforms,
            scheduled_time=scheduled_time,
            image_url=image_url,
            template_id=template_id
        )

    async def get_scheduled_posts(self, start_date: Optional[datetime] = None,
                                  end_date: Optional[datetime] = None) -> List[ScheduledPost]:
        """Get scheduled posts within date range"""
        calendar = self._load_calendar()

        if start_date:
            calendar = [p for p in calendar if p["scheduled_time"] >= start_date.isoformat()]
        if end_date:
            calendar = [p for p in calendar if p["scheduled_time"] <= end_date.isoformat()]

        return [ScheduledPost(**p) for p in calendar]

    async def cancel_post(self, post_id: str) -> bool:
        """Cancel a scheduled post"""
        calendar = self._load_calendar()

        for post in calendar:
            if post["id"] == post_id:
                post["status"] = "cancelled"
                self._save_calendar(calendar)
                logger.info(f"✅ Post {post_id} cancelled")
                return True

        logger.warning(f"Post {post_id} not found")
        return False

    async def get_pending_posts(self) -> List[ScheduledPost]:
        """Get all pending posts"""
        calendar = self._load_calendar()
        pending = [p for p in calendar if p["status"] == "pending"]
        return [ScheduledPost(**p) for p in pending]

    async def mark_post_posted(self, post_id: str, post_ids: Dict[str, str]):
        """Mark a post as posted with actual post IDs"""
        calendar = self._load_calendar()

        for post in calendar:
            if post["id"] == post_id:
                post["status"] = "posted"
                post["posted_at"] = datetime.now().isoformat()
                post["post_ids"] = post_ids
                self._save_calendar(calendar)
                logger.info(f"✅ Post {post_id} marked as posted")
                return True

        return False

    async def generate_calendar_view(self, year: int, month: int) -> ContentCalendar:
        """Generate a calendar view for a specific month"""
        calendar = self._load_calendar()

        # Filter posts for the month
        month_posts = []
        for post in calendar:
            post_date = datetime.fromisoformat(post["scheduled_time"])
            if post_date.year == year and post_date.month == month:
                month_posts.append(ScheduledPost(**post))

        # Calculate statistics
        posts_by_platform = {"facebook": 0, "instagram": 0, "both": 0}
        posts_by_category = {}

        for post in month_posts:
            if "both" in post.platforms:
                posts_by_platform["both"] += 1
            else:
                for platform in post.platforms:
                    posts_by_platform[platform] += 1

            if post.template_id:
                template = self.templates.get_template_by_id(post.template_id)
                if template:
                    category = template["category"]
                    posts_by_category[category] = posts_by_category.get(category, 0) + 1

        return ContentCalendar(
            month=month,
            year=year,
            posts=month_posts,
            total_posts=len(month_posts),
            posts_by_platform=posts_by_platform,
            posts_by_category=posts_by_category
        )


# ============== Analytics Dashboard Generator ==============

class AnalyticsDashboardGenerator:
    """Generates analytics dashboards from post data"""

    def __init__(self, integration=None):
        self.integration = integration
        self.dashboard_file = "dashboards/social_analytics.html"

    async def generate_dashboard(self, start_date: datetime, end_date: datetime) -> str:
        """Generate an HTML analytics dashboard"""
        os.makedirs("dashboards", exist_ok=True)

        # Get calendar data
        calendar_manager = ContentCalendarManager()
        posts = await calendar_manager.get_scheduled_posts(start_date, end_date)

        # Generate HTML
        html_content = self._generate_html(posts, start_date, end_date)

        # Save dashboard
        async with aiofiles.open(self.dashboard_file, "w", encoding="utf-8") as f:
            await f.write(html_content)

        logger.info(f"✅ Dashboard generated: {self.dashboard_file}")
        return self.dashboard_file

    def _generate_html(self, posts: List[ScheduledPost], start_date: datetime,
                      end_date: datetime) -> str:
        """Generate HTML content for dashboard"""

        # Calculate stats
        total_posts = len(posts)
        posted = len([p for p in posts if p.status == "posted"])
        pending = len([p for p in posts if p.status == "pending"])
        cancelled = len([p for p in posts if p.status == "cancelled"])

        platform_counts = {"facebook": 0, "instagram": 0}
        for post in posts:
            if "facebook" in post.platforms:
                platform_counts["facebook"] += 1
            if "instagram" in post.platforms:
                platform_counts["instagram"] += 1

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Analytics Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: white; padding: 30px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .header h1 {{ color: #667eea; margin-bottom: 10px; }}
        .header p {{ color: #666; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; }}
        .stat-card h3 {{ color: #666; font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }}
        .stat-card .number {{ font-size: 48px; font-weight: bold; color: #667eea; }}
        .stat-card.facebook .number {{ color: #1877f2; }}
        .stat-card.instagram .number {{ color: #e4405f; }}
        .posts-section {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .posts-section h2 {{ color: #667eea; margin-bottom: 20px; }}
        .post-item {{ border-left: 4px solid #667eea; padding: 15px; margin-bottom: 15px; background: #f8f9fa; border-radius: 0 10px 10px 0; }}
        .post-item.pending {{ border-left-color: #ffc107; }}
        .post-item.posted {{ border-left-color: #28a745; }}
        .post-item.cancelled {{ border-left-color: #dc3545; }}
        .post-item .meta {{ font-size: 12px; color: #666; margin-bottom: 8px; }}
        .post-item .message {{ color: #333; margin-bottom: 8px; }}
        .post-item .hashtags {{ color: #667eea; font-size: 12px; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
        .badge.pending {{ background: #ffc107; color: #000; }}
        .badge.posted {{ background: #28a745; color: #fff; }}
        .badge.cancelled {{ background: #dc3545; color: #fff; }}
        .chart-container {{ background: white; padding: 30px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Social Media Analytics Dashboard</h1>
            <p>Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}</p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Posts</h3>
                <div class="number">{total_posts}</div>
            </div>
            <div class="stat-card">
                <h3>Posted</h3>
                <div class="number" style="color: #28a745;">{posted}</div>
            </div>
            <div class="stat-card">
                <h3>Pending</h3>
                <div class="number" style="color: #ffc107;">{pending}</div>
            </div>
            <div class="stat-card">
                <h3>Cancelled</h3>
                <div class="number" style="color: #dc3545;">{cancelled}</div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card facebook">
                <h3>Facebook Posts</h3>
                <div class="number">{platform_counts['facebook']}</div>
            </div>
            <div class="stat-card instagram">
                <h3>Instagram Posts</h3>
                <div class="number">{platform_counts['instagram']}</div>
            </div>
        </div>

        <div class="posts-section">
            <h2>📅 Scheduled Posts</h2>
"""

        for post in posts[:50]:  # Limit to 50 posts
            status_badge = f'<span class="badge {post.status}">{post.status}</span>'
            hashtags_str = " ".join(post.hashtags[:5]) if post.hashtags else ""

            html += f"""
            <div class="post-item {post.status}">
                <div class="meta">
                    {status_badge}
                    | 📱 {', '.join(post.platforms)}
                    | 🕐 {datetime.fromisoformat(post.scheduled_time).strftime('%Y-%m-%d %H:%M')}
                </div>
                <div class="message">{post.message[:150]}{'...' if len(post.message) > 150 else ''}</div>
                <div class="hashtags">{hashtags_str}</div>
            </div>
"""

        html += """
        </div>
    </div>
</body>
</html>
"""
        return html


# ============== Main Demo ==============

async def demo():
    """Demonstrate the content calendar features"""

    print("=" * 80)
    print(" SOCIAL MEDIA CONTENT CALENDAR - DEMO")
    print("=" * 80)

    # Initialize managers
    calendar_manager = ContentCalendarManager()
    templates = PostTemplatesLibrary()
    hashtag_suggester = HashtagSuggester()

    # Show available templates
    print("\n📋 Available Post Templates:")
    print("-" * 80)
    for template in templates.get_all_templates():
        print(f"  • {template['name']} ({template['category']})")

    # Demo: Schedule posts from templates
    print("\n📅 Scheduling Posts from Templates:")
    print("-" * 80)

    # Schedule a promotional post for tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_10am = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)

    try:
        promo_post = await calendar_manager.schedule_from_template(
            template_id="template_promotion",
            variables={
                "product_name": "AI Employee Vault",
                "offer_details": "Get 50% off your first month!",
                "expiry_date": "March 31, 2026",
                "call_to_action": "Sign up now at our website!"
            },
            scheduled_time=tomorrow_10am,
            platforms=["facebook", "instagram"]
        )
        print(f"  ✅ Scheduled: Promotion post for {tomorrow_10am.strftime('%Y-%m-%d %H:%M')}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Schedule an engagement post
    tomorrow_2pm = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)

    try:
        engagement_post = await calendar_manager.schedule_from_template(
            template_id="template_engagement",
            variables={
                "engagement_question": "What's your favorite productivity tool?"
            },
            scheduled_time=tomorrow_2pm,
            platforms=["facebook", "instagram"]
        )
        print(f"  ✅ Scheduled: Engagement post for {tomorrow_2pm.strftime('%Y-%m-%d %H:%M')}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Demo: Hashtag suggestions
    print("\n#️⃣ Hashtag Suggestions:")
    print("-" * 80)
    sample_content = "Excited to announce our new AI-powered business automation tool!"
    suggested = hashtag_suggester.suggest_hashtags(sample_content, category="technology", count=10)
    print(f"  Content: {sample_content[:60]}...")
    print(f"  Suggested: {' '.join(suggested)}")

    # Demo: Get pending posts
    print("\n📋 Pending Posts:")
    print("-" * 80)
    pending = await calendar_manager.get_pending_posts()
    for post in pending[-5:]:  # Show last 5
        print(f"  • [{post.status}] {post.message[:50]}... @ {datetime.fromisoformat(post.scheduled_time).strftime('%Y-%m-%d %H:%M')}")

    # Demo: Generate calendar view
    print("\n📊 Generating Calendar View:")
    print("-" * 80)
    current_month = datetime.now().month
    current_year = datetime.now().year
    calendar_view = await calendar_manager.generate_calendar_view(current_year, current_month)
    print(f"  Month: {current_year}-{current_month:02d}")
    print(f"  Total Posts: {calendar_view.total_posts}")
    print(f"  By Platform: {calendar_view.posts_by_platform}")
    print(f"  By Category: {calendar_view.posts_by_category}")

    # Demo: Generate analytics dashboard
    print("\n📈 Generating Analytics Dashboard:")
    print("-" * 80)
    dashboard_gen = AnalyticsDashboardGenerator()
    start = datetime.now() - timedelta(days=30)
    end = datetime.now() + timedelta(days=30)
    dashboard_path = await dashboard_gen.generate_dashboard(start, end)
    print(f"  Dashboard saved to: {dashboard_path}")

    print("\n" + "=" * 80)
    print(" DEMO COMPLETED!")
    print("=" * 80)
    print("\nNext Steps:")
    print("  1. Check 'state/content_calendar.json' for scheduled posts")
    print("  2. Open 'dashboards/social_analytics.html' for analytics")
    print("  3. Check 'state/post_templates.json' for templates")
    print("  4. Use scheduler.py to automatically post at scheduled times")


if __name__ == "__main__":
    asyncio.run(demo())
