# 📷 Instagram ID & Token - Quick Visual Guide
## Step-by-Step Screenshot-Style Instructions

---

## 🎯 **Goal:** Get Instagram Business ID in 5 Minutes

---

## **STEP 1: Convert Instagram to Business Account** ⏱️ 2 minutes

### On Your Phone:

```
Instagram App
    ↓
Profile (👤 icon)
    ↓
Menu (☰ three lines)
    ↓
Settings and privacy
    ↓
Account type and tools
    ↓
Switch to professional account
    ↓
Business ← Select this
    ↓
Choose Category (e.g., "Business & Utility Services")
    ↓
Done! ✅
```

---

## **STEP 2: Connect Instagram to Facebook Page** ⏱️ 2 minutes

### Option A: From Instagram App

```
Instagram App
    ↓
Profile → Settings
    ↓
Accounts Center
    ↓
Connected Accounts
    ↓
Add Facebook Account
    ↓
Login to Facebook
    ↓
Select Your Facebook Page
    ↓
Done! ✅
```

### Option B: From Facebook

```
Facebook.com
    ↓
Your Facebook Page
    ↓
Page Settings
    ↓
Linked Accounts
    ↓
Instagram
    ↓
Connect Account
    ↓
Login to Instagram
    ↓
Done! ✅
```

---

## **STEP 3: Open Graph API Explorer** ⏱️ 1 minute

### On Computer:

1. **Open Browser**

2. **Go to:**
   ```
   https://developers.facebook.com/tools/explorer/
   ```

3. **Select Your App:**
   - Click dropdown at top
   - Select: `1275203508084665`

---

## **STEP 4: Generate Access Token** ⏱️ 2 minutes

### In Graph API Explorer:

```
Click "Get Token"
    ↓
Click "Get Page Access Token"
    ↓
Select Your Facebook Page
    ↓
Check These Permissions:
   ✅ pages_manage_posts
   ✅ pages_read_engagement
   ✅ pages_show_list
   ✅ instagram_basic
   ✅ instagram_content_publish
    ↓
Click "Get Access Token"
    ↓
Allow Permissions
    ↓
Done! ✅
```

---

## **STEP 5: Get Facebook Page ID** ⏱️ 1 minute

### In Graph API Explorer:

**Query Box میں لکھیں:**
```
GET /me/accounts
```

**Click "Submit"**

**Response کچھ ایسا ہوگا:**
```json
{
  "data": [
    {
      "access_token": "EAASHynQdn7kBQ...",
      "id": "61585659193997",  ← 📋 Copy this ID
      "name": "Your Page Name"
    }
  ]
}
```

**✅ Copy کریں:** `61585659193997`

---

## **STEP 6: Get Instagram Business ID** ⏱️ 1 minute

### In Graph API Explorer:

**Query Box میں لکھیں:**
```
GET /61585659193997?fields=instagram_business_account
```

(اپنا Page ID use کریں)

**Click "Submit"**

**Response کچھ ایسا ہوگا:**
```json
{
  "instagram_business_account": {
    "id": "17841405822304915"  ← 📋 Copy this ID!
  }
}
```

**✅ یہ ہے آپ کا Instagram Business ID!**

**✅ Copy کریں:** `17841405822304915`

---

## **STEP 7: Update .env File** ⏱️ 1 minute

### Open `.env` file:

**Add these lines:**
```env
# Instagram Configuration
INSTAGRAM_USER_ID=17841405822304915  ← Your ID from Step 6
INSTAGRAM_ACCESS_TOKEN=EAASHynQdn7kBQ...  ← Same as Facebook token

# Change this to false
SOCIAL_MOCK_MODE=false
```

---

## **STEP 8: Test!** ⏱️ 1 minute

### Run this command:

```bash
python instagram_autopost_now.py --template 1
```

### Expected Output:

```
================================================================================
  📷 INSTAGRAM AUTO-POST
================================================================================

✅ LIVE MODE - posts will be published to Instagram

📝 Template: 🎉 Product Announcement (Post)

📄 Message Preview:
--------------------------------------------------------------------------------
🎉 Exciting News from AI Employee Vault!
...

⏳ Posting to Instagram...

================================================================================
  ✅ INSTAGRAM POST SUCCESSFUL!
================================================================================
  📍 Post ID: 17841405822304915_1234567890
  ⏰ Posted at: 2026-03-11T04:30:00
================================================================================
```

---

## 🎯 **Quick Summary**

| Step | Time | What to Do |
|------|------|------------|
| 1 | 2 min | Convert Instagram to Business |
| 2 | 2 min | Connect to Facebook Page |
| 3 | 1 min | Open Graph API Explorer |
| 4 | 2 min | Generate Access Token |
| 5 | 1 min | Get Facebook Page ID |
| 6 | 1 min | Get Instagram Business ID |
| 7 | 1 min | Update .env file |
| 8 | 1 min | Test |

**Total Time:** ~11 minutes

---

## 🔧 **Helper Script**

Instead of manual steps, run:

```bash
python get_instagram_id.py
```

This script will:
- Open Graph API Explorer for you
- Guide you through each step
- Help you copy the right IDs

---

## ⚠️ **Common Issues**

### "Instagram Business Account not found"

**Fix:**
1. Make sure Instagram is Business Account (Step 1)
2. Make sure Instagram is connected to Facebook (Step 2)
3. Wait 5 minutes and try again

---

### "Empty response" or "No instagram_business_account"

**Fix:**
1. Disconnect Instagram from Facebook
2. Reconnect
3. Refresh Graph API Explorer
4. Try again

---

### "Permissions error"

**Fix:**

Make sure you have these permissions:
- ✅ `pages_manage_posts`
- ✅ `pages_read_engagement`
- ✅ `instagram_basic`
- ✅ `instagram_content_publish`

---

## ✅ **Checklist**

- [ ] Instagram Business Account بنایا
- [ ] Facebook Page سے connect کیا
- [ ] Graph API Explorer کھولا
- [ ] Access Token generate کیا
- [ ] Facebook Page ID copy کیا
- [ ] Instagram Business ID copy کیا
- [ ] .env file update کی
- [ ] `SOCIAL_MOCK_MODE=false` کیا
- [ ] Test کیا

---

## 📞 **Need Help?**

**Full Guide:** `INSTAGRAM_ID_TOKEN_GUIDE.md`

**Graph API Explorer:** https://developers.facebook.com/tools/explorer/

**Instagram Docs:** https://developers.facebook.com/docs/instagram-api

---

**Created:** 2026-03-11  
**Status:** ✅ Complete Visual Guide
