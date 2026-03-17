# ✅ FACEBOOK & INSTAGRAM INTEGRATION - COMPLETE GUIDE
## Post Messages and Generate Summaries

**Status:** ✅ COMPLETE | **Version:** 2.0.0 | **Date:** 2026-03-07

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [Configuration](#configuration)
6. [Quick Start](#quick-start)
7. [API Reference](#api-reference)
8. [Usage Examples](#usage-examples)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This integration provides seamless connectivity to **Facebook Pages** and **Instagram Business Accounts** through the Meta Graph API. You can:

- ✅ Post messages to Facebook
- ✅ Post messages to Instagram
- ✅ Post to both platforms simultaneously
- ✅ Fetch engagement metrics (likes, comments, shares, impressions)
- ✅ Generate comprehensive performance summaries
- ✅ Track cross-platform analytics

---

## ✨ Features

### Posting Capabilities

| Feature | Facebook | Instagram |
|---------|----------|-----------|
| Text Posts | ✅ | ✅ |
| Photo Posts | ✅ | ✅ |
| Link Posts | ✅ | ❌ |
| Reels | ❌ | ✅ |
| Cross-Posting | ✅ Both simultaneously |

### Analytics & Summaries

| Metric | Facebook | Instagram |
|--------|----------|-----------|
| Reactions/Likes | ✅ | ✅ |
| Comments | ✅ | ✅ |
| Shares | ✅ | ❌ |
| Impressions | ✅ | ✅ |
| Reach | ❌ | ✅ |
| Saves | ❌ | ✅ |
| Engagement Rate | ✅ | ✅ |

---

## 📋 Prerequisites

### 1. Facebook Requirements

- **Facebook Developer Account**: https://developers.facebook.com/
- **Facebook App** created
- **Facebook Page** with admin access
- **Page Access Token** with permissions:
  - `pages_manage_posts`
  - `pages_read_engagement`
  - `pages_show_list`

### 2. Instagram Requirements

- **Instagram Business Account** (convert from personal in Instagram settings)
- **Instagram account connected to Facebook Page**
- **Instagram Graph API** access enabled in Facebook App

### 3. Python Requirements

```bash
pip install fastapi uvicorn httpx python-dotenv pydantic aiofiles
```

---

## 🔧 Setup Instructions

### Step 1: Create Facebook App

1. Go to https://developers.facebook.com/
2. Click **"My Apps"** → **"Create App"**
3. Select **"Business"** as app type
4. Fill in app details:
   - App Name: `AI Employee Vault Social`
   - App Contact Email: your email
5. Click **"Create App"**

### Step 2: Add Instagram Graph API

1. In your App Dashboard, click **"Add Product"**
2. Find **"Instagram Graph API"** and click **"Set Up"**
3. Accept the terms

### Step 3: Get Page Access Token

1. Go to **Graph API Explorer**: https://developers.facebook.com/tools/explorer/
2. Select your app from dropdown
3. Click **"Get Token"** → **"Get Page Access Token"**
4. Select your Facebook Page
5. Check permissions:
   - ✅ `pages_manage_posts`
   - ✅ `pages_read_engagement`
   - ✅ `pages_show_list`
6. Click **"Get Access Token"**
7. Copy the token

### Step 4: Get Instagram User ID

1. In Graph API Explorer, run this query:
   ```
   GET /me/accounts
   ```
2. Find your page and copy the `id`
3. Then run:
   ```
   GET /{page-id}?fields=instagram_business_account
   ```
4. Copy the Instagram Business Account ID

### Step 5: Configure Environment Variables

Edit your `.env` file:

```bash
# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=your_page_access_token_here
FACEBOOK_PAGE_ID=your_facebook_page_id_here

# Instagram Configuration
INSTAGRAM_USER_ID=your_instagram_business_account_id
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token

# Graph API Version
GRAPH_API_VERSION=v19.0

# Mock Mode (set to false for live posting)
SOCIAL_MOCK_MODE=false
```

---

## ⚙️ Configuration

### Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `FACEBOOK_ACCESS_TOKEN` | Facebook Page Access Token | ✅ | `EAAV...` |
| `FACEBOOK_PAGE_ID` | Your Facebook Page ID | ✅ | `123456789012345` |
| `INSTAGRAM_USER_ID` | Instagram Business Account ID | ✅ | `17841400000000000` |
| `INSTAGRAM_ACCESS_TOKEN` | Instagram Access Token | ✅ | `EAAV...` |
| `GRAPH_API_VERSION` | Meta Graph API version | ❌ | `v19.0` |
| `SOCIAL_MOCK_MODE` | Enable mock mode for testing | ❌ | `true` or `false` |

---

## 🚀 Quick Start

### 1. Test in Mock Mode (Recommended First)

```bash
# Run the test script
python test_facebook_instagram.py
```

Expected output:
```
================================================================================
 FACEBOOK & INSTAGRAM INTEGRATION - TEST SUITE
================================================================================
✅ Module imported successfully
✅ Integration initialized (Mock Mode)

--------------------------------------------------------------------------------
 TEST 1: Post to Facebook
--------------------------------------------------------------------------------
✅ Facebook Post Successful!
   Post ID: fb_mock_20260307120000
   Message: 🎉 Hello from AI Employee Vault!
```

### 2. Start the MCP Server

```bash
# Start the server
python social_mcp_server_v2.py

# Server will start on http://localhost:8002
```

### 3. Access API Documentation

Open your browser to:
```
http://localhost:8002/docs
```

This shows the interactive Swagger UI with all API endpoints.

### 4. Make Your First API Call

```bash
# Post to Facebook
curl -X POST "http://localhost:8002/api/post_message" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "facebook",
    "message": "Hello from AI Employee Vault! 🚀"
  }'
```

---

## 📖 API Reference

### Base URL
```
http://localhost:8002
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Social MCP Server",
  "timestamp": "2026-03-07T12:00:00",
  "platforms": ["facebook", "instagram"],
  "mock_mode": true
}
```

---

#### 2. Post Message
```http
POST /api/post_message
```

**Request Body:**
```json
{
  "platform": "facebook",
  "message": "Your message here",
  "image_url": "https://example.com/image.jpg",
  "link": "https://example.com",
  "is_reel": false
}
```

**Platform Options:**
- `facebook` - Post to Facebook only
- `instagram` - Post to Instagram only
- `both` - Post to both platforms simultaneously

**Response:**
```json
{
  "success": true,
  "data": {
    "post_id": "123456789012345_987654321098765",
    "platform": "facebook",
    "message": "Your message here",
    "timestamp": "2026-03-07T12:00:00",
    "post_url": "https://facebook.com/123456789012345_987654321098765"
  },
  "request_id": "abc123def456"
}
```

---

#### 3. Get Engagement Metrics
```http
POST /api/get_metrics
```

**Request Body:**
```json
{
  "platform": "facebook",
  "post_id": "123456789012345_987654321098765"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "platform": "facebook",
    "post_id": "123456789012345_987654321098765",
    "reactions": 42,
    "comments": 15,
    "shares": 8,
    "impressions": 1250,
    "timestamp": "2026-03-07T12:00:00"
  },
  "request_id": "abc123def456"
}
```

---

#### 4. Generate Summary
```http
POST /api/generate_summary
```

**Request Body:**
```json
{
  "platform": "both"
}
```

**Platform Options:**
- `facebook` - Facebook summary only
- `instagram` - Instagram summary only
- `both` - Combined summary

**Response (Combined):**
```json
{
  "success": true,
  "data": {
    "timestamp": "2026-03-07T12:00:00",
    "facebook": {
      "total_posts": 5,
      "total_reactions": 210,
      "total_comments": 75,
      "total_shares": 40,
      "average_engagement": 65.0,
      "posts": [...]
    },
    "instagram": {
      "total_posts": 5,
      "total_likes": 640,
      "total_comments": 115,
      "average_engagement": 151.0,
      "posts": [...]
    },
    "combined_metrics": {
      "total_posts": 10,
      "total_engagement": 1080
    }
  },
  "request_id": "abc123def456"
}
```

---

#### 5. Get Summary (GET endpoint)
```http
GET /api/get_summary?platform=both
```

---

## 💡 Usage Examples

### Example 1: Post Text to Facebook

```python
import httpx

response = httpx.post("http://localhost:8002/api/post_message", json={
    "platform": "facebook",
    "message": "🎉 Exciting news from our team! Stay tuned for more updates. #CompanyNews"
})

print(response.json())
```

### Example 2: Post Photo to Instagram

```python
import httpx

response = httpx.post("http://localhost:8002/api/post_message", json={
    "platform": "instagram",
    "message": "🌟 Behind the scenes at our office! #TeamLife #CompanyCulture",
    "image_url": "https://example.com/office-photo.jpg"
})

print(response.json())
```

### Example 3: Cross-Post to Both Platforms

```python
import httpx

response = httpx.post("http://localhost:8002/api/post_message", json={
    "platform": "both",
    "message": "🚀 Big announcement! We're launching a new product next week. #ProductLaunch",
    "image_url": "https://example.com/product-teaser.jpg"
})

print(response.json())
```

### Example 4: Get Post Performance

```python
import httpx

# Get Facebook post metrics
response = httpx.post("http://localhost:8002/api/get_metrics", json={
    "platform": "facebook",
    "post_id": "123456789012345_987654321098765"
})

print(response.json())
```

### Example 5: Generate Performance Summary

```python
import httpx

# Get combined summary
response = httpx.get("http://localhost:8002/api/get_summary?platform=both")

summary = response.json()["data"]
print(f"Total Posts: {summary['combined_metrics']['total_posts']}")
print(f"Total Engagement: {summary['combined_metrics']['total_engagement']}")
print(f"Facebook Avg Engagement: {summary['facebook']['average_engagement']}")
print(f"Instagram Avg Engagement: {summary['instagram']['average_engagement']}")
```

### Example 6: Using Python Integration Module Directly

```python
from facebook_instagram_integration import FacebookInstagramIntegration
import asyncio

async def main():
    integration = FacebookInstagramIntegration(mock_mode=False)
    
    # Post to both platforms
    result = await integration.post_to_both(
        message="🎯 Marketing campaign launched!",
        image_url="https://example.com/campaign.jpg"
    )
    
    print(f"Facebook Post ID: {result['facebook']['post_id']}")
    print(f"Instagram Post ID: {result['instagram']['post_id']}")
    
    # Generate summary
    summary = await integration.generate_combined_summary()
    print(f"Total Engagement: {summary['combined_metrics']['total_engagement']}")

asyncio.run(main())
```

---

## 🧪 Testing

### Run Full Test Suite

```bash
python test_facebook_instagram.py
```

### Test Individual Components

```bash
# Test the integration module directly
python facebook_instagram_integration.py
```

### Test MCP Server API

```bash
# Start server in one terminal
python social_mcp_server_v2.py

# In another terminal, test endpoints
curl http://localhost:8002/health
```

---

## 🔧 Troubleshooting

### Problem: "Module not found" Error

**Solution:**
```bash
# Install required dependencies
pip install fastapi uvicorn httpx python-dotenv pydantic aiofiles
```

---

### Problem: "Invalid Access Token"

**Solution:**
1. Verify token in Graph API Explorer
2. Ensure token hasn't expired (Page tokens can expire)
3. Regenerate token with correct permissions
4. Check token is in `.env` without quotes

---

### Problem: "Page Not Found"

**Solution:**
1. Verify `FACEBOOK_PAGE_ID` is correct (numeric ID, not username)
2. Ensure you're admin of the page
3. Check page is published (not draft)

---

### Problem: "Instagram Account Not Connected"

**Solution:**
1. Convert Instagram to Business Account (in Instagram app Settings)
2. Connect Instagram to Facebook Page (in Instagram app Settings → Account → Linked Accounts)
3. Verify Instagram Graph API is enabled in Facebook App

---

### Problem: "Rate Limit Exceeded"

**Solution:**
- Facebook API limits: 200 requests/hour per user
- Instagram API limits: 200 requests/hour per user
- Wait 15 minutes before retrying
- Implement exponential backoff in production

---

### Problem: Server Won't Start

**Solution:**
```bash
# Check if port is in use
netstat -ano | findstr :8002

# Kill the process or change port in social_mcp_server_v2.py
# Or set environment variable:
set SOCIAL_MCP_PORT=8005
```

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `facebook_instagram_integration.py` | Core integration module |
| `social_mcp_server_v2.py` | MCP Server with API endpoints |
| `test_facebook_instagram.py` | Comprehensive test suite |
| `FACEBOOK_INSTAGRAM_INTEGRATION.md` | This documentation |
| `.env` (updated) | Configuration with FB/IG variables |

---

## ✅ Verification Checklist

- [ ] Dependencies installed
- [ ] Facebook Developer App created
- [ ] Instagram Graph API enabled
- [ ] Page Access Token obtained
- [ ] Instagram Business Account ID obtained
- [ ] `.env` file configured
- [ ] Test suite passes in mock mode
- [ ] MCP server starts successfully
- [ ] API documentation accessible at `/docs`
- [ ] Can post to Facebook (mock or live)
- [ ] Can post to Instagram (mock or live)
- [ ] Can generate summaries

---

## 🎉 You're Ready!

Your Facebook & Instagram integration is complete and ready to use!

### Next Steps:

1. **Test in Mock Mode**: Run tests with `SOCIAL_MOCK_MODE=true`
2. **Configure Live Credentials**: Add real tokens and IDs to `.env`
3. **Switch to Live Mode**: Set `SOCIAL_MOCK_MODE=false`
4. **Start Posting**: Use the API to post and analyze content

### Quick Commands:

```bash
# Run tests
python test_facebook_instagram.py

# Start server
python social_mcp_server_v2.py

# View API docs
# Open: http://localhost:8002/docs
```

---

**📧 Support:** Check the troubleshooting section or review API error messages for specific issues.

**📚 Additional Resources:**
- Facebook Graph API Docs: https://developers.facebook.com/docs/graph-api
- Instagram Graph API Docs: https://developers.facebook.com/docs/instagram-api
- Graph API Explorer: https://developers.facebook.com/tools/explorer/
