"""
Social MCP Server

FastAPI service that integrates with Facebook Graph API, Instagram Graph API,
and Twitter (X) API to manage social media operations like posting messages,
fetching engagement metrics, and generating post summaries.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import time
import hashlib

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiofiles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Social MCP Server", version="1.0.0")


class SocialConfig:
    """Configuration for social media platforms"""
    def __init__(self):
        self.facebook_access_token = os.getenv("FACEBOOK_ACCESS_TOKEN", "")
        self.instagram_access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "")
        self.twitter_api_key = os.getenv("TWITTER_API_KEY", "")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET", "")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN", "")
        self.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")


class JSONRPCResponse(BaseModel):
    """Standard response model"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: str


class PostMessageRequest(BaseModel):
    platform: str  # facebook, instagram, twitter
    message: str
    image_url: Optional[str] = None  # For image posts
    link: Optional[str] = None  # For link posts
    scheduled_time: Optional[str] = None  # ISO format for scheduling


class EngagementMetricsRequest(BaseModel):
    platform: str  # facebook, instagram, twitter
    post_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class PostSummaryRequest(BaseModel):
    platform: str  # facebook, instagram, twitter
    post_id: str


class RateLimitManager:
    """Handles rate limiting for different platforms"""

    def __init__(self):
        # Track requests per platform to respect rate limits
        self.rate_limits = {
            'facebook': {'requests': 0, 'reset_time': 0, 'limit': 200},  # Example limits
            'instagram': {'requests': 0, 'reset_time': 0, 'limit': 200},
            'twitter': {'requests': 0, 'reset_time': 0, 'limit': 300}  # Per 15-min window
        }

    def check_rate_limit(self, platform: str) -> bool:
        """Check if we're under the rate limit for the platform"""
        current_time = time.time()

        # Reset counter if we're past the reset time (15 minutes window)
        if current_time > self.rate_limits[platform]['reset_time']:
            self.rate_limits[platform]['requests'] = 0
            self.rate_limits[platform]['reset_time'] = current_time + 900  # 15 minutes

        if self.rate_limits[platform]['requests'] >= self.rate_limits[platform]['limit']:
            return False

        self.rate_limits[platform]['requests'] += 1
        return True

    def wait_if_needed(self, platform: str):
        """Wait if we're approaching the rate limit"""
        current_time = time.time()

        if current_time > self.rate_limits[platform]['reset_time']:
            self.rate_limits[platform]['requests'] = 0
            self.rate_limits[platform]['reset_time'] = current_time + 900

        # Add a small delay to prevent hitting limits too quickly
        time.sleep(0.1)


class SocialAPIClient:
    """API client for social media platforms"""

    def __init__(self):
        self.config = SocialConfig()
        self.rate_limiter = RateLimitManager()
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(30.0))

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

    async def make_request(self, platform: str, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make an API request with rate limiting and error handling"""

        # Check rate limit
        if not self.rate_limiter.check_rate_limit(platform):
            raise HTTPException(status_code=429, detail=f"Rate limit exceeded for {platform}")

        # Wait briefly to respect rate limits
        self.rate_limiter.wait_if_needed(platform)

        # Add authentication headers based on platform
        headers = kwargs.get('headers', {})

        if platform == 'facebook':
            headers['Authorization'] = f"Bearer {self.config.facebook_access_token}"
        elif platform == 'instagram':
            headers['Authorization'] = f"Bearer {self.config.instagram_access_token}"
        elif platform == 'twitter':
            headers['Authorization'] = f"Bearer {self.config.twitter_bearer_token}"

        kwargs['headers'] = headers

        # Log the request
        await self.log_request(platform, method, url, kwargs)

        try:
            response = await self.client.request(method, url, **kwargs)

            # Log the response
            await self.log_response(platform, method, url, response)

            if response.status_code == 429:  # Rate limit exceeded
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            elif response.status_code >= 400:
                error_detail = response.text if response.text else f"HTTP {response.status_code}"
                raise HTTPException(status_code=response.status_code, detail=error_detail)

            result = response.json() if response.content else {}
            return result

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            await self.log_error(platform, method, url, str(e))
            raise HTTPException(status_code=e.response.status_code, detail=error_msg)

        except httpx.RequestError as e:
            error_msg = f"Request error occurred: {str(e)}"
            logger.error(error_msg)
            await self.log_error(platform, method, url, str(e))
            raise HTTPException(status_code=500, detail=error_msg)

        except Exception as e:
            error_msg = f"Unexpected error occurred: {str(e)}"
            logger.error(error_msg)
            await self.log_error(platform, method, url, str(e))
            raise HTTPException(status_code=500, detail=error_msg)

    async def log_request(self, platform: str, method: str, url: str, kwargs: dict):
        """Log the API request to social_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        request_id = hashlib.md5(f"{timestamp}_{platform}_{method}".encode()).hexdigest()[:8]

        log_entry = f"""
## Request Log - {request_id}
- **Timestamp:** {timestamp}
- **Platform:** {platform}
- **Method:** {method}
- **URL:** {url}
- **Headers:** {json.dumps({k: '***' if k.lower() in ['authorization', 'token'] else v for k, v in kwargs.get('headers', {}).items()}, default=str)}
- **Params:** {json.dumps(kwargs.get('params', {}), default=str)}
- **JSON Data:** {json.dumps(kwargs.get('json', {}), default=str)[:500]}

"""

        async with aiofiles.open("social_log.md", "a", encoding="utf-8") as log_file:
            await log_file.write(log_entry)

    async def log_response(self, platform: str, method: str, url: str, response: httpx.Response):
        """Log the API response to social_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        log_entry = f"""- **Status Code:** {response.status_code}
- **Response:** {response.text[:500]}...

---

"""

        async with aiofiles.open("social_log.md", "a", encoding="utf-8") as log_file:
            await log_file.write(log_entry)

    async def log_error(self, platform: str, method: str, url: str, error: str):
        """Log errors to social_log.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        log_entry = f"""
## Error Log
- **Timestamp:** {timestamp}
- **Platform:** {platform}
- **Method:** {method}
- **URL:** {url}
- **Error:** {error}

---

"""

        async with aiofiles.open("social_log.md", "a", encoding="utf-8") as log_file:
            await log_file.write(log_entry)

    # Facebook API Methods
    async def facebook_post_message(self, message: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """Post a message to Facebook Page"""
        page_id = os.getenv("FACEBOOK_PAGE_ID", "")  # This should be configured

        if image_url:
            # Upload photo first
            upload_url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
            params = {
                'message': message,
                'url': image_url,
                'published': 'false'  # We'll publish after getting the photo ID
            }

            result = await self.make_request('facebook', 'POST', upload_url, params=params)
            photo_id = result.get('id')

            # Now create a post with the photo
            post_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            post_params = {
                'message': message,
                'attached_media[0]': json.dumps({'media_fbid': photo_id})
            }

            return await self.make_request('facebook', 'POST', post_url, params=post_params)
        else:
            # Text-only post
            post_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            params = {
                'message': message
            }

            return await self.make_request('facebook', 'POST', post_url, params=params)

    async def facebook_fetch_engagement_metrics(self, post_id: str) -> Dict[str, Any]:
        """Fetch engagement metrics for a Facebook post"""
        fields = "reactions.summary(true),comments.summary(true),shares,insights.metric(post_impressions,post_reactions_by_type_total,post_clicks)"
        url = f"https://graph.facebook.com/v19.0/{post_id}"
        params = {'fields': fields}

        return await self.make_request('facebook', 'GET', url, params=params)

    # Instagram API Methods
    async def instagram_post_message(self, message: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """Post a message to Instagram"""
        ig_user_id = os.getenv("INSTAGRAM_USER_ID", "")  # This should be configured

        if image_url:
            # Create media container
            container_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
            params = {
                'image_url': image_url,
                'caption': message
            }

            result = await self.make_request('instagram', 'POST', container_url, params=params)
            container_id = result.get('id')

            # Publish the media
            publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
            publish_params = {'creation_id': container_id}

            return await self.make_request('instagram', 'POST', publish_url, params=publish_params)
        else:
            # Text-only post
            url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
            params = {
                'text': message,
                'media_type': 'TEXT_POST'
            }

            result = await self.make_request('instagram', 'POST', url, params=params)
            container_id = result.get('id')

            # Publish the media
            publish_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish"
            publish_params = {'creation_id': container_id}

            return await self.make_request('instagram', 'POST', publish_url, params=publish_params)

    async def instagram_fetch_engagement_metrics(self, post_id: str) -> Dict[str, Any]:
        """Fetch engagement metrics for an Instagram post"""
        fields = "like_count,comments_count,engagement,impressions,reach,saved"
        url = f"https://graph.facebook.com/v19.0/{post_id}"
        params = {'fields': fields}

        return await self.make_request('instagram', 'GET', url, params=params)

    # Twitter API Methods
    async def twitter_post_message(self, message: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """Post a message to Twitter"""
        if image_url:
            # First, we need to upload the media
            # For simplicity in this example, we'll just post the text with a link to the image
            if len(message) + len(image_url) > 280:
                message = message[:280-len(image_url)-5] + "... " + image_url
            else:
                message = message + " " + image_url

        url = "https://api.twitter.com/2/tweets"
        json_data = {
            'text': message
        }

        return await self.make_request('twitter', 'POST', url, json=json_data)

    async def twitter_fetch_engagement_metrics(self, post_id: str) -> Dict[str, Any]:
        """Fetch engagement metrics for a Twitter post"""
        url = f"https://api.twitter.com/2/tweets/{post_id}"
        params = {
            'expansions': 'author_id',
            'tweet.fields': 'public_metrics,created_at,lang',
            'user.fields': 'public_metrics'
        }

        return await self.make_request('twitter', 'GET', url, params=params)


# Initialize the API client
social_client = SocialAPIClient()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    await social_client.close()


@app.post("/post_message", response_model=JSONRPCResponse)
async def post_message(request: PostMessageRequest):
    """Post a message to the specified social media platform"""
    try:
        platform = request.platform.lower()
        message = request.message
        image_url = request.image_url

        if platform not in ['facebook', 'instagram', 'twitter']:
            raise HTTPException(status_code=400, detail="Invalid platform. Supported: facebook, instagram, twitter")

        if platform == 'facebook':
            result = await social_client.facebook_post_message(message, image_url)
        elif platform == 'instagram':
            result = await social_client.instagram_post_message(message, image_url)
        elif platform == 'twitter':
            result = await social_client.twitter_post_message(message, image_url)
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")

        return JSONRPCResponse(
            success=True,
            data={"post_id": result.get('id', 'unknown'), "platform": platform},
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )

    except Exception as e:
        logger.error(f"Error posting message: {str(e)}")
        return JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )


@app.post("/fetch_engagement_metrics", response_model=JSONRPCResponse)
async def fetch_engagement_metrics(request: EngagementMetricsRequest):
    """Fetch engagement metrics for a specific post"""
    try:
        platform = request.platform.lower()
        post_id = request.post_id

        if platform not in ['facebook', 'instagram', 'twitter']:
            raise HTTPException(status_code=400, detail="Invalid platform. Supported: facebook, instagram, twitter")

        if platform == 'facebook':
            result = await social_client.facebook_fetch_engagement_metrics(post_id)
        elif platform == 'instagram':
            result = await social_client.instagram_fetch_engagement_metrics(post_id)
        elif platform == 'twitter':
            result = await social_client.twitter_fetch_engagement_metrics(post_id)
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")

        return JSONRPCResponse(
            success=True,
            data=result,
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )

    except Exception as e:
        logger.error(f"Error fetching engagement metrics: {str(e)}")
        return JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )


@app.post("/generate_post_summary", response_model=JSONRPCResponse)
async def generate_post_summary(request: PostSummaryRequest):
    """Generate a summary of a post and its metrics"""
    try:
        platform = request.platform.lower()
        post_id = request.post_id

        if platform not in ['facebook', 'instagram', 'twitter']:
            raise HTTPException(status_code=400, detail="Invalid platform. Supported: facebook, instagram, twitter")

        # Fetch the post details
        if platform == 'facebook':
            post_data = await social_client.facebook_fetch_engagement_metrics(post_id)
        elif platform == 'instagram':
            post_data = await social_client.instagram_fetch_engagement_metrics(post_id)
        elif platform == 'twitter':
            post_data = await social_client.twitter_fetch_engagement_metrics(post_id)
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")

        # Generate a structured summary based on the platform
        summary = {
            "platform": platform,
            "post_id": post_id,
            "timestamp": datetime.now().isoformat()
        }

        if platform == 'facebook':
            reactions = post_data.get('reactions', {}).get('summary', {}).get('total_count', 0)
            comments = post_data.get('comments', {}).get('summary', {}).get('total_count', 0)
            shares = post_data.get('shares', {}).get('count', 0) if post_data.get('shares') else 0

            summary.update({
                "reactions": reactions,
                "comments": comments,
                "shares": shares,
                "impressions": 0  # Would need to extract from insights
            })
        elif platform == 'instagram':
            like_count = post_data.get('like_count', 0)
            comments_count = post_data.get('comments_count', 0)
            impressions = post_data.get('impressions', 0)
            reach = post_data.get('reach', 0)
            saved = post_data.get('saved', 0)

            summary.update({
                "likes": like_count,
                "comments": comments_count,
                "impressions": impressions,
                "reach": reach,
                "saved": saved
            })
        elif platform == 'twitter':
            public_metrics = post_data.get('data', {}).get('public_metrics', {})
            retweet_count = public_metrics.get('retweet_count', 0)
            like_count = public_metrics.get('like_count', 0)
            reply_count = public_metrics.get('reply_count', 0)
            quote_count = public_metrics.get('quote_count', 0)

            summary.update({
                "retweets": retweet_count,
                "likes": like_count,
                "replies": reply_count,
                "quotes": quote_count
            })

        return JSONRPCResponse(
            success=True,
            data=summary,
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )

    except Exception as e:
        logger.error(f"Error generating post summary: {str(e)}")
        return JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "platforms": ["facebook", "instagram", "twitter"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)