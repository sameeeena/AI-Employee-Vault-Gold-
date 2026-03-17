# 🔑 Facebook Page Access Token Setup Guide

**Issue:** Your current Facebook Page Access Token is not returning any pages.

---

## ❌ Current Status

- **Token Present:** ✅ Yes
- **Pages Returned:** ❌ None (empty list)
- **Page ID:** 61585659193997

This means the token is either:
1. **Expired** (tokens typically last 60 days)
2. **Missing permissions** (needs `pages_manage_posts`, `pages_read_engagement`)
3. **Wrong token type** (needs to be a Page Access Token, not User Access Token)

---

## ✅ How to Get a Valid Facebook Page Access Token

### Method 1: Facebook Graph API Explorer (Quick - 1 Hour Token)

1. **Go to Graph API Explorer**
   - Visit: https://developers.facebook.com/tools/explorer/

2. **Select Your App**
   - Choose your app: `1275203508084665`

3. **Get User Token**
   - Click "Get Token" → "Get User Access Token"
   - Select permissions:
     - ✅ `pages_manage_posts`
     - ✅ `pages_read_engagement`
     - ✅ `pages_show_list`
   - Click "Generate Access Token"

4. **Get Page Token**
   - In the query box, enter: `me/accounts`
   - Click "Submit"
   - Find your page in the results
   - Copy the `access_token` value (this is your Page Access Token)

5. **Update .env**
   ```
   FACEBOOK_PAGE_ACCESS_TOKEN=YOUR_NEW_TOKEN_HERE
   FACEBOOK_PAGE_ID=YOUR_PAGE_ID_HERE
   ```

---

### Method 2: Facebook Business Manager (Long-lived Token)

1. **Go to Business Settings**
   - Visit: https://business.facebook.com/settings

2. **Select Your Business**
   - Choose your business account

3. **Go to Pages**
   - Navigate to: Accounts → Pages

4. **Add/Select Page**
   - Select your page or add it if not listed

5. **Generate Token**
   - Go to: https://developers.facebook.com/tools/accesstoken/
   - Select "Page Access Token"
   - Choose your page
   - Copy the token

---

### Method 3: Use the Included Script

Run the included script to find your Page ID:

```bash
python find_facebook_page_id.py
```

This will:
1. Fetch all pages you manage
2. Display their IDs and names
3. Optionally update your `.env` file

---

## 🔍 Verify Your Token

After updating `.env`, run:

```bash
python debug_facebook.py
```

**Expected output:**
```
Status: 200
Response: {"data":[{"name":"Your Page Name","id":"1234567890","access_token":"..."}]}
```

---

## 📋 Required Permissions

Your token MUST have these permissions:

| Permission | Purpose |
|------------|---------|
| `pages_manage_posts` | Create and publish posts |
| `pages_read_engagement` | Read post metrics |
| `pages_show_list` | List pages you manage |

---

## 🎯 Quick Fix Steps

1. **Get new token** (Method 1 above - fastest)
2. **Update `.env`**:
   ```
   FACEBOOK_PAGE_ACCESS_TOKEN=new_token_here
   FACEBOOK_PAGE_ID=page_id_from_step_1
   ```
3. **Test connection**:
   ```bash
   python test_facebook_connection.py
   ```
4. **If successful, run auto-post**:
   ```bash
   python autopost_facebook.py
   ```

---

## 📞 Troubleshooting

### "No pages found"
- Token doesn't have `pages_show_list` permission
- You're not an admin of any Facebook Page

### "Token expired"
- Generate a new token (tokens last ~60 days)
- Consider using a long-lived token (Method 2)

### "Invalid permissions"
- Make sure app has been reviewed by Facebook
- Add permissions in App Review

### "Page ID mismatch"
- Use the token's page ID from `me/accounts` response
- Don't manually guess the Page ID

---

## 🔗 Helpful Links

- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **Access Token Tool:** https://developers.facebook.com/tools/accesstoken/
- **Graph API Docs:** https://developers.facebook.com/docs/graph-api
- **Page Token Guide:** https://developers.facebook.com/docs/facebook-login/guides/access-tokens/page-access-tokens

---

**Once you have a valid token, run `facebook_autopost.bat` to start posting!**
