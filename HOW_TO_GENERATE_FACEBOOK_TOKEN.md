# 📘 HOW TO GENERATE FACEBOOK PAGE ACCESS TOKEN

**Complete Step-by-Step Guide (2026)**

---

## ⏱️ Time Required: 5-10 minutes

---

## 📋 Prerequisites

1. **Facebook Developer Account** - https://developers.facebook.com/
2. **Facebook App** (created in your developer account)
3. **Facebook Page** that you admin

---

## 🚀 STEP-BY-STEP INSTRUCTIONS

### Step 1: Go to Graph API Explorer

**URL:** https://developers.facebook.com/tools/explorer/

![Step 1](https://developers.facebook.com/tools/explorer/)

---

### Step 2: Select Your App

1. Look for the **"Application"** dropdown at the top
2. Select your app from the list
3. If you don't have an app, click **"Add New App"**

![Step 2](Select your app from dropdown)

---

### Step 3: Click "Get Token"

1. Click the **"Get Token"** button (blue button)
2. Select **"Get Page Access Token"** from the menu

![Step 3](Get Token → Get Page Access Token)

---

### Step 4: Select Your Facebook Page

1. A popup will appear showing your Facebook Pages
2. Find and **select your page** (1496288429174042)
3. Click **"Next"** or **"Generate Token"**

![Step 4](Select your Facebook Page)

---

### Step 5: Grant Permissions

Facebook will ask for permissions. **Check these boxes:**

- ✅ **pages_manage_posts** - Required for posting
- ✅ **pages_read_engagement** - Required for analytics
- ✅ **pages_show_list** - Required to view pages

![Step 5](Check all required permissions)

**Click "Continue"** or **"Allow"**

---

### Step 6: Copy the Access Token

1. The token will appear in the **"Access Token"** field at the top
2. It will be a **long string** starting with `EAAV...`
3. Click the **copy icon** 📋 next to the token field

![Step 6](Copy the generated token)

**⚠️ IMPORTANT:** 
- Copy the **ENTIRE** token
- Don't miss any characters
- Token is **case-sensitive**

---

### Step 7: Paste in .env File

1. Open your project folder:
   ```
   C:\Users\ESHOP\Documents\AI Employee Vault [Gold]\.env
   ```

2. Find this line:
   ```
   FACEBOOK_PAGE_ACCESS_TOKEN=
   ```

3. **Paste your token** (NO quotes):
   ```
   FACEBOOK_PAGE_ACCESS_TOKEN=EAAVQ3cxNbRoBQ...rest_of_token
   ```

4. **Save the file** (Ctrl + S)

---

### Step 8: Verify Token

Open Command Prompt and run:

```bash
cd "C:\Users\ESHOP\Documents\AI Employee Vault [Gold]"
python test_facebook_token.py
```

**Expected output:**
```
✅ Token is VALID!
✅ All required permissions granted!
✅ Page access confirmed!
```

---

### Step 9: Post Live!

```bash
python post_facebook_live_now.py
```

---

## 🔍 TROUBLESHOOTING

### Problem: "No pages available"

**Solution:**
- Make sure you're an **admin** of the Facebook Page
- Page must be **published** (not in draft)

---

### Problem: "Missing permissions"

**Solution:**
- When generating token, make sure to check ALL required permissions
- If already generated, click "Get Token" again and re-select permissions

---

### Problem: "Token expired immediately"

**Solution:**
- Token generation takes time - use it within 1-2 hours
- For longer validity, get a **long-lived token** (see below)

---

### Problem: "App not found"

**Solution:**
1. Create a new app: https://developers.facebook.com/apps/
2. Choose **"Business"** as app type
3. Fill in app name and contact email
4. Complete app creation

---

## 🕐 TOKEN VALIDITY

| Token Type | Lifespan | How to Get |
|------------|----------|------------|
| **Short-Lived** | 1-2 hours | Graph API Explorer (this guide) |
| **Long-Lived** | 60 days | Exchange short-lived token |

---

## 🎯 GET LONG-LIVED TOKEN (60 Days)

After getting short-lived token:

### Option A: Use Our Script

```bash
python get_long_lived_token.py
```

You'll need:
- **App ID** (from Facebook App Dashboard)
- **App Secret** (from Facebook App Dashboard)

---

### Option B: Manual Method

1. **Get App ID and Secret:**
   - Go to: https://developers.facebook.com/apps/
   - Select your app
   - Go to **Settings → Basic**
   - Copy **App ID** and **App Secret**

2. **Visit this URL** (replace placeholders):
   ```
   https://graph.facebook.com/v19.0/oauth/access_token?
   grant_type=fb_exchange_token&
   client_id=YOUR_APP_ID&
   client_secret=YOUR_APP_SECRET&
   fb_exchange_token=YOUR_SHORT_TOKEN
   ```

3. **Copy the `access_token`** from response

4. **Update .env** with new token

---

## ✅ VERIFICATION CHECKLIST

After generating token:

- [ ] Token pasted in `.env` (no quotes)
- [ ] File saved
- [ ] `python test_facebook_token.py` shows ✅
- [ ] All permissions granted
- [ ] Page access confirmed
- [ ] Ready to post!

---

## 📸 VISUAL GUIDE

### Graph API Explorer Main Page
```
┌─────────────────────────────────────────────────────┐
│  Facebook Graph API Explorer                        │
├─────────────────────────────────────────────────────┤
│  Application: [Your App Name ▼]                     │
│  Access Token: [Get Token ▼] ← CLICK HERE           │
│                                                     │
│  GET /me?fields=id,name                             │
│  [Submit]                                           │
└─────────────────────────────────────────────────────┘
```

### Get Page Access Token
```
┌─────────────────────────────────────────────────────┐
│  Select Page                                        │
├─────────────────────────────────────────────────────┤
│  ☑ Your Page Name (1496288429174042)               │
│  ☐ Another Page                                     │
│                                                     │
│  Permissions:                                       │
│  ☑ pages_manage_posts                              │
│  ☑ pages_read_engagement                           │
│  ☑ pages_show_list                                 │
│                                                     │
│  [Continue]  [Cancel]                               │
└─────────────────────────────────────────────────────┘
```

### Generated Token
```
┌─────────────────────────────────────────────────────┐
│  Access Token:                                      │
│  EAAVQ3cxNbRoBQZB...[very long string]...KNG 📋    │
│                                                     │
│  Token type: Page Access Token                      │
│  Expires: In 1 hour                                 │
└─────────────────────────────────────────────────────┘
```

---

## 🆘 STILL NEED HELP?

### Quick Video Tutorial
Watch: https://www.youtube.com/results?search_query=facebook+page+access+token+2026

### Facebook Documentation
https://developers.facebook.com/docs/pages/access-tokens/

### Graph API Explorer
https://developers.facebook.com/tools/explorer/

---

## 🎉 SUCCESS!

Once you see ✅ from `test_facebook_token.py`, you're ready to post:

```bash
python post_facebook_live_now.py
```

---

**Good luck! 🚀**
