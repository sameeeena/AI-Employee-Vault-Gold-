"""
Social MCP Server - Facebook & Instagram Integration

FastAPI service that integrates with Facebook Graph API and Instagram Graph API
to manage social media operations like posting messages and generating summaries.

Features:
- Post to Facebook Page
- Post to Instagram Business Account
- Post to both platforms simultaneously
- Fetch engagement metrics
- Generate post summaries
- Combined analytics dashboard

Setup:
1. Configure environment variables in .env file
2. Run: python social_mcp_server.py
3. Server will start on http://localhost:8002
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
import hashlib
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Import the Facebook/Instagram integration module
from facebook_instagram_integration import FacebookInstagramIntegration

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan handler for startup/shutdown events"""
    logger.info("Initializing Social MCP Server...")
    logger.info("Social MCP Server ready")
    yield
    logger.info("Shutting down Social MCP Server...")


app = FastAPI(
    title="Social MCP Server",
    version="2.0.0",
    lifespan=lifespan,
    description="Facebook & Instagram integration for posting and analytics"
)


# ============== Request/Response Models ==============

class JSONRPCResponse(BaseModel):
    """Standard response model"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: str


class PostMessageRequest(BaseModel):
    """Request model for posting messages"""
    platform: str  # facebook, instagram, both
    message: str
    image_url: Optional[str] = None
    link: Optional[str] = None
    is_reel: Optional[bool] = False


class EngagementMetricsRequest(BaseModel):
    """Request model for fetching engagement metrics"""
    platform: str  # facebook, instagram
    post_id: str


class PostSummaryRequest(BaseModel):
    """Request model for generating post summary"""
    platform: str  # facebook, instagram, both
    post_id: Optional[str] = None


# ============== Social Media Manager ==============

class SocialMediaManager:
    """Manages Facebook and Instagram operations"""

    def __init__(self):
        mock_mode = os.getenv("SOCIAL_MOCK_MODE", "true").lower() == "true"
        self.integration = FacebookInstagramIntegration(mock_mode=mock_mode)
        logger.info(f"SocialMediaManager initialized (mock_mode={mock_mode})")

    async def post_message(self, platform: str, message: str,
                          image_url: Optional[str] = None,
                          link: Optional[str] = None,
                          is_reel: bool = False) -> Dict[str, Any]:
        """
        Post message to specified platform(s).
        
        Args:
            platform: facebook, instagram, or both
            message: Message text
            image_url: Optional image URL
            link: Optional link (Facebook only)
            is_reel: If True, create Instagram Reel
            
        Returns:
            Post result dictionary
        """
        platform = platform.lower()
        
        if platform == "facebook":
            return await self.integration.post_to_facebook(message, image_url, link)
        
        elif platform == "instagram":
            return await self.integration.post_to_instagram(message, image_url, is_reel)
        
        elif platform == "both":
            return await self.integration.post_to_both(message, image_url, link)
        
        else:
            return {
                "success": False,
                "error": f"Unsupported platform: {platform}. Supported: facebook, instagram, both"
            }

    async def get_metrics(self, platform: str, post_id: str) -> Dict[str, Any]:
        """
        Get engagement metrics for a post.
        
        Args:
            platform: facebook or instagram
            post_id: Post ID
            
        Returns:
            Metrics dictionary
        """
        platform = platform.lower()
        
        if platform == "facebook":
            return await self.integration.get_facebook_metrics(post_id)
        
        elif platform == "instagram":
            return await self.integration.get_instagram_metrics(post_id)
        
        else:
            return {
                "success": False,
                "error": f"Unsupported platform: {platform}"
            }

    async def generate_summary(self, platform: str = "both") -> Dict[str, Any]:
        """
        Generate summary of posts and performance.
        
        Args:
            platform: facebook, instagram, or both
            
        Returns:
            Summary dictionary
        """
        platform = platform.lower()
        
        if platform == "facebook":
            return await self.integration.generate_facebook_summary()
        
        elif platform == "instagram":
            return await self.integration.generate_instagram_summary()
        
        elif platform == "both":
            return await self.integration.generate_combined_summary()
        
        else:
            return {
                "success": False,
                "error": f"Unsupported platform: {platform}"
            }


# Global instance
social_manager = SocialMediaManager()


# ============== API Endpoints ==============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    mock_mode = os.getenv("SOCIAL_MOCK_MODE", "true").lower() == "true"
    return {
        "status": "healthy",
        "service": "Social MCP Server",
        "timestamp": datetime.now().isoformat(),
        "platforms": ["facebook", "instagram"],
        "mock_mode": mock_mode
    }


@app.post("/api/post_message", response_model=JSONRPCResponse)
async def post_message(request: PostMessageRequest):
    """
    Post a message to Facebook, Instagram, or both.
    
    **Facebook:**
    - Supports text, photo, and link posts
    - Requires Facebook Page Access Token
    
    **Instagram:**
    - Supports text, photo, and Reel posts
    - Requires Instagram Business Account
    
    **Both:**
    - Posts to both platforms simultaneously
    - Returns combined result
    """
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.message[:50]}".encode()).hexdigest()[:12]
    
    try:
        result = await social_manager.post_message(
            platform=request.platform,
            message=request.message,
            image_url=request.image_url,
            link=request.link,
            is_reel=request.is_reel
        )
        
        if result.get("success"):
            response = JSONRPCResponse(
                success=True,
                data=result,
                request_id=request_id
            )
        else:
            response = JSONRPCResponse(
                success=False,
                error=result.get("error", "Unknown error"),
                request_id=request_id
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error posting message: {str(e)}")
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        return response


@app.post("/api/get_metrics", response_model=JSONRPCResponse)
async def get_metrics(request: EngagementMetricsRequest):
    """
    Get engagement metrics for a specific post.
    
    **Facebook Metrics:**
    - Reactions (likes, loves, etc.)
    - Comments
    - Shares
    - Impressions
    
    **Instagram Metrics:**
    - Likes
    - Comments
    - Impressions
    - Reach
    - Saves
    """
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.post_id}".encode()).hexdigest()[:12]
    
    try:
        result = await social_manager.get_metrics(
            platform=request.platform,
            post_id=request.post_id
        )
        
        if result.get("success"):
            response = JSONRPCResponse(
                success=True,
                data=result,
                request_id=request_id
            )
        else:
            response = JSONRPCResponse(
                success=False,
                error=result.get("error", "Unknown error"),
                request_id=request_id
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        return response


@app.post("/api/generate_summary", response_model=JSONRPCResponse)
async def generate_summary(request: PostSummaryRequest):
    """
    Generate a summary of posts and their performance.
    
    **Facebook Summary:**
    - Total posts
    - Total reactions, comments, shares
    - Average engagement rate
    - Recent posts list
    
    **Instagram Summary:**
    - Total posts
    - Total likes, comments
    - Average engagement rate
    - Recent media list
    
    **Both:**
    - Combined metrics from both platforms
    - Cross-platform comparison
    """
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{request.platform}".encode()).hexdigest()[:12]
    
    try:
        result = await social_manager.generate_summary(platform=request.platform)
        
        if result.get("success"):
            response = JSONRPCResponse(
                success=True,
                data=result,
                request_id=request_id
            )
        else:
            response = JSONRPCResponse(
                success=False,
                error=result.get("error", "Unknown error"),
                request_id=request_id
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        return response


@app.get("/api/get_summary", response_model=JSONRPCResponse)
async def get_summary(platform: str = "both"):
    """
    GET endpoint for generating summary.
    Convenience endpoint for simple GET requests.
    """
    request_id = hashlib.md5(f"{datetime.now().isoformat()}{platform}".encode()).hexdigest()[:12]
    
    try:
        result = await social_manager.generate_summary(platform=platform)
        
        if result.get("success"):
            response = JSONRPCResponse(
                success=True,
                data=result,
                request_id=request_id
            )
        else:
            response = JSONRPCResponse(
                success=False,
                error=result.get("error", "Unknown error"),
                request_id=request_id
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        response = JSONRPCResponse(
            success=False,
            error=str(e),
            request_id=request_id
        )
        return response


# ============== Main Entry Point ==============

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.getenv("SOCIAL_MCP_PORT", "8002"))
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
    
    logger.info(f"Social MCP Server started on port {port}")
