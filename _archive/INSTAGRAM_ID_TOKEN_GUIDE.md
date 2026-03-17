# 📷 Instagram ID & Access Token - Complete Step-by-Step Guide
## (اردو / ہندی میں)

---

## 🎯 **Overview**

Instagram پر posts کرنے کے لیے آپ کو 3 چیزیں چاہیے:

1. ✅ **Facebook Page Access Token** (already ہے)
2. ⚠️ **Instagram Business ID** (حاصل کرنا ہے)
3. ⚠️ **Instagram Access Token** (already ہے - Facebook token ہی use ہوگا)

---

## 📋 **Prerequisites**

### **ضروری چیزیں:**

- [ ] Facebook Business Page (ہونا چاہیے)
- [ ] Instagram Account (ہونا چاہیے)
- [ ] Instagram کو **Business Account** میں convert کریں
- [ ] Instagram کو Facebook Page سے **connect** کریں

---

## 🚀 **Step-by-Step Instructions**

### **STEP 1: Instagram Business Account بنائیں**

#### **Mobile App سے:**

1. **Instagram App** کھولیں
2. **Profile** پر جائیں (نیچے دائیں طرف)
3. **Menu** (3 lines) → **Settings and privacy**
4. **Account type and tools** پر click کریں
5. **Switch to professional account** select کریں
6. **Business** select کریں (Creator نہیں)
7. Category select کریں (e.g., "Business & Utility Services")
8. **Done!**

---

### **STEP 2: Instagram کو Facebook Page سے Connect کریں**

#### **Mobile App سے:**

1. **Instagram App** کھولیں
2. **Profile** → **Menu** (3 lines) → **Settings**
3. **Accounts Center** → **Connected Accounts**
4. **Facebook** select کریں
5. اپنا Facebook account سے login کریں
6. اپنا **Facebook Page** select کریں
7. **Done!**

#### **یا Facebook سے:**

1. Facebook.com پر جائیں
2. اپنا **Page** کھولیں
3. **Settings** → **Linked Accounts**
4. **Instagram** select کریں
5. **Connect Account** click کریں
6. Instagram login کریں
7. **Done!**

---

### **STEP 3: Facebook App میں Instagram Graph API Enable کریں**

1. **Facebook Developers** کھولیں:
   ```
   https://developers.facebook.com/
   ```

2. **My Apps** → اپنا App select کریں (`1275203508084665`)

3. **Add Product** click کریں

4. **Instagram Graph API** ڈھونڈیں

5. **Set Up** click کریں

6. **Done!**

---

### **STEP 4: Instagram Business ID حاصل کریں**

#### **طریقہ 1: Graph API Explorer (Recommended)**

1. **Graph API Explorer** کھولیں:
   ```
   https://developers.facebook.com/tools/explorer/
   ```

2. **App Select کریں:**
   - Dropdown سے `1275203508084665` select کریں

3. **Access Token Generate کریں:**
   - **Get Token** → **Get Page Access Token** click کریں
   - اپنا Facebook Page select کریں
   - Permissions check کریں:
     - ✅ `pages_manage_posts`
     - ✅ `pages_read_engagement`
     - ✅ `pages_show_list`
     - ✅ `instagram_basic`
     - ✅ `instagram_content_publish`
     - ✅ `instagram_manage_comments`
     - ✅ `instagram_manage_insights`

4. **Query چلائیں:**

   Graph API Explorer میں یہ لکھیں:
   ```
   GET /me/accounts
   ```
   
   **Submit** click کریں

5. **Response میں Page ID copy کریں:**

   ```json
   {
     "data": [
       {
         "access_token": "EAASHynQdn7kBQ...",
         "id": "61585659193997",
         "name": "Your Page Name"
       }
     ]
   }
   ```

6. **Instagram Business ID حاصل کریں:**

   اب یہ query چلائیں:
   ```
   GET /61585659193997?fields=instagram_business_account
   ```
   
   (اپنا Page ID use کریں)

7. **Response:**

   ```json
   {
     "instagram_business_account": {
       "id": "17841405822304915"
     }
   }
   ```

   **یہ ہے آپ کا Instagram Business ID!**
   
   ✅ **Copy کریں:** `17841405822304915`

---

#### **طریقہ 2: Python Script سے (Automated)**

میں نے script بنائی ہے، run کریں:

```bash
python get_instagram_id.py
```

---

### **STEP 5: Instagram Access Token حاصل کریں**

**اچھی خبر:** Instagram کے لیے الگ token کی ضرورت نہیں! 

آپ **Facebook Page Access Token** ہی use کر سکتے ہیں۔

#### **Already ہے آپ کے پاس:**

`.env` file میں:
```env
FACEBOOK_PAGE_ACCESS_TOKEN=EAASHynQdn7kBQ...
```

یہی token Instagram کے لیے بھی use ہوگا۔

#### **یا نیا Token چاہیے تو:**

1. **Graph API Explorer** کھولیں:
   ```
   https://developers.facebook.com/tools/explorer/
   ```

2. **Query چلائیں:**
   ```
   GET /me/accounts
   ```

3. **Response سے copy کریں:**
   ```json
   {
     "data": [
       {
         "access_token": "EAASHynQdn7kBQ...",  ← یہ copy کریں
         "id": "61585659193997"
       }
     ]
   }
   ```

---

### **STEP 6: .env File Update کریں**

`.env` file کھولیں اور یہ add کریں:

```env
# Instagram Configuration
INSTAGRAM_USER_ID=17841405822304915  # Step 4 سے ID
INSTAGRAM_ACCESS_TOKEN=EAASHynQdn7kBQ...  # Facebook token ہی use کریں

# Mock Mode بند کریں
SOCIAL_MOCK_MODE=false
```

---

### **STEP 7: Test کریں**

```bash
python instagram_autopost_now.py --template 1
```

---

## 🎯 **Quick Summary**

| Step | کام | کہاں سے |
|------|-----|---------|
| 1 | Instagram Business Account | Instagram App |
| 2 | Connect to Facebook | Instagram/Facebook Settings |
| 3 | Enable Instagram Graph API | Facebook Developers |
| 4 | Get Instagram ID | Graph API Explorer |
| 5 | Get Access Token | Graph API Explorer (Facebook token) |
| 6 | Update .env | .env file |
| 7 | Test | Command line |

---

## 🔧 **Alternative: Use My Script**

میں نے automated script بنائی ہے:

```bash
python get_instagram_id.py
```

یہ script:
- Graph API Explorer کھولے گی
- Step-by-step guide دے گی
- ID automatically fetch کرنے میں مدد کرے گی

---

## ⚠️ **Troubleshooting**

### **Problem: "Instagram Business Account not found"**

**Solution:**
1. Instagram کو Business Account میں convert کریں
2. Facebook Page سے connect کریں
3. 5 minutes wait کریں (propagation کے لیے)
4. دوبارہ try کریں

---

### **Problem: "Permissions missing"**

**Solution:**

Graph API Explorer میں یہ permissions ضرور لیں:
- ✅ `pages_manage_posts`
- ✅ `pages_read_engagement`
- ✅ `instagram_basic`
- ✅ `instagram_content_publish`

---

### **Problem: "Empty response"**

**Solution:**
1. Facebook Page سے Instagram disconnect کریں
2. دوبارہ connect کریں
3. Graph API Explorer میں token refresh کریں
4. دوبارہ try کریں

---

## 📞 **Need More Help?**

### **Video Tutorials:**

1. **Instagram Graph API Setup:**
   ```
   https://www.youtube.com/results?search_query=instagram+graph+api+setup
   ```

2. **Get Instagram Business ID:**
   ```
   https://www.youtube.com/results?search_query=get+instagram+business+account+id
   ```

### **Official Documentation:**

- **Instagram Graph API:** https://developers.facebook.com/docs/instagram-api
- **Getting Started:** https://developers.facebook.com/docs/instagram-api/getting-started

---

## ✅ **Quick Checklist**

- [ ] Instagram Business Account بنایا
- [ ] Facebook Page سے connect کیا
- [ ] Instagram Graph API enable کیا
- [ ] Graph API Explorer میں query چلائی
- [ ] Instagram Business ID copy کیا
- [ ] .env file update کی
- [ ] `SOCIAL_MOCK_MODE=false` کیا
- [ ] Test کیا: `python instagram_autopost_now.py --template 1`

---

## 🎉 **You're Done!**

After completing all steps:

```bash
# Instagram پر post کریں
python instagram_autopost_now.py --template 1

# Template 2 سے
python instagram_autopost_now.py --template 2

# Template 3 سے
python instagram_autopost_now.py --template 3
```

---

**Created:** 2026-03-11  
**Status:** ✅ Step-by-Step Guide Complete
