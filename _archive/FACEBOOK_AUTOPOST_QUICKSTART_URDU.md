# 📘 Facebook Auto-Post - Complete Guide
## (اردو / ہندی میں)

---

## ✅ آپ کے پروجیکٹ میں Facebook Auto-Post موجود ہے!

---

## 🚀 **Quick Start - 3 آسان Steps**

### **Step 1: فوراً Post کریں**

```bash
python facebook_autopost_now.py
```

یہ command available templates دکھائے گی۔

### **Step 2: Template Select کر کے Post کریں**

```bash
# Template 1 سے Post کریں
python facebook_autopost_now.py --template 1

# Template 2 سے Post کریں
python facebook_autopost_now.py --template 2

# Template 3 سے Post کریں
python facebook_autopost_now.py --template 3
```

### **Step 3: Custom Message کے ساتھ Post کریں**

```bash
python facebook_autopost_now.py --message "آپ کا message یہاں" --link "https://example.com"
```

---

## 📋 **Available Post Templates**

| ID | Template Name | Use Case |
|----|--------------|----------|
| 1 | 🎉 Product Announcement | نئی product announce کرنے کے لیے |
| 2 | 💼 Business Tips | Business tips share کرنے کے لیے |
| 3 | 🌟 Motivational Post | Motivational content کے لیے |
| 4 | 📊 Industry Insights | Industry trends کے لیے |
| 5 | 🎯 Customer Success | Customer testimonials کے لیے |
| 6 | 🔧 Feature Highlight | Features showcase کرنے کے لیے |
| 7 | 📚 Educational Content | Educational posts کے لیے |
| 8 | 🎊 Special Offer | Special offers/promotions کے لیے |

---

## ⏰ **Scheduled Posts (مقررہ وقت پر Post کریں)**

### **ایک خاص وقت پر Post کریں:**

```bash
# کل 9 بجے صبح Post کریں
python facebook_autopost_schedule.py --date 2026-03-12 --time 09:00 --template 1

# آج شام 6 بجے Post کریں
python facebook_autopost_schedule.py --date 2026-03-11 --time 18:00 --template 2
```

### **روزانہ کی Recurring Post:**

```bash
# روزانہ 9 بجے صبح Post
python facebook_autopost_schedule.py --recurring daily --time 09:00 --template 2

# روزانہ 6 بجے شام Post
python facebook_autopost_schedule.py --recurring daily --time 18:00 --template 3
```

### **ہفتہ وار Weekly Post:**

```bash
# ہر ہفتے پیر کو 9 بجے صبح Post
python facebook_autopost_schedule.py --recurring weekly --time 09:00 --template 1
```

### **تمام Scheduled Posts دیکھیں:**

```bash
python facebook_autopost_schedule.py --list
```

---

## 🔄 **Auto-Post Scheduler Start کریں**

Scheduled posts کو automatically publish کرنے کے لیے:

```bash
# Scheduler start کریں
python social_scheduler.py

# یا background میں چلائیں
start python social_scheduler.py
```

---

## 💡 **Complete Examples**

### **Example 1: Product Announcement**

```bash
python facebook_autopost_now.py --template 1 --link "https://yourwebsite.com"
```

### **Example 2: Daily Business Tips**

```bash
# Schedule daily business tips at 10 AM
python facebook_autopost_schedule.py --recurring daily --time 10:00 --template 2
```

### **Example 3: Custom Post with Image**

```bash
python facebook_autopost_now.py --message "🎉 Big News! Visit our new store." --image "https://example.com/store.jpg" --link "https://example.com"
```

### **Example 4: Multiple Scheduled Posts**

```bash
# Morning motivation at 8 AM
python facebook_autopost_schedule.py --recurring daily --time 08:00 --template 3

# Business tips at 2 PM
python facebook_autopost_schedule.py --recurring daily --time 14:00 --template 2

# Evening post at 6 PM
python facebook_autopost_schedule.py --recurring daily --time 18:00 --template 4
```

---

## 📁 **Files Reference**

| File | کام |
|------|-----|
| `facebook_autopost_now.py` | ⭐ فوراً Post کرنے کے لیے |
| `facebook_autopost_schedule.py` | ⏰ Scheduled posts کے لیے |
| `autopost_facebook.py` | Simple autopost script |
| `social_scheduler.py` | 🔄 Auto scheduler engine |
| `facebook_autopost.bat` | Windows quick menu |

---

## 🎯 **Quick Commands Reference**

| کام | Command |
|-----|---------|
| **فوراً Post کریں** | `python facebook_autopost_now.py` |
| **Template سے Post** | `python facebook_autopost_now.py --template 1` |
| **Custom Message** | `python facebook_autopost_now.py --message "Your message"` |
| **Schedule for later** | `python facebook_autopost_schedule.py -d 2026-03-12 -t 09:00 -t 1` |
| **Daily recurring** | `python facebook_autopost_schedule.py -r daily -t 09:00 -t 2` |
| **List schedules** | `python facebook_autopost_schedule.py --list` |
| **Start scheduler** | `python social_scheduler.py` |
| **Test connection** | `python test_facebook_connection.py` |

---

## 🔧 **Configuration (.env file)**

آپ کی `.env` file میں یہ ہونا ضروری ہے:

```env
# Facebook Configuration
FACEBOOK_PAGE_ACCESS_TOKEN=EAASHynQdn7kBQxr5ewsf1pNQmZBEsUZCCHx9j5dcueQR9s8ZBFPMoYG24k1fdRbTZAtUz9xapNxZBMWakToimOUBLhzboKQPGdDL1ttZCZB4XoBZASEMUrgmyZCVScpgHBesMUrm2YbR7EZATB7WgR5TJdZCoZC5sPwZAkarg62Ik83JSO4zH1cKXZAGZAQ3um2xoAZAg65OSbTE9YyHahlZBNYCuAuDpQWZA0jL5KQYdfyELnusPYzSaVVJygMTrjM2SGIBPtJVDcCbbvMB7vShZBAHQ83Q7oNpUTwRwZDZD
FACEBOOK_PAGE_ID=61585659193997

# Mock Mode (true = test, false = live)
SOCIAL_MOCK_MODE=false
```

---

## ⚠️ **Troubleshooting**

### **Problem: "Mock Mode is enabled"**

**Solution:**
`.env` file میں جائیں اور change کریں:
```env
SOCIAL_MOCK_MODE=false
```

### **Problem: "Invalid Access Token"**

**Solution:**
1. Graph API Explorer میں جائیں: https://developers.facebook.com/tools/explorer/
2. نیا token generate کریں
3. `.env` میں update کریں

### **Problem: "Module not found"**

**Solution:**
```bash
pip install httpx python-dotenv
```

---

## ✅ **Verification Checklist**

- [ ] `python facebook_autopost_now.py` run ہوا
- [ ] Template select کر کے post کیا
- [ ] Custom message سے post کیا
- [ ] Scheduled post create کیا
- [ ] Scheduler start کیا
- [ ] Live mode میں post کیا (SOCIAL_MOCK_MODE=false)

---

## 🎉 **You're Ready!**

آپ کا Facebook Auto-Post system تیار ہے!

### **Start Posting:**

```bash
# آج ہی post کریں
python facebook_autopost_now.py --template 1

# یا schedule کریں
python facebook_autopost_schedule.py --recurring daily --time 09:00 --template 2
```

---

**📧 Support:** Troubleshooting section دیکھیں یا API error messages پڑھیں

**📚 Additional Resources:**
- Full Documentation: `FACEBOOK_AUTOPOST_GUIDE.md`
- Token Setup: `FACEBOOK_TOKEN_SETUP.md`
- Integration Guide: `FACEBOOK_INSTAGRAM_INTEGRATION.md`
