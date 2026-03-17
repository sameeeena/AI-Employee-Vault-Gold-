# 📘📷 Facebook & Instagram Integration - Quick Start

## 🎯 In a Hurry? Follow These Steps

---

## ⚡ Quick Setup (60 minutes)

### **1. Get Credentials** (30 min)
```
1. Go to: https://developers.facebook.com/
2. Create App → "Business" use case
3. Add Products: Marketing API + Instagram Graph API
4. Copy: App ID, App Secret
```

### **2. Get Page & Instagram IDs** (15 min)
```
1. Go to: https://developers.facebook.com/tools/explorer/
2. Get Token → Get Page Access Token
3. Query: me/accounts → Copy Page ID
4. Query: {page-id}?fields=instagram_business_account → Copy Instagram ID
```

### **3. Generate Access Token** (10 min)
```
1. In Graph API Explorer, select permissions:
   - pages_manage_posts
   - pages_read_engagement
   - instagram_basic
2. Generate Access Token
3. Copy the token (valid for 60 days)
```

### **4. Update Configuration** (5 min)
```bash
# Edit .env file - add these lines:
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_PAGE_ID=your_page_id
INSTAGRAM_ACCESS_TOKEN=your_access_token
INSTAGRAM_USER_ID=your_instagram_id
```

### **5. Start Server** (2 min)
```bash
python social_mcp_server.py
```

### **6. Test** (3 min)
```bash
# Post to Facebook
curl -X POST http://localhost:8001/post_message ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"facebook\", \"message\": \"Test post!\"}"
```

---

## 📋 Credential Checklist

You need these 6 values:

| Value | Where to Get | Example |
|-------|--------------|---------|
| `FACEBOOK_APP_ID` | Facebook App Dashboard | `123456789012345` |
| `FACEBOOK_APP_SECRET` | Facebook App Dashboard | `abc123def456...` |
| `FACEBOOK_ACCESS_TOKEN` | Graph API Explorer | `EAABsbCS1iHgBO...` |
| `FACEBOOK_PAGE_ID` | Graph API Explorer | `987654321098765` |
| `INSTAGRAM_ACCESS_TOKEN` | Same as Facebook token | `EAABsbCS1iHgBO...` |
| `INSTAGRAM_USER_ID` | Graph API Explorer | `17841400000000000` |

---

## 🚀 Quick Commands

### Start Server:
```bash
python social_mcp_server.py
```

### Post to Facebook:
```bash
curl -X POST http://localhost:8001/post_message ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"facebook\", \"message\": \"Hello World!\"}"
```

### Post to Instagram (with image):
```bash
curl -X POST http://localhost:8001/post_message ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"instagram\", \"message\": \"Beautiful day!\", \"image_url\": \"https://example.com/photo.jpg\"}"
```

### Get Summary:
```bash
curl -X POST http://localhost:8001/generate_post_summary ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"facebook\", \"post_id\": \"12345_67890\"}"
```

### Health Check:
```bash
curl http://localhost:8001/health
```

---

## 🔗 Quick Links

| Tool | URL |
|------|-----|
| Facebook Developers | https://developers.facebook.com/ |
| Graph API Explorer | https://developers.facebook.com/tools/explorer/ |
| Access Token Tool | https://developers.facebook.com/tools/access_token/ |
| Create Facebook Page | https://www.facebook.com/pages/create/ |

---

## 📖 Full Documentation

For detailed step-by-step instructions, see: **`SOCIAL_MEDIA_SETUP.md`**

---

**Quick Setup Time:** 60 minutes  
**Status:** Ready to implement
