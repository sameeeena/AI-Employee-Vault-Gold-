# 📘 COMPLETE FACEBOOK DEVELOPER SETUP GUIDE (2026)

## Follow these steps EXACTLY in order.

---

## 🔹 PART 1: Register as Facebook Developer

### Step 1.1: Go to Facebook Developers
- **URL**: https://developers.facebook.com/
- Click **"Get Started"** or **"Log In"** (top right)
- Log in with your Facebook account

### Step 1.2: Complete Developer Registration
After logging in, you'll see a **registration form**:

1. **Country**: Select your country
2. **Accept Terms**: Check the box to accept Facebook Platform Terms
3. Click **"Complete Registration"** or **"Confirm"**

### Step 1.3: Verify Your Account (if asked)
Facebook may ask you to:
- **Add a phone number** → Enter and verify with SMS code
- **Confirm email** → Check your email for verification link

---

## 🔹 PART 2: Create Your Facebook Business Page

### Step 2.1: Go to Facebook Business
- **URL**: https://business.facebook.com/
- Click **"Create Account"** or **"Get Started"**

### Step 2.2: Fill Business Info
1. **Business Name**: Your business name (or "AI Employee Vault")
2. **Your Name**: Your full name
3. **Work Email**: Your email address
4. Click **"Submit"**

### Step 2.3: Create a Facebook Page (if you don't have one)
1. Go to: https://www.facebook.com/pages/create/
2. Fill in:
   - **Page Name**: Your business name
   - **Category**: Select "Business" or "Technology"
   - **Description**: Brief description
3. Click **"Create Page"**
4. **COPY YOUR PAGE ID** from the URL or About section

---

## 🔹 PART 3: Create Facebook App

### Step 3.1: Go to Apps Dashboard
- **URL**: https://developers.facebook.com/apps/
- Click **"Create App"** (top right, blue button)

### Step 3.2: Select App Type
You'll see options. Select:
- **"Business"** → Click **"Next"**

### Step 3.3: Fill App Details
1. **App Name**: `AI Employee Vault`
2. **App Contact Email**: Your email
3. **Business Account**: Select your business (if you created one)
4. Click **"Create App"**

### Step 3.4: Complete Setup Wizard
Facebook may show a setup wizard. You can:
- Click **"Skip"** for now (we'll configure manually)

---

## 🔹 PART 4: Add Required Products

### Step 4.1: Add Facebook Login
1. On your App Dashboard, scroll to **"Add Products"**
2. Find **"Facebook Login for Business"**
3. Click **"Set Up"**

### Step 4.2: Configure Facebook Login
1. In left sidebar, click **"Facebook Login"** → **"Settings"**
2. **Valid OAuth Redirect URIs**: Leave blank for now
3. Click **"Save Changes"**

### Step 4.3: Add Instagram Basic Display (for Instagram posting)
1. In left sidebar, scroll to **"Add Products"**
2. Find **"Instagram Basic Display"**
3. Click **"Set Up"**

---

## 🔹 PART 5: Get Your Access Token

### Step 5.1: Open Graph API Explorer
- **URL**: https://developers.facebook.com/tools/explorer/

### Step 5.2: Select Your App
- At the top, click the **dropdown** that says "Meta App" or shows an app name
- Select **"AI Employee Vault"** (your new app)

### Step 5.3: Generate Access Token
1. Click **"Generate Access Token"** button (or "Get User Access Token")
2. A **popup window** appears

### Step 5.4: Select Permissions
In the popup, you'll see a **list of permissions** (may be scrollable):

**Find and CHECK these 5 permissions:**

| Permission | What it does |
|------------|--------------|
| ✅ `pages_manage_posts` | Create posts on your Page |
| ✅ `pages_read_engagement` | See likes, comments, shares |
| ✅ `pages_show_list` | See list of pages you manage |
| ✅ `instagram_basic` | Access Instagram profile info |
| ✅ `instagram_content_publish` | Post to Instagram |

**How to find them:**
- Scroll through the list
- Or look for tabs like "Facebook Pages" and "Instagram"
- **CHECK THE BOX** next to each permission

### Step 5.5: Generate Token
1. After checking all 5 boxes, click **"Continue"** or **"Generate Token"**
2. Facebook opens **another popup**:
   - **Select your Facebook Page** from the list
   - Click **"Done"** or **"OK"**
3. Back in Graph API Explorer, you'll see a **long string** in the "Access Token" box
4. **COPY THIS TOKEN** (it starts with `EAAC` or `EAASH`)

---

## 🔹 PART 6: Get Your Page ID

### Method 1: From Facebook Page
1. Go to your Facebook Page
2. Look at the **URL** in browser
3. The number is your Page ID (e.g., `61585659193997`)

### Method 2: From Graph API Explorer
1. In Graph API Explorer, type: `/me/accounts`
2. Click **"Submit"**
3. Look for your page in results
4. Copy the **"id"** value

---

## 🔹 PART 7: Update Your .env File

### Open your `.env` file and update these lines:

```env
# Facebook Page Access Token (the long token you just copied)
FACEBOOK_PAGE_ACCESS_TOKEN=EAAC...<paste your full token here>

# Your Facebook Page ID (numeric)
FACEBOOK_PAGE_ID=61585659193997

# Your App ID (from App Dashboard)
FACEBOOK_APP_ID=<your new app id>

# Turn off mock mode to post live
SOCIAL_MOCK_MODE=false
```

---

## 🔹 PART 8: Test Your Setup

### Run the test script:
```
python check_facebook_permissions.py
```

### Expected output:
```
✅ Granted permissions:
   ✅ pages_manage_posts
   ✅ pages_read_engagement
   ✅ pages_show_list
   ✅ instagram_basic
   ✅ instagram_content_publish

🎉 All required permissions are granted!
```

---

## 🔹 PART 9: Test Auto-Posting

### Run the auto-post script:
```
python autopost_facebook.py
```

If successful, you'll see:
```
✅ POST SUCCESSFUL!
📍 Post ID: <id>
🔗 View: <url>
```

---

## ❓ Common Issues

| Problem | Solution |
|---------|----------|
| Can't find permissions in popup | Scroll down in the popup list |
| Token expires quickly | Make sure you selected your Page |
| "App not approved" error | Stay in Development mode for testing |
| Page not showing in list | Make sure you're Page Admin |

---

## 📞 Need Help?

Tell me:
- **Which STEP number** are you on?
- **What do you see** on your screen?
- **Any error message**?

I'll guide you through!
