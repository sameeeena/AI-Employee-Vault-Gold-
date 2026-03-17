# 🔧 FIX: pages_manage_posts Permission Missing

## ❌ Problem
The `pages_manage_posts` permission is not showing in the permissions list.

---

## ✅ SOLUTIONS

### Solution 1: Enable App Review (Most Common Fix)

1. **Go to App Dashboard:**
   https://developers.facebook.com/apps/

2. **Select your app**

3. **Go to App Review → Settings:**
   https://developers.facebook.com/apps/YOUR_APP_ID/app-review/

4. **Toggle "Make [App Name] public?"** to **YES**

5. **Save changes**

6. **Go back to Graph API Explorer** and try again

---

### Solution 2: Add Instagram Graph API Product

Sometimes adding the product enables the permissions:

1. **In App Dashboard**, click **"Add Product"**

2. **Find "Instagram Graph API"** and click **"Set Up"**

3. **Accept terms**

4. **Go back to Graph API Explorer** and try again

---

### Solution 3: Use Page Access Token Directly (Workaround)

If permissions still don't show, use this workaround:

1. **Go to Facebook Page:**
   https://www.facebook.com/YOUR_PAGE_ID

2. **Go to Page Settings → Page Access Token**

3. **Click "Generate Token"** or "Get Token"

4. **Copy the token**

This token already has posting permissions by default!

---

### Solution 4: Use Meta Business Suite

1. **Go to Meta Business Suite:**
   https://business.facebook.com/

2. **Select your Page**

3. **Go to Settings → Developers**

4. **Generate Access Token**

This token will have all permissions for your page.

---

### Solution 5: Check Page Admin Role

Make sure you're an **Admin** of the page:

1. **Go to your Facebook Page**

2. **Click Settings → Page Access**

3. **Check if you have "Full Control" or "Admin" role**

4. If not, ask an admin to grant you access

---

## 🎯 ALTERNATIVE: Direct Page Token (Easiest!)

### Get Token Directly from Your Page:

1. **Visit this URL** (replace PAGE_ID with your actual page ID):
   ```
   https://www.facebook.com/1496288429174042/settings/?tab=page_access
   ```

2. **Click "Page Access Token" or "Generate Token"**

3. **Copy the token** - it already has posting permissions!

4. **Paste in .env:**
   ```
   FACEBOOK_PAGE_ACCESS_TOKEN=YOUR_TOKEN_HERE
   ```

---

## 🧪 Test After Getting Token

```bash
python test_facebook_token.py
```

---

## 📞 Still Not Working?

### Check App Status:

1. Go to: https://developers.facebook.com/apps/
2. Select your app
3. Check if app status is **"Live"** (not "In Development")
4. If "In Development", toggle to "Live"

### Check App Permissions:

1. Go to: https://developers.facebook.com/tools/explorer/permissions/
2. Select your app
3. Look for "Pages" section
4. Ensure `pages_manage_posts` is available

---

## ✅ Quick Fix Summary

**Try in this order:**

1. ✅ **Make app Live** (App Dashboard → Settings → Toggle to Live)
2. ✅ **Add Instagram Graph API product** (App Dashboard → Add Product)
3. ✅ **Get token directly from Page Settings** (Easiest!)
4. ✅ **Use Meta Business Suite** (business.facebook.com)

---

**After trying any solution, run:**
```bash
python test_facebook_token.py
```

**Then post live:**
```bash
python post_facebook_live_now.py
```
