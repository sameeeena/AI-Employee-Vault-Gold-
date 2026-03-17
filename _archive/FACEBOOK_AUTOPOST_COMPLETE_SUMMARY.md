# ✅ Facebook Auto-Post - COMPLETE SETUP GUIDE
## (اردو / ہندی میں)

---

## 🎯 **Summary - کیا بنایا گیا ہے**

آپ کے پروجیکٹ میں **Facebook Auto-Post system** مکمل طور پر تیار ہے!

---

## 📁 **New Files Created**

| File | Purpose | Status |
|------|---------|--------|
| `facebook_autopost_now.py` | ⭐ فوراً Post کریں | ✅ Ready |
| `facebook_autopost_schedule.py` | ⏰ Schedule posts | ✅ Ready |
| `facebook_autopost_easy_menu.bat` | 📋 Easy Menu (Windows) | ✅ Ready |
| `FACEBOOK_AUTOPOST_QUICKSTART_URDU.md` | 📖 Urdu Guide | ✅ Ready |

---

## 🚀 **Quick Start - 3 Steps**

### **Step 1: Easy Menu استعمال کریں (سب سے آسان)**

Double-click کریں:
```
facebook_autopost_easy_menu.bat
```

یہ ایک menu کھولے گا جس میں آپ select کر سکتے ہیں:
- Post templates (1-8)
- Schedule posts
- View scheduled posts
- Start scheduler

---

### **Step 2: Command Line سے Post کریں**

```bash
# Template 1 سے Post کریں (Product Announcement)
python facebook_autopost_now.py --template 1

# Template 2 سے Post کریں (Business Tips)
python facebook_autopost_now.py --template 2

# Template 3 سے Post کریں (Motivational)
python facebook_autopost_now.py --template 3
```

---

### **Step 3: Schedule Post کریں**

```bash
# کل 9 بجے صبح Post کریں
python facebook_autopost_schedule.py --date 2026-03-12 --time 09:00 --template 1

# روزانہ 9 بجے صبح Post کریں
python facebook_autopost_schedule.py --recurring daily --time 09:00 --template 2
```

---

## ⚠️ **IMPORTANT: Facebook Token Fix Required**

آپ کا Facebook Page ID یا Access Token صحیح نہیں ہے۔

**Error:**
```
(#100) The global id 61585659193997 is not allowed for this call
```

### **Solution - Token Fix کریں:**

#### **Step 1: Graph API Explorer میں جائیں**

URL: https://developers.facebook.com/tools/explorer/

#### **Step 2: App Select کریں**

Dropdown سے select کریں: `1275203508084665`

#### **Step 3: Permissions Select کریں**

Click کریں **"Get Token"** → **"Get Page Access Token"**

Select کریں:
- ✅ `pages_manage_posts`
- ✅ `pages_read_engagement`
- ✅ `pages_show_list`

#### **Step 4: Query چلائیں**

Graph API Explorer میں یہ query چلائیں:

```
GET /me/accounts
```

#### **Step 5: Results copy کریں**

Response میں سے یہ copy کریں:
- `access_token` → یہ ہے آپ کا **FACEBOOK_PAGE_ACCESS_TOKEN**
- `id` → یہ ہے آپ کا **FACEBOOK_PAGE_ID**

Example response:
```json
{
  "data": [
    {
      "access_token": "EAASHynQdn7kBQxr5ewsf1pNQmZBEsUZCCHx9j5dcueQR9s8ZBFPMoYG24k1fdRbTZAtUz9xapNxZBMWakToimOUBLhzboKQPGdDL1ttZCZB4XoBZASEMUrgmyZCVScpgHBesMUrm2YbR7EZATB7WgR5TJdZCoZC5sPwZAkarg62Ik83JSO4zH1cKXZAGZAQ3um2xoAZAg65OSbTE9YyHahlZBNYCuAuDpQWZA0jL5KQYdfyELnusPYzSaVVJygMTrjM2SGIBPtJVDcCbbvMB7vShZBAHQ83Q7oNpUTwRwZDZD",
      "id": "61585659193997"
    }
  ]
}
```

#### **Step 6: .env File Update کریں**

`.env` file کھولیں اور update کریں:

```env
FACEBOOK_PAGE_ACCESS_TOKEN=NEW_TOKEN_HERE (Step 5 سے copy کریں)
FACEBOOK_PAGE_ID=61585659193997 (Step 5 سے copy کریں)
SOCIAL_MOCK_MODE=false
```

#### **Step 7: Test کریں**

```bash
python facebook_autopost_now.py --template 1
```

---

## 📋 **Available Post Templates**

| ID | Name | Use Case |
|----|------|----------|
| 1 | 🎉 Product Announcement | نئی product launch |
| 2 | 💼 Business Tips | Business tips share |
| 3 | 🌟 Motivational | Motivational quotes |
| 4 | 📊 Industry Insights | Industry trends |
| 5 | 🎯 Customer Success | Testimonials |
| 6 | 🔧 Feature Highlight | Features showcase |
| 7 | 📚 Educational | Educational content |
| 8 | 🎊 Special Offer | Promotions/offers |

---

## 💡 **Usage Examples**

### **Example 1: فوراً Post کریں**

```bash
python facebook_autopost_now.py --template 1
```

### **Example 2: Custom Message**

```bash
python facebook_autopost_now.py --message "آپ کا message یہاں" --link "https://example.com"
```

### **Example 3: Schedule for Tomorrow**

```bash
python facebook_autopost_schedule.py --date 2026-03-12 --time 09:00 --template 2
```

### **Example 4: Daily Recurring Post**

```bash
python facebook_autopost_schedule.py --recurring daily --time 09:00 --template 3
```

### **Example 5: View All Scheduled Posts**

```bash
python facebook_autopost_schedule.py --list
```

---

## 🔄 **Auto Scheduler Start کریں**

Scheduled posts کو automatically publish کرنے کے لیے:

```bash
# Background میں scheduler start کریں
start python social_scheduler.py
```

---

## 📊 **Complete Commands Reference**

| کام | Command |
|-----|---------|
| **Easy Menu** | `facebook_autopost_easy_menu.bat` |
| **Post Now (Template 1)** | `python facebook_autopost_now.py --template 1` |
| **Post Now (Template 2)** | `python facebook_autopost_now.py --template 2` |
| **Custom Message** | `python facebook_autopost_now.py --message "Your message"` |
| **Schedule Post** | `python facebook_autopost_schedule.py -d 2026-03-12 -t 09:00 -t 1` |
| **Daily Recurring** | `python facebook_autopost_schedule.py -r daily -t 09:00 -t 2` |
| **Weekly Recurring** | `python facebook_autopost_schedule.py -r weekly -t 09:00 -t 3` |
| **View Schedules** | `python facebook_autopost_schedule.py --list` |
| **Start Scheduler** | `start python social_scheduler.py` |
| **Test Connection** | `python test_facebook_connection.py` |

---

## ✅ **Verification Checklist**

- [ ] Facebook Token fix کیا (Graph API Explorer سے)
- [ ] `.env` file update کی
- [ ] `facebook_autopost_easy_menu.bat` run کیا
- [ ] Template سے post کیا
- [ ] Custom message سے post کیا
- [ ] Scheduled post create کیا
- [ ] Scheduler start کیا

---

## 🎉 **You're Ready!**

### **Start Posting Now:**

```bash
# Double-click کریں
facebook_autopost_easy_menu.bat

# Select کریں: 2 (Post - Product Announcement)
```

**یا command line سے:**

```bash
python facebook_autopost_now.py --template 1
```

---

## 📧 **Support**

**Token Issues:** `FACEBOOK_TOKEN_SETUP.md` دیکھیں

**Full Documentation:** `FACEBOOK_AUTOPOST_GUIDE.md` دیکھیں

**Graph API Explorer:** https://developers.facebook.com/tools/explorer/

---

## 📚 **All Documentation Files**

| File | Language |
|------|----------|
| `FACEBOOK_AUTOPOST_QUICKSTART_URDU.md` | Urdu/Hindi |
| `FACEBOOK_AUTOPOST_GUIDE.md` | English |
| `FACEBOOK_TOKEN_SETUP.md` | English |
| `FACEBOOK_INSTAGRAM_INTEGRATION.md` | English |

---

**Created:** 2026-03-11  
**Status:** ✅ Complete (Token Fix Required)
