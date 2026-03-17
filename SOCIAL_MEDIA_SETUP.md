# 📘📷 Facebook & Instagram Integration - Step by Step Guide

## 🎯 Task: "Integrate Facebook and Instagram and post messages and generate summary"

---

## 📋 Implementation Overview

```
┌─────────────────────────────────────────────────────────────────┐
│         FACEBOOK & INSTAGRAM INTEGRATION FLOW                    │
└─────────────────────────────────────────────────────────────────┘

Step 1: Get Facebook Developer Credentials
        ↓
Step 2: Configure Facebook Page & Instagram Business
        ↓
Step 3: Generate Access Tokens
        ↓
Step 4: Update .env Configuration
        ↓
Step 5: Start Social MCP Server
        ↓
Step 6: Test Posting Messages
        ↓
Step 7: Generate Engagement Summaries
```

---

## 🔧 STEP 1: Get Facebook Developer Credentials (30 minutes)

### 1.1 Create Facebook Developer Account

1. **Go to**: https://developers.facebook.com/
2. **Click**: "Get Started" or "Log In"
3. **Sign in** with your Facebook account
4. **Complete** developer verification (may require phone verification)

### 1.2 Create a New App

1. **Go to**: https://developers.facebook.com/apps/
2. **Click**: "Create App" button
3. **Select use case**: 
   - Choose **"Business"** (recommended for business pages)
   - OR **"Other"** → "Business Integrations"
4. **Fill in app details**:
   - **App Name**: `AI Employee Social Media`
   - **App Contact Email**: `sameena02134@gmail.com`
   - Click **"Create App"**
5. **Complete security check** (enter password)

### 1.3 Configure App Settings

1. **In App Dashboard**, find **"App Review"** in left menu
2. **Toggle** "Set to Public" (turn ON)
3. **Add Products** to your app:
   - Click **"Add Products"**
   - Find and add:
     - ✅ **Marketing API**
     - ✅ **Instagram Graph API**
     - ✅ **Facebook Login**

### 1.4 Get App Credentials

1. **Go to**: Settings → Basic in left menu
2. **Copy these values**:
   ```
   App ID: [Your App ID - 15 digit number]
   App Secret: [Your App Secret - long string]
   ```

**Save these!** You'll need them for the next steps.

---

## 📘 STEP 2: Configure Facebook Page (15 minutes)

### 2.1 Requirements

You need:
- A **Facebook Business Page** (not personal profile)
- **Admin access** to the page

### 2.2 Create Facebook Page (if you don't have one)

1. **Go to**: https://www.facebook.com/pages/create/
2. **Fill in**:
   - **Page Name**: Your business name
   - **Category**: Choose appropriate category
   - **Description**: Brief description
3. **Click**: "Create Page"
4. **Add profile picture** and **cover photo** (optional but recommended)

### 2.3 Get Your Page ID

**Method 1: From Page Settings**
1. Go to your Facebook Page
2. Click **"About"** in left menu
3. Scroll down to find **"Page ID"** (15-16 digit number)

**Method 2: From URL**
- Your page URL: `https://www.facebook.com/your-page-name-123456789/`
- The numbers at the end = Page ID

**Method 3: Using Graph API Explorer**
1. Go to: https://developers.facebook.com/tools/explorer/
2. Select your app from dropdown
3. Click **"Get Token"** → **"Get Page Access Token"**
4. Select your page
5. Query: `me/accounts`
6. Find your page in results → copy `"id"` field

---

## 📷 STEP 3: Configure Instagram Business Account (20 minutes)

### 3.1 Requirements

You need:
- **Instagram Business** or **Creator** account (not personal)
- Instagram account **connected to Facebook Page**

### 3.2 Convert to Business Account

1. **Open Instagram app** on mobile
2. **Go to**: Profile → Menu (☰) → Settings
3. **Tap**: Account type and tools
4. **Tap**: "Switch to professional account"
5. **Select**: "Business" (or Creator)
6. **Choose category**: e.g., "Business & Utility Services"
7. **Complete** the setup

### 3.3 Connect Instagram to Facebook Page

1. **In Instagram app**: Profile → Menu (☰) → Settings
2. **Tap**: Account → Linked accounts
3. **Tap**: Facebook
4. **Log in** to Facebook if prompted
5. **Select** your business page
6. **Confirm** the connection

### 3.4 Get Instagram User ID

**Method 1: Using Graph API Explorer** (Recommended)

1. **Go to**: https://developers.facebook.com/tools/explorer/
2. **Select your app** from dropdown
3. **Click "Get Token"** → Select permissions:
   - `instagram_basic`
   - `pages_show_list`
   - `pages_read_engagement`
   - `instagram_manage_insights`
   - `pages_manage_posts`
4. **Click "Generate Access Token"**
5. **Login and authorize** if prompted
6. **In the query box**, enter:
   ```
   me/accounts
   ```
7. **Click "Submit"**
8. **Find your page** in results and copy:
   - `"id"` → This is your **Facebook Page ID**
   - `"access_token"` → This is your **Page Access Token**

9. **Now query Instagram account**:
   ```
   {page-id}?fields=instagram_business_account
   ```
   (Replace `{page-id}` with your actual Page ID)

10. **Copy the Instagram ID** from the response:
    ```json
    {
      "instagram_business_account": {
        "id": "17841400000000000"  ← This is your Instagram User ID
      }
    }
    ```

---

## 🔑 STEP 4: Generate Long-Lived Access Tokens (10 minutes)

### 4.1 Get Page Access Token (Facebook)

1. **Go to**: https://developers.facebook.com/tools/explorer/
2. **Select your app**
3. **Click "Get Token"** → **"Get Page Access Token"**
4. **Select your page**
5. **Copy the access token**

### 4.2 Exchange for Long-Lived Token

**Facebook tokens expire in 1-2 hours by default. You need a long-lived token (60 days).**

1. **Go to**: https://developers.facebook.com/tools/access_token/
2. **Paste your short-lived token** in "Debug Token" tool
3. **Click "Debug"** to verify
4. **Use this URL** in browser (replace YOUR_SHORT_LIVED_TOKEN):
   ```
   https://graph.facebook.com/oauth/access_token?
     grant_type=fb_exchange_token&
     client_id={app-id}&
     client_secret={app-secret}&
     fb_exchange_token={YOUR_SHORT_LIVED_TOKEN}
   ```
5. **Copy the long-lived token** from response

**Alternative: Use Graph API Explorer**
- Select permissions: `pages_manage_posts`, `pages_read_engagement`
- Generate token
- Token will be valid for 60 days if app is live

### 4.3 Instagram Access Token

Instagram uses the **same token** as Facebook Page (since it's connected).

Use the **same long-lived token** you generated for Facebook.

---

## ⚙️ STEP 5: Update Configuration Files (5 minutes)

### 5.1 Update `.env` File

Open `.env` and add these lines at the end:

```env
# ===========================================
# SOCIAL MEDIA (Facebook & Instagram)
# ===========================================
# Facebook App Credentials
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here

# Facebook Page Access Token (long-lived, 60 days)
FACEBOOK_ACCESS_TOKEN=your_page_access_token_here

# Facebook Page ID (from Step 2)
FACEBOOK_PAGE_ID=your_page_id_here

# Instagram Access Token (same as Facebook)
INSTAGRAM_ACCESS_TOKEN=your_page_access_token_here

# Instagram User ID (from Step 3)
INSTAGRAM_USER_ID=your_instagram_user_id_here

# Twitter (Optional - for future)
TWITTER_BEARER_TOKEN=
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
```

### 5.2 Update `mcp_config/mcp_server_config.json`

```json
{
  "server_name": "Silver AI Employee MCP Server",
  "version": "1.0.0",
  "tools": [
    "send_email",
    "log_activity",
    "create_task",
    "get_system_status",
    "post_to_facebook",
    "post_to_instagram",
    "get_engagement_metrics",
    "generate_social_summary"
  ],
  "smtp": {
    "server": "smtp.gmail.com",
    "port": 587,
    "use_tls": true
  },
  "social": {
    "facebook_enabled": true,
    "instagram_enabled": true,
    "twitter_enabled": false
  }
}
```

---

## 🚀 STEP 6: Start Social MCP Server (2 minutes)

### 6.1 Install Dependencies (if needed)

```bash
pip install fastapi uvicorn httpx pydantic aiofiles python-dotenv
```

### 6.2 Start the Server

```bash
# Start Social MCP Server
python social_mcp_server.py
```

Server will start on: `http://localhost:8001`

### 6.3 Verify Server is Running

```bash
# Test health endpoint
curl http://localhost:8001/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-03-04T...",
  "platforms": ["facebook", "instagram", "twitter"]
}
```

---

## 📝 STEP 7: Test Posting Messages (5 minutes)

### 7.1 Post to Facebook

```bash
curl -X POST http://localhost:8001/post_message ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"facebook\", \"message\": \"Hello from AI Employee! This is my first automated post. 🤖\"}"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "post_id": "123456789_987654321",
    "platform": "facebook"
  }
}
```

### 7.2 Post to Instagram (with image)

```bash
curl -X POST http://localhost:8001/post_message ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"instagram\", \"message\": \"Beautiful day! ☀️ #AI #Automation\", \"image_url\": \"https://example.com/image.jpg\"}"
```

**Note:** Instagram requires an image URL. The image must be publicly accessible.

### 7.3 Post with Link (Facebook)

```bash
curl -X POST http://localhost:8001/post_message ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"facebook\", \"message\": \"Check out our latest update!\", \"link\": \"https://yourwebsite.com/blog\"}"
```

---

## 📊 STEP 8: Generate Engagement Summary (3 minutes)

### 8.1 Get Engagement Metrics

After posting, wait a few minutes for engagement, then:

```bash
curl -X POST http://localhost:8001/fetch_engagement_metrics ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"facebook\", \"post_id\": \"123456789_987654321\"}"
```

### 8.2 Generate Post Summary

```bash
curl -X POST http://localhost:8001/generate_post_summary ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"facebook\", \"post_id\": \"123456789_987654321\"}"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "platform": "facebook",
    "post_id": "123456789_987654321",
    "timestamp": "2026-03-04T...",
    "reactions": 15,
    "comments": 3,
    "shares": 2,
    "impressions": 250
  }
}
```

---

## 🛠️ Create Command Files (Optional but Recommended)

### Create `social.bat`

```batch
@echo off
REM ===========================================
REM Social Media MCP Server Command
REM ===========================================
REM Usage: social [start|stop|status|test]
REM ===========================================

if "%1"=="start" (
    echo Starting Social MCP Server...
    echo Platforms: Facebook, Instagram
    python social_mcp_server.py
    goto :end
)

if "%1"=="test" (
    echo Testing Social MCP Server...
    echo.
    echo 1. Health Check...
    curl http://localhost:8001/health
    echo.
    echo.
    echo 2. Test Facebook Post...
    echo curl -X POST http://localhost:8001/post_message -H "Content-Type: application/json" -d "{\"platform\": \"facebook\", \"message\": \"Test post\"}"
    goto :end
)

if "%1"=="status" (
    echo Checking Social MCP Server status...
    curl http://localhost:8001/health
    goto :end
)

echo.
echo ===========================================
echo   SOCIAL MEDIA MCP SERVER
echo ===========================================
echo.
echo Usage: social [command]
echo.
echo Commands:
echo   start   - Start the Social MCP Server
echo   test    - Test API endpoints
echo   status  - Check server health
echo.
echo ===========================================

:end
```

---

## ✅ Verification Checklist

Before you start, make sure you have:

- [ ] Facebook Developer account created
- [ ] Facebook App created and set to Public
- [ ] Marketing API & Instagram Graph API added to app
- [ ] Facebook Business Page created
- [ ] Instagram Business account created
- [ ] Instagram connected to Facebook Page
- [ ] App ID and App Secret copied
- [ ] Page ID copied
- [ ] Instagram User ID copied
- [ ] Long-lived access token generated
- [ ] `.env` file updated with all credentials
- [ ] Dependencies installed
- [ ] Social MCP Server starts without errors
- [ ] Test post to Facebook successful
- [ ] Test post to Instagram successful
- [ ] Engagement metrics retrieval working
- [ ] Summary generation working

---

## 🔐 Required Permissions

Make sure your access token has these permissions:

### Facebook:
- `pages_manage_posts` - Create posts
- `pages_read_engagement` - Read metrics
- `pages_show_list` - List pages

### Instagram:
- `instagram_basic` - Basic profile info
- `instagram_manage_insights` - Analytics
- `pages_show_list` - Connected pages

---

## 📚 API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Server health check |
| `/post_message` | POST | Post to Facebook/Instagram |
| `/fetch_engagement_metrics` | POST | Get likes, comments, shares |
| `/generate_post_summary` | POST | Generate structured summary |

---

## 🐛 Troubleshooting

### "Invalid access token"
- Token expired → Generate new long-lived token
- Wrong token format → Ensure no extra spaces
- Token doesn't have required permissions → Re-authorize

### "Page not found"
- Check Page ID is correct
- Ensure you're admin of the page
- Verify token has page permissions

### "Instagram account not connected"
- Convert to Business account first
- Link Instagram to Facebook Page in settings
- Wait 5-10 minutes after linking

### "Rate limit exceeded"
- Facebook: 200 requests/hour per token
- Instagram: 200 requests/hour per token
- Wait and retry later

---

## 📖 Additional Resources

- **Facebook Graph API Docs**: https://developers.facebook.com/docs/graph-api
- **Instagram Graph API**: https://developers.facebook.com/docs/instagram-api
- **Access Token Tool**: https://developers.facebook.com/tools/access_token/
- **Graph API Explorer**: https://developers.facebook.com/tools/explorer/

---

**Estimated Total Time:** 90 minutes  
**Difficulty:** Medium  
**Status:** Ready to implement
