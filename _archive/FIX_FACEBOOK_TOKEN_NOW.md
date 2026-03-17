# ⚠️ FACEBOOK TOKEN FIX - Quick Guide
## (اردو / ہندی میں)

---

## ❌ **Current Error:**

```
(#100) The global id 61585659193997 is not allowed for this call
```

**Problem:** آپ کا Facebook Page Access Token expire ہو گیا ہے یا صحیح نہیں ہے۔

---

## ✅ **Solution - 5 Easy Steps:**

### **Step 1: Graph API Explorer کھولیں**

URL پر جائیں:
```
https://developers.facebook.com/tools/explorer/
```

---

### **Step 2: App Select کریں**

Dropdown سے select کریں:
```
1275203508084665
```

---

### **Step 3: Get Page Access Token**

1. **"Get Token"** button پر click کریں
2. **"Get Page Access Token"** select کریں
3. اپنی Facebook Page select کریں
4. Permissions check کریں:
   - ✅ `pages_manage_posts`
   - ✅ `pages_read_engagement`
   - ✅ `pages_show_list`

---

### **Step 4: Query چلائیں**

Graph API Explorer میں یہ query چلائیں:

```
GET /me/accounts
```

**Response کچھ ایسا ہوگا:**

```json
{
  "data": [
    {
      "access_token": "EAAG... (long token here)",
      "id": "123456789012345",
      "name": "Your Page Name"
    }
  ]
}
```

---

### **Step 5: .env File Update کریں**

1. `.env` file کھولیں
2. یہ values replace کریں:

```env
# OLD (delete this):
FACEBOOK_PAGE_ACCESS_TOKEN=EAASHynQdn7kBQxr5ewsf1pNQmZBEsUZCCHx9j5dcueQR9s8ZBFPMoYG24k1fdRbTZAtUz9xapNxZBMWakToimOUBLhzboKQPGdDL1ttZCZB4XoBZASEMUrgmyZCVScpgHBesMUrm2YbR7EZATB7WgR5TJdZCoZC5sPwZAkarg62Ik83JSO4zH1cKXZAGZAQ3um2xoAZAg65OSbTE9YyHahlZBNYCuAuDpQWZA0jL5KQYdfyELnusPYzSaVVJygMTrjM2SGIBPtJVDcCbbvMB7vShZBAHQ83Q7oNpUTwRwZDZD
FACEBOOK_PAGE_ID=61585659193997

# NEW (paste from Graph API Explorer results):
FACEBOOK_PAGE_ACCESS_TOKEN=NEW_TOKEN_FROM_STEP_4
FACEBOOK_PAGE_ID=NEW_PAGE_ID_FROM_STEP_4
```

---

## 🧪 **Test کریں:**

```bash
python facebook_autopost_now.py --template 1
```

---

## 🎯 **Quick Alternative - Use Mock Mode for Testing:**

اگر آپ abhi test کرنا چاہتے ہیں (live post نہیں):

1. `.env` file میں:
```env
SOCIAL_MOCK_MODE=true
```

2. Test کریں:
```bash
python facebook_autopost_now.py --template 1
```

**Mock mode میں:**
- ✅ Post simulate ہوگی
- ✅ آپ کو success message ملے گا
- ❌ Facebook پر actually post نہیں ہوگی

---

## 📞 **Need Help?**

1. **Video Tutorial:** https://www.youtube.com/results?search_query=facebook+page+access+token+graph+api+explorer

2. **Facebook Docs:** https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow

3. **Existing Guide:** `FACEBOOK_TOKEN_SETUP.md` دیکھیں

---

**Token fix کرنے کے بعد:**
```bash
python facebook_autopost_now.py --template 1
```

---

**Created:** 2026-03-11  
**Status:** ⚠️ Token Fix Required
