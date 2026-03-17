# 🔑 Facebook Page Access Token - Hindi Guide

**Problem:** `pages_manage_posts` permission show nahi ho rahi hai.

---

## ✅ Solution: Step-by-Step

### Step 1: App Review Check Karein

1. **Facebook Developers Dashboard pe jayein:**
   - https://developers.facebook.com/apps/1275203508084665/dashboard/

2. **App Mode Check Karein:**
   - Top-right corner mein dekhein
   - Agar **Development Mode** hai, toh sirf aap hi use kar sakte hain
   - **Public** karne ke liye App Review zaroori hai

3. **Permissions Add Karein:**
   - Left menu: **App Review** → **Permissions and Features**
   - `pages_manage_posts` search karein
   - **Request Advanced Access** pe click karein

---

### Step 2: Testing ke liye (Development Mode)

Agar App Review nahi karna chahte, toh **Development Mode** mein test karein:

1. **Graph API Explorer kholein:**
   - https://developers.facebook.com/tools/explorer/

2. **App Select karein:**
   - Dropdown se `1275203508084665` select karein

3. **Get Token → Get User Access Token:**
   - Neeche permissions select karein:
     - ✅ `pages_manage_posts`
     - ✅ `pages_read_engagement`
     - ✅ `pages_show_list`
   
   - **Agar `pages_manage_posts` show nahi ho rahi:**
     - Neeche "Custom Permissions" mein manually type karein
     - Ya direct URL use karein (Step 3 dekhein)

4. **Continue** → **Done**

---

### Step 3: Direct URL Method (Best Solution)

**Direct link se token generate karein:**

```
https://developers.facebook.com/tools/explorer/?selected_tab=api_explorer&graph_api_version=v19.0&user_token=
```

**Ya ye URL try karein:**

```
https://www.facebook.com/v19.0/dialog/oauth?client_id=1275203508084665&redirect_uri=https://developers.facebook.com/tools/explorer&scope=pages_manage_posts,pages_read_engagement,pages_show_list&response_type=token
```

---

### Step 4: Page Access Token Nikalein

1. **Graph API Explorer mein query chalayen:**
   ```
   GET /me/accounts
   ```

2. **Response mein dekhein:**
   ```json
   {
     "data": [
       {
         "name": "Your Page Name",
         "id": "1234567890",
         "access_token": "EAAG...yeh_hai_page_token"
       }
     ]
   }
   ```

3. **`access_token` copy karein** (ye hai Page Access Token)

4. **`.env` file update karein:**
   ```
   FACEBOOK_PAGE_ACCESS_TOKEN=EAAG...yeh_token
   FACEBOOK_PAGE_ID=1234567890
   ```

---

## 🎯 Alternative: Meta Business Suite

Agar Graph API mein problem ho rahi hai:

### Meta Business Suite se Token:

1. **Business Settings:**
   - https://business.facebook.com/settings

2. **Apps → Select your app**

3. **Add Assets → Pages**

4. **Assign Token:**
   - Generate long-lived token

---

## 🧪 Test Token

Token milne ke baad test karein:

```bash
python debug_facebook.py
```

**Expected output:**
```
Status: 200
Response: {"data":[{"name":"Your Page","id":"...","access_token":"..."}]}
```

---

## ⚡ Quick Fix Script

Main aapke liye ek script bana raha hoon jo directly token fetch karegi:

```bash
python get_facebook_token.py
```

(Ye script abhi create hogi)

---

## 📞 Common Issues

### "pages_manage_posts not available"
- **Cause:** App review pending hai
- **Fix:** Development mode mein aapke account se test karein

### "No pages found"
- **Cause:** Aap page ke admin nahi hain
- **Fix:** Page se aapko admin access chahiye

### "Token expired"
- **Cause:** 1-hour token hai
- **Fix:** Long-lived token generate karein (60 days)

---

## 🔗 Helpful Links

- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **Access Token Tool:** https://developers.facebook.com/tools/accesstoken/
- **Business Manager:** https://business.facebook.com/settings

---

**Agar abhi bhi problem ho toh batayein, main aur help karunga!**
