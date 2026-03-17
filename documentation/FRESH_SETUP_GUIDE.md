# 📘 Fresh Facebook Setup Guide

## Quick Steps - Do These IN ORDER:

---

### ✅ STEP 1: Log in to Facebook
- **Tab 1** is already open: https://www.facebook.com/
- Log in with your **NEW Facebook account**
- Make sure this account is **ADMIN** of your Facebook Page

---

### ✅ STEP 2: Create New App
- **Tab 2** is already open: https://developers.facebook.com/apps/
- Click **"Create App"** (top right, blue button)
- Select **"Business"** → Click **"Next"**
- Fill in:
  - **App Name**: `AI Employee Vault`
  - **Contact Email**: Your email
- Click **"Create App"**
- **COPY YOUR NEW APP ID** (shown on dashboard)

---

### ✅ STEP 3: Add Facebook Login
- On your App Dashboard, scroll to **"Add Products"**
- Find **"Facebook Login for Business"**
- Click **"Set Up"**

---

### ✅ STEP 4: Get Access Token
- **Tab 3** is already open: https://developers.facebook.com/tools/explorer/
- Select your **NEW APP** from the dropdown (top of page)
- Click **"Generate Access Token"**
- **In the popup, check these 5 boxes:**
  - ✅ `pages_manage_posts`
  - ✅ `pages_read_engagement`
  - ✅ `pages_show_list`
  - ✅ `instagram_basic`
  - ✅ `instagram_content_publish`
- Click **"Continue"**
- Facebook opens another window → **Select your Page** → Click **"Done"**
- **COPY THE TOKEN** that appears in Graph API Explorer

---

### ✅ STEP 5: Get Page ID
- In Graph API Explorer, type: `/me/accounts`
- Click **"Submit"**
- Find your page in results → Copy the **"id"** value

---

### ✅ STEP 6: Update .env File

Open your `.env` file and replace these lines:

```
FACEBOOK_PAGE_ACCESS_TOKEN=<paste your NEW token here>
FACEBOOK_PAGE_ID=<paste your Page ID here>
FACEBOOK_APP_ID=<paste your NEW App ID here>
SOCIAL_MOCK_MODE=false
```

---

### ✅ STEP 7: Test
Run this command:
```
python check_facebook_permissions.py
```

If it shows all permissions ✅, you're done!

---

## 📞 Need Help?

Tell me:
- Which step are you on?
- What do you see?
- Any error message?
