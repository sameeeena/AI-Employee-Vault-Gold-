"""
Facebook & Instagram Integration Module

Handles posting messages and generating summaries for Facebook and Instagram
using the Meta Graph API.

Requirements:
1. Facebook App created at https://developers.facebook.com/
2. Facebook Page Access Token with permissions: pages_manage_posts, pages_read_engagement
3. Instagram Business Account connected to Facebook Page
4. Instagram Graph API access

Setup Guide:
1. Go to https://developers.facebook.com/ and create an app
2. Add Facebook Login product
3. Generate Page Access Token with required permissions
4. Get Instagram Business Account ID
5. Add tokens to .env file
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacebookInstagramIntegration:
    """
    Integration class for Facebook and Instagram posting and analytics.
    
    Supports:
    - Text posts
    - Photo posts (via URL)
    - Link posts
    - Engagement metrics retrieval
    - Post summary generation
    """

    def __init__(self, mock_mode: bool = False):
        """
        Initialize the integration.
        
        Args:
            mock_mode: If True, simulate API calls without actually posting
        """
        self.mock_mode = mock_mode or os.getenv("SOCIAL_MOCK_MODE", "false").lower() == "true"
        
        # Facebook configuration
        self.facebook_access_token = os.getenv("FACEBOOK_ACCESS_TOKEN", "")
        self.facebook_page_id = os.getenv("FACEBOOK_PAGE_ID", "")
        self.facebook_page_access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
        
        # Instagram configuration
        self.instagram_user_id = os.getenv("INSTAGRAM_USER_ID", "")
        self.instagram_access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
        
        # Graph API version
        self.graph_api_version = os.getenv("GRAPH_API_VERSION", "v19.0")
        
        # Base URLs
        self.facebook_base_url = f"https://graph.facebook.com/{self.graph_api_version}"
        self.instagram_base_url = f"https://graph.facebook.com/{self.graph_api_version}"
        
        # HTTP client
        self.timeout = httpx.Timeout(30.0)
        
        if self.mock_mode:
            logger.info("🎭 MOCK MODE enabled - API calls will be simulated")
        else:
            logger.info("🌐 Live mode - API calls will be executed")
            
        # Validate configuration
        self._validate_config()

    def _validate_config(self):
        """Validate that required configuration is present"""
        if not self.mock_mode:
            missing = []
            if not self.facebook_access_token and not self.facebook_page_access_token:
                missing.append("FACEBOOK_ACCESS_TOKEN or FACEBOOK_PAGE_ACCESS_TOKEN")
            if not self.facebook_page_id:
                missing.append("FACEBOOK_PAGE_ID")
            if not self.instagram_user_id:
                missing.append("INSTAGRAM_USER_ID")
            if not self.instagram_access_token:
                missing.append("INSTAGRAM_ACCESS_TOKEN")
            
            if missing:
                logger.warning(f"⚠️ Missing configuration: {', '.join(missing)}")
                logger.warning("Set SOCIAL_MOCK_MODE=true to test without API credentials")

    async def post_to_facebook(self, message: str, image_url: Optional[str] = None,
                               link: Optional[str] = None) -> Dict[str, Any]:
        """
        Post a message to Facebook Page.
        
        Args:
            message: The message/text to post
            image_url: Optional URL of an image to include
            link: Optional link to share
            
        Returns:
            Dictionary with post_id and status
        """
        logger.info(f"📘 Posting to Facebook: {message[:50]}...")
        
        if self.mock_mode:
            return self._mock_facebook_post(message, image_url, link)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Use page access token
                access_token = self.facebook_page_access_token or self.facebook_access_token
                params = {'access_token': access_token}
                
                if image_url:
                    # Post with photo
                    photo_url = f"{self.facebook_base_url}/{self.facebook_page_id}/photos"
                    photo_params = {
                        **params,
                        'url': image_url,
                        'message': message
                    }
                    
                    # First upload the photo
                    photo_response = await client.post(photo_url, params=photo_params)
                    photo_response.raise_for_status()
                    photo_data = photo_response.json()
                    photo_id = photo_data.get('id')
                    
                    # Create post with attached photo
                    post_url = f"{self.facebook_base_url}/{self.facebook_page_id}/feed"
                    post_params = {
                        **params,
                        'message': message,
                        'attached_media': json.dumps({'media_fbid': photo_id})
                    }
                    
                    post_response = await client.post(post_url, params=post_params)
                    post_response.raise_for_status()
                    result = post_response.json()
                    
                elif link:
                    # Post with link
                    post_url = f"{self.facebook_base_url}/{self.facebook_page_id}/feed"
                    post_params = {
                        **params,
                        'message': message,
                        'link': link
                    }
                    
                    post_response = await client.post(post_url, params=post_params)
                    post_response.raise_for_status()
                    result = post_response.json()
                    
                else:
                    # Text-only post
                    post_url = f"{self.facebook_base_url}/{self.facebook_page_id}/feed"
                    post_params = {
                        **params,
                        'message': message
                    }
                    
                    post_response = await client.post(post_url, params=post_params)
                    post_response.raise_for_status()
                    result = post_response.json()
                
                post_result = {
                    "success": True,
                    "platform": "facebook",
                    "post_id": result.get('id', 'unknown'),
                    "message": message[:100],
                    "timestamp": datetime.now().isoformat(),
                    "post_url": f"https://facebook.com/{result.get('id', '')}"
                }
                
                logger.info(f"✅ Facebook post successful! Post ID: {post_result['post_id']}")
                return post_result
                
        except httpx.HTTPStatusError as e:
            error_detail = f"Facebook API Error: {e.response.status_code} - {e.response.text}"
            logger.error(error_detail)
            return {
                "success": False,
                "platform": "facebook",
                "error": error_detail
            }
        except Exception as e:
            error_detail = f"Facebook posting failed: {str(e)}"
            logger.error(error_detail)
            return {
                "success": False,
                "platform": "facebook",
                "error": error_detail
            }

    async def post_to_instagram(self, message: str, image_url: Optional[str] = None,
                                is_reel: bool = False) -> Dict[str, Any]:
        """
        Post a message to Instagram.
        
        Args:
            message: The caption/text to post
            image_url: URL of the image/video to post (required for most post types)
            is_reel: If True, create a Reel instead of a regular post
            
        Returns:
            Dictionary with post_id and status
        """
        logger.info(f"📷 Posting to Instagram: {message[:50]}...")
        
        if self.mock_mode:
            return self._mock_instagram_post(message, image_url, is_reel)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                access_token = self.instagram_access_token or self.facebook_access_token
                params = {'access_token': access_token}
                
                if is_reel:
                    # Create Reel
                    if not image_url:
                        return {
                            "success": False,
                            "platform": "instagram",
                            "error": "Image/video URL required for Reels"
                        }
                    
                    # Create media container for Reel
                    container_url = f"{self.instagram_base_url}/{self.instagram_user_id}/media"
                    container_params = {
                        **params,
                        'media_type': 'REELS',
                        'video_url': image_url,
                        'caption': message
                    }
                    
                    container_response = await client.post(container_url, params=container_params)
                    container_response.raise_for_status()
                    container_data = container_response.json()
                    container_id = container_data.get('id')
                    
                    # Publish the Reel
                    publish_url = f"{self.instagram_base_url}/{self.instagram_user_id}/media_publish"
                    publish_params = {
                        **params,
                        'creation_id': container_id
                    }
                    
                    publish_response = await client.post(publish_url, params=publish_params)
                    publish_response.raise_for_status()
                    result = publish_response.json()
                    
                else:
                    # Regular post
                    media_type = 'IMAGE'
                    
                    if image_url:
                        # Create media container
                        container_url = f"{self.instagram_base_url}/{self.instagram_user_id}/media"
                        container_params = {
                            **params,
                            'media_type': media_type,
                            'image_url': image_url,
                            'caption': message
                        }
                        
                        container_response = await client.post(container_url, params=container_params)
                        container_response.raise_for_status()
                        container_data = container_response.json()
                        container_id = container_data.get('id')
                        
                        # Publish the media
                        publish_url = f"{self.instagram_base_url}/{self.instagram_user_id}/media_publish"
                        publish_params = {
                            **params,
                            'creation_id': container_id
                        }
                        
                        publish_response = await client.post(publish_url, params=publish_params)
                        publish_response.raise_for_status()
                        result = publish_response.json()
                        
                    else:
                        # Text-only post (TEXT_POST media type)
                        container_url = f"{self.instagram_base_url}/{self.instagram_user_id}/media"
                        container_params = {
                            **params,
                            'media_type': 'TEXT_POST',
                            'text': message
                        }
                        
                        container_response = await client.post(container_url, params=container_params)
                        container_response.raise_for_status()
                        container_data = container_response.json()
                        container_id = container_data.get('id')
                        
                        # Publish the media
                        publish_url = f"{self.instagram_base_url}/{self.instagram_user_id}/media_publish"
                        publish_params = {
                            **params,
                            'creation_id': container_id
                        }
                        
                        publish_response = await client.post(publish_url, params=publish_params)
                        publish_response.raise_for_status()
                        result = publish_response.json()
                
                post_result = {
                    "success": True,
                    "platform": "instagram",
                    "post_id": result.get('id', 'unknown'),
                    "media_id": result.get('id', 'unknown'),
                    "message": message[:100],
                    "timestamp": datetime.now().isoformat(),
                    "is_reel": is_reel
                }
                
                logger.info(f"✅ Instagram post successful! Post ID: {post_result['post_id']}")
                return post_result
                
        except httpx.HTTPStatusError as e:
            error_detail = f"Instagram API Error: {e.response.status_code} - {e.response.text}"
            logger.error(error_detail)
            return {
                "success": False,
                "platform": "instagram",
                "error": error_detail
            }
        except Exception as e:
            error_detail = f"Instagram posting failed: {str(e)}"
            logger.error(error_detail)
            return {
                "success": False,
                "platform": "instagram",
                "error": error_detail
            }

    async def post_to_both(self, message: str, image_url: Optional[str] = None,
                           link: Optional[str] = None) -> Dict[str, Any]:
        """
        Post to both Facebook and Instagram simultaneously.
        
        Args:
            message: The message to post
            image_url: Optional image URL
            link: Optional link (Facebook only)
            
        Returns:
            Dictionary with results for both platforms
        """
        logger.info("📱 Posting to both Facebook and Instagram...")
        
        # Post to both platforms in parallel
        facebook_task = self.post_to_facebook(message, image_url, link)
        instagram_task = self.post_to_instagram(message, image_url)
        
        facebook_result, instagram_result = await asyncio.gather(
            facebook_task, instagram_task, return_exceptions=True
        )
        
        # Handle exceptions
        if isinstance(facebook_result, Exception):
            facebook_result = {
                "success": False,
                "platform": "facebook",
                "error": str(facebook_result)
            }
        
        if isinstance(instagram_result, Exception):
            instagram_result = {
                "success": False,
                "platform": "instagram",
                "error": str(instagram_result)
            }
        
        combined_result = {
            "success": facebook_result.get("success", False) or instagram_result.get("success", False),
            "timestamp": datetime.now().isoformat(),
            "facebook": facebook_result,
            "instagram": instagram_result,
            "summary": {
                "total_platforms": 2,
                "successful_posts": sum([
                    1 if facebook_result.get("success") else 0,
                    1 if instagram_result.get("success") else 0
                ])
            }
        }
        
        return combined_result

    async def get_facebook_metrics(self, post_id: str) -> Dict[str, Any]:
        """
        Get engagement metrics for a Facebook post.
        
        Args:
            post_id: The Facebook post ID
            
        Returns:
            Dictionary with engagement metrics
        """
        logger.info(f"📊 Fetching Facebook metrics for post {post_id}")
        
        if self.mock_mode:
            return self._mock_facebook_metrics(post_id)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                access_token = self.facebook_page_access_token or self.facebook_access_token
                params = {
                    'access_token': access_token,
                    'fields': 'reactions.summary(true),comments.summary(true),shares,insights.metric(post_impressions,post_reactions_by_type_total,post_clicks)'
                }
                
                url = f"{self.facebook_base_url}/{post_id}"
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                metrics = {
                    "success": True,
                    "platform": "facebook",
                    "post_id": post_id,
                    "reactions": data.get('reactions', {}).get('summary', {}).get('total_count', 0),
                    "comments": data.get('comments', {}).get('summary', {}).get('total_count', 0),
                    "shares": data.get('shares', {}).get('count', 0) if data.get('shares') else 0,
                    "impressions": 0,  # Would need to extract from insights
                    "timestamp": datetime.now().isoformat()
                }
                
                logger.info(f"✅ Facebook metrics retrieved: {metrics['reactions']} reactions, {metrics['comments']} comments")
                return metrics
                
        except Exception as e:
            error_detail = f"Failed to fetch Facebook metrics: {str(e)}"
            logger.error(error_detail)
            return {
                "success": False,
                "platform": "facebook",
                "error": error_detail
            }

    async def get_instagram_metrics(self, post_id: str) -> Dict[str, Any]:
        """
        Get engagement metrics for an Instagram post.
        
        Args:
            post_id: The Instagram post ID (media ID)
            
        Returns:
            Dictionary with engagement metrics
        """
        logger.info(f"📊 Fetching Instagram metrics for post {post_id}")
        
        if self.mock_mode:
            return self._mock_instagram_metrics(post_id)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                access_token = self.instagram_access_token or self.facebook_access_token
                params = {
                    'access_token': access_token,
                    'fields': 'like_count,comments_count,engagement,impressions,reach,saved'
                }
                
                url = f"{self.instagram_base_url}/{post_id}"
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                metrics = {
                    "success": True,
                    "platform": "instagram",
                    "post_id": post_id,
                    "likes": data.get('like_count', 0),
                    "comments": data.get('comments_count', 0),
                    "impressions": data.get('impressions', 0),
                    "reach": data.get('reach', 0),
                    "saved": data.get('saved', 0),
                    "timestamp": datetime.now().isoformat()
                }
                
                logger.info(f"✅ Instagram metrics retrieved: {metrics['likes']} likes, {metrics['comments']} comments")
                return metrics
                
        except Exception as e:
            error_detail = f"Failed to fetch Instagram metrics: {str(e)}"
            logger.error(error_detail)
            return {
                "success": False,
                "platform": "instagram",
                "error": error_detail
            }

    async def generate_facebook_summary(self, post_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate a summary of Facebook posts and their performance.
        
        Args:
            post_ids: Optional list of specific post IDs to summarize
            
        Returns:
            Dictionary with summary statistics
        """
        logger.info("📊 Generating Facebook summary...")
        
        if self.mock_mode:
            return self._mock_facebook_summary(post_ids)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                access_token = self.facebook_page_access_token or self.facebook_access_token
                
                # Get recent posts from the page
                posts_url = f"{self.facebook_base_url}/{self.facebook_page_id}/feed"
                posts_params = {
                    'access_token': access_token,
                    'fields': 'id,message,created_time,reactions.summary(true),comments.summary(true),shares',
                    'limit': 10
                }
                
                posts_response = await client.get(posts_url, params=posts_params)
                posts_response.raise_for_status()
                posts_data = posts_response.json()
                
                posts = posts_data.get('data', [])
                
                # Calculate summary statistics
                total_posts = len(posts)
                total_reactions = 0
                total_comments = 0
                total_shares = 0
                
                post_summaries = []
                
                for post in posts:
                    reactions = post.get('reactions', {}).get('summary', {}).get('total_count', 0)
                    comments = post.get('comments', {}).get('summary', {}).get('total_count', 0)
                    shares = post.get('shares', {}).get('count', 0) if post.get('shares') else 0
                    
                    total_reactions += reactions
                    total_comments += comments
                    total_shares += shares
                    
                    post_summaries.append({
                        "post_id": post.get('id'),
                        "message": (post.get('message', '')[:50] + '...') if post.get('message') else 'No text',
                        "created_time": post.get('created_time'),
                        "reactions": reactions,
                        "comments": comments,
                        "shares": shares
                    })
                
                summary = {
                    "success": True,
                    "platform": "facebook",
                    "timestamp": datetime.now().isoformat(),
                    "total_posts": total_posts,
                    "total_reactions": total_reactions,
                    "total_comments": total_comments,
                    "total_shares": total_shares,
                    "average_engagement": (total_reactions + total_comments + total_shares) / total_posts if total_posts > 0 else 0,
                    "posts": post_summaries
                }
                
                logger.info(f"✅ Facebook summary generated: {total_posts} posts, {total_reactions} total reactions")
                return summary
                
        except Exception as e:
            error_detail = f"Failed to generate Facebook summary: {str(e)}"
            logger.error(error_detail)
            return {
                "success": False,
                "platform": "facebook",
                "error": error_detail
            }

    async def generate_instagram_summary(self, post_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate a summary of Instagram posts and their performance.
        
        Args:
            post_ids: Optional list of specific post IDs to summarize
            
        Returns:
            Dictionary with summary statistics
        """
        logger.info("📊 Generating Instagram summary...")
        
        if self.mock_mode:
            return self._mock_instagram_summary(post_ids)
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                access_token = self.instagram_access_token or self.facebook_access_token
                
                # Get recent media from the Instagram account
                media_url = f"{self.instagram_base_url}/{self.instagram_user_id}/media"
                media_params = {
                    'access_token': access_token,
                    'fields': 'id,caption,timestamp,like_count,comments_count',
                    'limit': 10
                }
                
                media_response = await client.get(media_url, params=media_params)
                media_response.raise_for_status()
                media_data = media_response.json()
                
                media_items = media_data.get('data', [])
                
                # Calculate summary statistics
                total_posts = len(media_items)
                total_likes = 0
                total_comments = 0
                
                post_summaries = []
                
                for media in media_items:
                    likes = media.get('like_count', 0)
                    comments = media.get('comments_count', 0)
                    
                    total_likes += likes
                    total_comments += comments
                    
                    post_summaries.append({
                        "post_id": media.get('id'),
                        "caption": (media.get('caption', '')[:50] + '...') if media.get('caption') else 'No caption',
                        "timestamp": media.get('timestamp'),
                        "likes": likes,
                        "comments": comments
                    })
                
                summary = {
                    "success": True,
                    "platform": "instagram",
                    "timestamp": datetime.now().isoformat(),
                    "total_posts": total_posts,
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "average_engagement": (total_likes + total_comments) / total_posts if total_posts > 0 else 0,
                    "posts": post_summaries
                }
                
                logger.info(f"✅ Instagram summary generated: {total_posts} posts, {total_likes} total likes")
                return summary
                
        except Exception as e:
            error_detail = f"Failed to generate Instagram summary: {str(e)}"
            logger.error(error_detail)
            return {
                "success": False,
                "platform": "instagram",
                "error": error_detail
            }

    async def generate_combined_summary(self) -> Dict[str, Any]:
        """
        Generate a combined summary of both Facebook and Instagram.
        
        Returns:
            Dictionary with combined summary statistics
        """
        logger.info("📊 Generating combined Facebook & Instagram summary...")
        
        # Import asyncio for gathering results
        import asyncio
        
        facebook_task = self.generate_facebook_summary()
        instagram_task = self.generate_instagram_summary()
        
        facebook_summary, instagram_summary = await asyncio.gather(
            facebook_task, instagram_task, return_exceptions=True
        )
        
        # Handle exceptions
        if isinstance(facebook_summary, Exception):
            facebook_summary = {
                "success": False,
                "platform": "facebook",
                "error": str(facebook_summary)
            }
        
        if isinstance(instagram_summary, Exception):
            instagram_summary = {
                "success": False,
                "platform": "instagram",
                "error": str(instagram_summary)
            }
        
        combined = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "facebook": facebook_summary,
            "instagram": instagram_summary,
            "combined_metrics": {
                "total_posts": (
                    facebook_summary.get("total_posts", 0) +
                    instagram_summary.get("total_posts", 0)
                ),
                "total_engagement": (
                    facebook_summary.get("total_reactions", 0) +
                    facebook_summary.get("total_comments", 0) +
                    facebook_summary.get("total_shares", 0) +
                    instagram_summary.get("total_likes", 0) +
                    instagram_summary.get("total_comments", 0)
                )
            }
        }
        
        return combined

    # Mock methods for testing without API credentials
    def _mock_facebook_post(self, message: str, image_url: Optional[str] = None,
                            link: Optional[str] = None) -> Dict[str, Any]:
        """Mock Facebook post for testing"""
        post_id = f"fb_mock_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            "success": True,
            "platform": "facebook",
            "post_id": post_id,
            "message": message[:100],
            "image_url": image_url,
            "link": link,
            "timestamp": datetime.now().isoformat(),
            "post_url": f"https://facebook.com/{post_id}",
            "mock": True
        }

    def _mock_instagram_post(self, message: str, image_url: Optional[str] = None,
                             is_reel: bool = False) -> Dict[str, Any]:
        """Mock Instagram post for testing"""
        post_id = f"ig_mock_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            "success": True,
            "platform": "instagram",
            "post_id": post_id,
            "message": message[:100],
            "image_url": image_url,
            "is_reel": is_reel,
            "timestamp": datetime.now().isoformat(),
            "mock": True
        }

    def _mock_facebook_metrics(self, post_id: str) -> Dict[str, Any]:
        """Mock Facebook metrics for testing"""
        return {
            "success": True,
            "platform": "facebook",
            "post_id": post_id,
            "reactions": 42,
            "comments": 15,
            "shares": 8,
            "impressions": 1250,
            "timestamp": datetime.now().isoformat(),
            "mock": True
        }

    def _mock_instagram_metrics(self, post_id: str) -> Dict[str, Any]:
        """Mock Instagram metrics for testing"""
        return {
            "success": True,
            "platform": "instagram",
            "post_id": post_id,
            "likes": 128,
            "comments": 23,
            "impressions": 3500,
            "reach": 2800,
            "saved": 45,
            "timestamp": datetime.now().isoformat(),
            "mock": True
        }

    def _mock_facebook_summary(self, post_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Mock Facebook summary for testing"""
        return {
            "success": True,
            "platform": "facebook",
            "timestamp": datetime.now().isoformat(),
            "total_posts": 5,
            "total_reactions": 210,
            "total_comments": 75,
            "total_shares": 40,
            "average_engagement": 65.0,
            "posts": [
                {
                    "post_id": "fb_mock_1",
                    "message": "Sample Facebook Post 1",
                    "created_time": datetime.now().isoformat(),
                    "reactions": 50,
                    "comments": 20,
                    "shares": 10
                }
            ],
            "mock": True
        }

    def _mock_instagram_summary(self, post_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Mock Instagram summary for testing"""
        return {
            "success": True,
            "platform": "instagram",
            "timestamp": datetime.now().isoformat(),
            "total_posts": 5,
            "total_likes": 640,
            "total_comments": 115,
            "average_engagement": 151.0,
            "posts": [
                {
                    "post_id": "ig_mock_1",
                    "caption": "Sample Instagram Post 1",
                    "timestamp": datetime.now().isoformat(),
                    "likes": 150,
                    "comments": 30
                }
            ],
            "mock": True
        }


# Convenience functions for direct usage
async def post_to_facebook(message: str, image_url: Optional[str] = None,
                          link: Optional[str] = None) -> Dict[str, Any]:
    """Post to Facebook"""
    integration = FacebookInstagramIntegration()
    return await integration.post_to_facebook(message, image_url, link)


async def post_to_instagram(message: str, image_url: Optional[str] = None,
                           is_reel: bool = False) -> Dict[str, Any]:
    """Post to Instagram"""
    integration = FacebookInstagramIntegration()
    return await integration.post_to_instagram(message, image_url, is_reel)


async def post_to_both(message: str, image_url: Optional[str] = None,
                      link: Optional[str] = None) -> Dict[str, Any]:
    """Post to both Facebook and Instagram"""
    integration = FacebookInstagramIntegration()
    return await integration.post_to_both(message, image_url, link)


async def generate_summary() -> Dict[str, Any]:
    """Generate combined summary"""
    integration = FacebookInstagramIntegration()
    return await integration.generate_combined_summary()


# Test function
if __name__ == "__main__":
    import asyncio
    import sys
    
    # Fix Windows console encoding for emojis
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    async def test_integration():
        print("=" * 70)
        print("FACEBOOK & INSTAGRAM INTEGRATION TEST")
        print("=" * 70)
        
        integration = FacebookInstagramIntegration(mock_mode=True)
        
        # Test Facebook post
        print("\n[FB] Testing Facebook Post...")
        fb_result = await integration.post_to_facebook(
            message="Hello from AI Employee Vault! Testing Facebook integration. #AI #Automation",
            link="https://example.com"
        )
        print(json.dumps(fb_result, indent=2))
        
        # Test Instagram post
        print("\n[IG] Testing Instagram Post...")
        ig_result = await integration.post_to_instagram(
            message="Beautiful day for Instagram! Testing Instagram integration. #Instagram #AI",
            image_url="https://example.com/image.jpg"
        )
        print(json.dumps(ig_result, indent=2))
        
        # Test posting to both
        print("\n[BOTH] Testing Post to Both Platforms...")
        both_result = await integration.post_to_both(
            message="Cross-posting to Facebook and Instagram! #SocialMedia #Automation"
        )
        print(json.dumps(both_result, indent=2))
        
        # Test Facebook metrics
        print("\n[METRICS] Testing Facebook Metrics...")
        fb_metrics = await integration.get_facebook_metrics("fb_mock_post")
        print(json.dumps(fb_metrics, indent=2))
        
        # Test Instagram metrics
        print("\n[METRICS] Testing Instagram Metrics...")
        ig_metrics = await integration.get_instagram_metrics("ig_mock_post")
        print(json.dumps(ig_metrics, indent=2))
        
        # Test Facebook summary
        print("\n[SUMMARY] Testing Facebook Summary...")
        fb_summary = await integration.generate_facebook_summary()
        print(json.dumps(fb_summary, indent=2))
        
        # Test Instagram summary
        print("\n[SUMMARY] Testing Instagram Summary...")
        ig_summary = await integration.generate_instagram_summary()
        print(json.dumps(ig_summary, indent=2))
        
        # Test combined summary
        print("\n[SUMMARY] Testing Combined Summary...")
        combined_summary = await integration.generate_combined_summary()
        print(json.dumps(combined_summary, indent=2))
        
        print("\n" + "=" * 70)
        print("ALL TESTS COMPLETED!")
        print("=" * 70)
    
    asyncio.run(test_integration())
