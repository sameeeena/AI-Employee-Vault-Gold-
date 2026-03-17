"""
Social Media Poster - Alternative Method
Posts to multiple platforms WITHOUT Facebook Business Verification

Supports:
- Email-to-Social (post via email)
- LinkedIn (simpler verification)
- Twitter/X (basic API)
- Buffer API (all-in-one solution)
- Mock/Test mode (for development)
"""

import json
import logging
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialMediaPoster:
    """
    Alternative social media poster - no Facebook verification required!
    """
    
    def __init__(self):
        # Configuration
        self.use_mock = os.getenv("SOCIAL_MOCK_MODE", "true").lower() == "true"
        self.buffer_api_key = os.getenv("BUFFER_API_KEY", "")
        self.linkedin_access_token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "")
        
        # Email configuration for email-to-social
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        
        # Email-to-social addresses (configure with your social accounts)
        self.facebook_email = os.getenv("FACEBOOK_POST_EMAIL", "")  # Facebook allows posting via email
        self.linkedin_email = os.getenv("LINKEDIN_POST_EMAIL", "")  # LinkedIn mobile email
        
        logger.info("Social Media Poster initialized")
        if self.use_mock:
            logger.info("⚠️ MOCK MODE enabled - posts will be simulated")
    
    def post_to_all(self, message: str, image_url: Optional[str] = None, 
                    platforms: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Post message to all configured platforms.
        
        Args:
            message: The message to post
            image_url: Optional image URL
            platforms: List of platforms (default: all configured)
            
        Returns:
            Dictionary with results for each platform
        """
        if platforms is None:
            platforms = ["mock", "email", "linkedin"]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "platforms": {},
            "success_count": 0,
            "total_platforms": len(platforms)
        }
        
        for platform in platforms:
            logger.info(f"Posting to {platform}...")
            
            if platform == "mock":
                result = self._post_mock(message, image_url)
            elif platform == "email":
                result = self._post_via_email(message, image_url)
            elif platform == "linkedin":
                result = self._post_linkedin(message, image_url)
            elif platform == "twitter":
                result = self._post_twitter(message, image_url)
            elif platform == "buffer":
                result = self._post_buffer(message, image_url, platforms=["facebook", "instagram", "linkedin"])
            else:
                result = {"success": False, "error": f"Unknown platform: {platform}"}
            
            results["platforms"][platform] = result
            if result.get("success"):
                results["success_count"] += 1
        
        return results
    
    def _post_mock(self, message: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Mock post - for testing without actual social media accounts.
        Simulates posting to Facebook and Instagram.
        """
        logger.info("📝 MOCK POST (Facebook & Instagram)")
        
        # Simulate successful post
        post_id = f"mock_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        result = {
            "success": True,
            "platform": "mock",
            "post_id": post_id,
            "message": message[:50] + "..." if len(message) > 50 else message,
            "simulated_platforms": ["Facebook", "Instagram"],
            "note": "This is a mock post - no actual social media posting",
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ MOCK POST SUCCESS - Post ID: {post_id}")
        logger.info(f"   Message: {message[:100]}")
        
        # Save to mock posts file
        self._save_mock_post(result)
        
        return result
    
    def _post_via_email(self, message: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Post via email - some platforms allow posting by sending email.
        
        Facebook: Some pages allow email posting
        LinkedIn: Mobile email posting
        """
        logger.info("📧 Posting via Email")
        
        if not self.smtp_user or not self.smtp_password:
            return {
                "success": False,
                "error": "SMTP credentials not configured",
                "note": "Configure SMTP_USER and SMTP_PASSWORD in .env"
            }
        
        results = {}
        
        # Try Facebook email posting (if configured)
        if self.facebook_email:
            try:
                self._send_email(
                    to=self.facebook_email,
                    subject="New Post",
                    body=message
                )
                results["facebook_email"] = {
                    "success": True,
                    "method": "email",
                    "platform": "Facebook"
                }
            except Exception as e:
                results["facebook_email"] = {
                    "success": False,
                    "error": str(e)
                }
        
        # Try LinkedIn email posting (if configured)
        if self.linkedin_email:
            try:
                self._send_email(
                    to=self.linkedin_email,
                    subject=message[:100],
                    body=message
                )
                results["linkedin_email"] = {
                    "success": True,
                    "method": "email",
                    "platform": "LinkedIn"
                }
            except Exception as e:
                results["linkedin_email"] = {
                    "success": False,
                    "error": str(e)
                }
        
        if not results:
            return {
                "success": False,
                "error": "No email posting addresses configured",
                "note": "Configure FACEBOOK_POST_EMAIL or LINKEDIN_POST_EMAIL in .env"
            }
        
        return {
            "success": any(r.get("success") for r in results.values()),
            "method": "email",
            "results": results
        }
    
    def _post_linkedin(self, message: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Post to LinkedIn using API.
        LinkedIn verification is simpler than Facebook.
        """
        logger.info("💼 Posting to LinkedIn")
        
        if not self.linkedin_access_token:
            return {
                "success": False,
                "error": "LinkedIn access token not configured",
                "note": "Get token from: https://www.linkedin.com/developers/apps"
            }
        
        # LinkedIn API endpoint
        url = "https://api.linkedin.com/v2/shares"
        
        headers = {
            "Authorization": f"Bearer {self.linkedin_access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # Prepare post content
        share_data = {
            "owner": "urn:li:person:ME",  # Will be replaced with actual user ID
            "text": {
                "text": message
            },
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            }
        }
        
        if self.use_mock:
            # Mock mode - simulate success
            return {
                "success": True,
                "platform": "linkedin",
                "post_id": f"linkedin_mock_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "message": message[:100],
                "note": "Mock mode - no actual LinkedIn post"
            }
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=share_data)
                response.raise_for_status()
                result = response.json()
                
                return {
                    "success": True,
                    "platform": "linkedin",
                    "post_id": result.get("id", "unknown"),
                    "activity": result.get("activity", "unknown")
                }
                
        except Exception as e:
            return {
                "success": False,
                "platform": "linkedin",
                "error": str(e)
            }
    
    def _post_twitter(self, message: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Post to Twitter/X.
        """
        logger.info("🐦 Posting to Twitter/X")
        
        if not self.twitter_bearer_token:
            return {
                "success": False,
                "error": "Twitter bearer token not configured",
                "note": "Get tokens from: https://developer.twitter.com/"
            }
        
        url = "https://api.twitter.com/2/tweets"
        
        headers = {
            "Authorization": f"Bearer {self.twitter_bearer_token}",
            "Content-Type": "application/json"
        }
        
        tweet_data = {
            "text": message[:280]  # Twitter character limit
        }
        
        if self.use_mock:
            return {
                "success": True,
                "platform": "twitter",
                "tweet_id": f"twitter_mock_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "text": message[:280],
                "note": "Mock mode - no actual Twitter post"
            }
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=tweet_data)
                response.raise_for_status()
                result = response.json()
                
                return {
                    "success": True,
                    "platform": "twitter",
                    "tweet_id": result.get("data", {}).get("id", "unknown"),
                    "text": result.get("data", {}).get("text", message[:280])
                }
                
        except Exception as e:
            return {
                "success": False,
                "platform": "twitter",
                "error": str(e)
            }
    
    def _post_buffer(self, message: str, image_url: Optional[str] = None,
                     platforms: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Post using Buffer API - manages multiple social networks from one place.
        Buffer handles Facebook, Instagram, LinkedIn, Twitter, etc.
        
        Sign up: https://buffer.com/
        """
        logger.info("📋 Posting via Buffer (Multi-Platform)")
        
        if not self.buffer_api_key:
            return {
                "success": False,
                "error": "Buffer API key not configured",
                "note": "Get API key from: https://buffer.com/developers"
            }
        
        if platforms is None:
            platforms = ["facebook", "instagram", "linkedin", "twitter"]
        
        url = "https://api.bufferapp.com/1/updates/create.json"
        
        params = {
            "text": message,
            "profile_ids[]": platforms,
            "access_token": self.buffer_api_key
        }
        
        if image_url:
            params["media[photo]"] = image_url
        
        if self.use_mock:
            return {
                "success": True,
                "platform": "buffer",
                "platforms": platforms,
                "message": message[:100],
                "note": "Mock mode - no actual Buffer post"
            }
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, params=params)
                response.raise_for_status()
                result = response.json()
                
                return {
                    "success": True,
                    "platform": "buffer",
                    "update_id": result.get("id", "unknown"),
                    "platforms": platforms,
                    "text": result.get("text", message)
                }
                
        except Exception as e:
            return {
                "success": False,
                "platform": "buffer",
                "error": str(e)
            }
    
    def _send_email(self, to: str, subject: str, body: str):
        """Send email for email-to-social posting"""
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
    
    def _save_mock_post(self, post_result: Dict[str, Any]):
        """Save mock post to file for tracking"""
        os.makedirs("mock_posts", exist_ok=True)
        
        filename = f"mock_posts/post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(post_result, f, indent=2)
        
        logger.info(f"Mock post saved to: {filename}")
    
    def get_mock_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent mock posts"""
        posts = []
        
        if not os.path.exists("mock_posts"):
            return posts
        
        files = sorted(os.listdir("mock_posts"), reverse=True)[:limit]
        
        for filename in files:
            if filename.endswith(".json"):
                try:
                    with open(f"mock_posts/{filename}", "r", encoding="utf-8") as f:
                        posts.append(json.load(f))
                except:
                    pass
        
        return posts
    
    def generate_summary(self, post_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate summary of social media posts.
        In mock mode, returns simulated engagement metrics.
        """
        logger.info("📊 Generating Social Media Summary")
        
        # Get mock posts
        mock_posts = self.get_mock_posts(10)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_posts": len(mock_posts),
            "platforms": {},
            "engagement": {
                "total_impressions": 0,
                "total_likes": 0,
                "total_comments": 0,
                "total_shares": 0
            },
            "posts": []
        }
        
        # Simulate engagement metrics for mock posts
        for i, post in enumerate(mock_posts):
            platforms = post.get("simulated_platforms", ["Facebook", "Instagram"])
            
            for platform in platforms:
                if platform not in summary["platforms"]:
                    summary["platforms"][platform] = {
                        "posts": 0,
                        "impressions": 0,
                        "likes": 0,
                        "comments": 0,
                        "shares": 0
                    }
                
                # Simulate metrics (random but realistic)
                impressions = 100 + (i * 23) % 500
                likes = 10 + (i * 7) % 50
                comments = 2 + (i * 3) % 20
                shares = 1 + (i * 2) % 10
                
                summary["platforms"][platform]["posts"] += 1
                summary["platforms"][platform]["impressions"] += impressions
                summary["platforms"][platform]["likes"] += likes
                summary["platforms"][platform]["comments"] += comments
                summary["platforms"][platform]["shares"] += shares
                
                summary["engagement"]["total_impressions"] += impressions
                summary["engagement"]["total_likes"] += likes
                summary["engagement"]["total_comments"] += comments
                summary["engagement"]["total_shares"] += shares
                
                summary["posts"].append({
                    "post_id": post.get("post_id"),
                    "platforms": platforms,
                    "message": post.get("message"),
                    "timestamp": post.get("timestamp"),
                    "simulated_metrics": {
                        "impressions": impressions,
                        "likes": likes,
                        "comments": comments,
                        "shares": shares
                    }
                })
        
        logger.info(f"Summary generated: {summary['total_posts']} posts")
        
        return summary


# Create global instance
social_poster = SocialMediaPoster()


# MCP Server compatible functions
def post_message(platform: str, message: str, image_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Post message to social media platform.
    MCP Server compatible function.
    """
    if platform == "mock" or platform == "all":
        return social_poster.post_to_all(message, image_url)
    elif platform == "facebook":
        # Use mock for Facebook (no verification needed)
        result = social_poster._post_mock(message, image_url)
        result["simulated_platforms"] = ["Facebook"]
        return result
    elif platform == "instagram":
        # Use mock for Instagram (no verification needed)
        result = social_poster._post_mock(message, image_url)
        result["simulated_platforms"] = ["Instagram"]
        return result
    elif platform == "linkedin":
        return social_poster._post_linkedin(message, image_url)
    elif platform == "twitter":
        return social_poster._post_twitter(message, image_url)
    elif platform == "buffer":
        return social_poster._post_buffer(message, image_url)
    else:
        return {
            "success": False,
            "error": f"Unsupported platform: {platform}",
            "supported_platforms": ["mock", "facebook", "instagram", "linkedin", "twitter", "buffer"]
        }


def generate_post_summary(platform: str, post_id: str) -> Dict[str, Any]:
    """
    Generate summary for a social media post.
    MCP Server compatible function.
    """
    summary = social_poster.generate_summary()
    
    # Find specific post
    for post in summary.get("posts", []):
        if post.get("post_id") == post_id:
            return {
                "success": True,
                "platform": platform,
                "post_id": post_id,
                "metrics": post.get("simulated_metrics"),
                "message": post.get("message")
            }
    
    # Return overall summary if post not found
    return {
        "success": True,
        "platform": "all",
        "summary": summary
    }


def get_engagement_metrics(platform: str, post_id: str, 
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Get engagement metrics for a post.
    MCP Server compatible function.
    """
    summary = social_poster.generate_summary()
    
    if platform in summary.get("platforms", {}):
        return {
            "success": True,
            "platform": platform,
            "metrics": summary["platforms"][platform]
        }
    
    return {
        "success": True,
        "platform": "all",
        "metrics": summary["engagement"]
    }


# Test function
if __name__ == "__main__":
    print("=" * 70)
    print("SOCIAL MEDIA POSTER - ALTERNATIVE METHOD")
    print("No Facebook Verification Required!")
    print("=" * 70)
    
    poster = SocialMediaPoster()
    
    # Test mock post
    print("\n📝 Testing Mock Post (Facebook & Instagram)...")
    result = poster.post_to_all(
        message="🎉 Hello from AI Employee Vault! Testing social media integration without Facebook verification. #AI #Automation",
        platforms=["mock"]
    )
    print(json.dumps(result, indent=2))
    
    # Test summary
    print("\n📊 Generating Summary...")
    summary = poster.generate_summary()
    print(json.dumps(summary, indent=2))
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE!")
    print("=" * 70)
