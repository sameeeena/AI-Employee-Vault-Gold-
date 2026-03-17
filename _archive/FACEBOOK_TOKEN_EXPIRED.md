# 🔴 FACEBOOK TOKEN EXPIRED - ACTION REQUIRED

## Issue

Your Facebook Page Access Token has expired on **March 8, 2026**.

**Error Message:**
```
Error validating access token: Session has expired on Sunday, 08-Mar-26 18:00:00 PDT.
```

---

## ✅ Solution: Generate New Facebook Page Access Token

### Option 1: Quick Method (Graph API Explorer)

1. **Go to Graph API Explorer:**
   https://developers.facebook.com/tools/explorer/

2. **Select Your App:**
   - Choose your app from the dropdown (or create one if you don't have)

3. **Get Token:**
   - Click **"Get Token"** → **"Get Page Access Token"**
   - Select your Facebook Page: `1496288429174042`

4. **Add Permissions:**
   Make sure these permissions are checked:
   - ✅ `pages_manage_posts`
   - ✅ `pages_read_engagement`
   - ✅ `pages_show_list`

5. **Copy the Token:**
   - Click **"Get Access Token"**
   - Copy the generated token (starts with `EAAV...`)

6. **Update .env File:**
   Open `.env` and replace the old token:
   ```bash
   FACEBOOK_PAGE_ACCESS_TOKEN=YOUR_NEW_TOKEN_HERE
   ```

7. **Test:**
   ```bash
   python post_facebook_live_now.py
   ```

---

### Option 2: Long-Lived Token (Recommended for Production)

For a token that lasts 60 days instead of a few hours:

1. **Get Short-Lived Token** (follow Option 1 above)

2. **Exchange for Long-Lived Token:**
   
   Run this Python script:
   ```python
   import httpx
   
   short_token = "YOUR_SHORT_TOKEN_HERE"
   
   response = httpx.get(
       "https://graph.facebook.com/v19.0/oauth/access_token",
       params={
           'grant_type': 'fb_exchange_token',
           'client_id': 'YOUR_APP_ID',
           'client_secret': 'YOUR_APP_SECRET',
           'fb_exchange_token': short_token
       }
   )
   
   print(response.json())
   ```

3. **Update .env with Long-Lived Token**

---

### Option 3: Use Meta Business Suite (Easiest)

1. Go to **Meta Business Suite:**
   https://business.facebook.com/

2. Select your Page

3. Go to **Settings** → **Developers** → **Access Tokens**

4. Generate new token with posting permissions

---

## 🔍 Verify Token is Working

After updating `.env`, run:

```bash
python test_facebook_token.py
```

This will verify your token is valid and has the right permissions.

---

## 📝 Token Expiry Info

| Token Type | Lifespan | Use Case |
|------------|----------|----------|
| Short-Lived | 1-2 hours | Testing |
| Long-Lived | 60 days | Production |
| Never Expires | Never | Enterprise (requires review) |

---

## ⚠️ Important Notes

1. **Never share your access token** publicly
2. **Store tokens securely** in `.env` file
3. **Set a reminder** to renew before expiry
4. **Use long-lived tokens** for production

---

## 🆘 Still Having Issues?

### Check Page Permissions
- Ensure you're an **admin** of the Facebook Page
- Page must be **published** (not in draft mode)

### Check App Permissions
- App must be **live** (not in development mode)
- App review may be required for some permissions

### Check Token Permissions
Run this to see what permissions your token has:

```python
import httpx

token = "YOUR_TOKEN"
response = httpx.get(
    "https://graph.facebook.com/v19.0/me/permissions",
    params={'access_token': token}
)
print(response.json())
```

---

## ✅ After Fixing

Once you've updated the token in `.env`:

```bash
# Post to Facebook
python post_facebook_live_now.py

# Or use the main poster
python post_live.py
```

---

**📧 Need Help?** Check the full documentation: `ADVANCED_SOCIAL_FEATURES.md`
