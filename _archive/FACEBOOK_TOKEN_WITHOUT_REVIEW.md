# 🔑 Facebook Token Without pages_manage_posts

**Problem:** `pages_manage_posts` permission show nahi ho rahi hai.

**Reason:** Yeh permission **Advanced Access** maangti hai, jo sirf App Review ke baad milti hai.

---

## ✅ Solution: Alternative Permissions Use Karein

### Method 1: Basic Permissions (No Review Required)

In permissions ko try karein (ye sabko mil jaati hain):

```
pages_show_list
pages_read_engagement
publish_to_groups
```

**Direct Link:**
```
https://www.facebook.com/v19.0/dialog/oauth?client_id=1275203508084665&scope=pages_show_list,pages_read_engagement,publish_to_groups&response_type=token&display=page
```

---

### Method 2: Instagram Basic Display (Alternative)

Agar Facebook mein problem ho, toh Instagram use karein:

**Instagram Basic Display API:**
```
https://www.instagram.com/oauth/authorize?client_id=1275203508084665&redirect_uri=https://localhost&scope=user_profile&response_type=code
```

---

### Method 3: Meta Business Suite (Best Solution)

**Meta Business Suite se direct posting:**

1. https://business.facebook.com/ pe jayein
2. Apna Page select karein
3. Settings → Integrations
4. Generate Access Token

---

### Method 4: Long-Lived Token Generator

**Step 1: User Token lein (basic permissions):**

```
https://www.facebook.com/v19.0/dialog/oauth?client_id=1275203508084665&scope=public_profile,email&response_type=token&display=page
```

**Step 2: Token Exchange Tool use karein:**

https://developers.facebook.com/tools/access_token/

---

### Method 5: Mock Mode Mein Test Karein (Temporary)

Jab tak token nahi milta, **Mock Mode** mein test karein:

**.env file update karein:**
```
SOCIAL_MOCK_MODE=true
```

**Phir test karein:**
```bash
python autopost_facebook.py
```

Mock mode mein post actually publish nahi hoga, lekin aapka code test ho jayega.

---

## 🎯 Recommended: Page Access Token Direct Link

**Ye try karein (sabse aasan):**

```
https://www.facebook.com/v19.0/dialog/oauth?client_id=1275203508084665&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=pages_manage_posts,pages_read_engagement,pages_show_list&response_type=token&display=popup
```

Agar yeh bhi na chale, toh:

**Sirf basic permissions ke saath:**
```
https://www.facebook.com/v19.0/dialog/oauth?client_id=1275203508084665&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=pages_show_list&response_type=token&display=popup
```

---

## 📋 Step-by-Step: App Review Ke Bina

### Step 1: App Status Check Karein

1. https://developers.facebook.com/apps/1275203508084665/app-review/
2. Agar "Development Mode" hai, toh aap hi use kar sakte hain
3. "Public" karne ke liye review chahiye

### Step 2: Test User Add Karein

1. https://developers.facebook.com/apps/1275203508084665/roles/test-users/
2. "Add" button click karein
3. Apna Facebook account add karein
4. Test user ban jayega

### Step 3: Test User Se Token Lein

1. Facebook se logout karein
2. Test user credentials se login karein
3. Graph API Explorer pe jayein
4. `/me/accounts` query chalayein

---

## 🧪 Quick Test Script

```bash
python check_facebook_token.py
```

(Ye script batayegi ki kaunsi permissions available hain)

---

## ⚡ Fastest Solution

**Agar kuch bhi na chale, toh ye karein:**

1. **.env mein Mock Mode ON karein:**
   ```
   SOCIAL_MOCK_MODE=true
   ```

2. **Test karein:**
   ```bash
   python autopost_facebook.py
   ```

3. **Jab time mile, tab App Review submit karein**

---

## 📞 App Review Kaise Submit Karein

Agar aapko `pages_manage_posts` chahiye:

1. **Dashboard:** https://developers.facebook.com/apps/1275203508084665/
2. **App Review → Permissions**
3. **pages_manage_posts** select karein
4. **Use Case** likhein (kya banana chahte hain)
5. **Video demo** record karein (2-3 minute)
6. **Submit for Review**

**Review time:** 3-7 days

---

## 🔗 Helpful Links

| Link | Purpose |
|------|---------|
| https://developers.facebook.com/apps/1275203508084665/app-review/ | App Review |
| https://developers.facebook.com/tools/explorer/1275203508084665/ | Graph API Explorer |
| https://developers.facebook.com/tools/access_token/ | Token Tool |
| https://business.facebook.com/ | Meta Business Suite |

---

**Recommendation:** Pehle **Mock Mode** mein test karein, phir App Review submit karein.
