# 📘 Facebook & Instagram Integration - Quick Start Guide
## (اردو / ہندی میں)

---

## ✅ آپ کے پروجیکٹ میں Integration پہلے سے موجود ہے!

---

## 🚀 **Step 1: Test کریں (5 منٹ)**

### Mock Mode میں Test کریں:
```bash
python test_facebook_instagram.py
```

**Expected Output:**
```
================================================================================
 FACEBOOK & INSTAGRAM INTEGRATION - TEST SUITE
================================================================================
[OK] Module imported successfully
[OK] Integration initialized (Mock Mode)

--------------------------------------------------------------------------------
 TEST 1: Post to Facebook
--------------------------------------------------------------------------------
[OK] Facebook Post Successful!
   Post ID: fb_mock_20260311120000
```

---

## 🚀 **Step 2: Complete Example Run کریں (5 منٹ)**

میں نے ایک نیا script بنایا ہے جو **posting + summary** دونوں کرتا ہے:

```bash
python social_post_summary_example.py
```

**یہ script یہ کام کرے گا:**
1. ✅ Facebook پر post کرے گا
2. ✅ Instagram پر post کرے گا
3. ✅ Facebook summary generate کرے گا
4. ✅ Instagram summary generate کرے گا
5. ✅ Combined summary generate کرے گا

---

## 🚀 **Step 3: API Server Start کریں (Optional)**

اگر آپ API endpoints use کرنا چاہتے ہیں:

```bash
python social_mcp_server_v2.py
```

**API Documentation کھولیں:**
```
http://localhost:8002/docs
```

**API Calls:**

```bash
# Facebook Post
curl -X POST "http://localhost:8002/api/post_message" ^
  -H "Content-Type: application/json" ^
  -d "{\"platform\": \"facebook\", \"message\": \"Hello from AI Employee Vault!\"}"

# Generate Summary
curl "http://localhost:8002/api/get_summary?platform=both"
```

---

## 📋 **Important Files**

| File | کام |
|------|-----|
| `social_post_summary_example.py` | ⭐ **Complete Example - Start Here!** |
| `test_facebook_instagram.py` | Testing script |
| `facebook_instagram_integration.py` | Main integration module |
| `social_mcp_server_v2.py` | API Server |
| `.env` | Configuration (tokens, IDs) |

---

## 🔧 **Configuration (.env file)**

آپ کی `.env` file میں:

```env
# ✅ Facebook (Already configured)
FACEBOOK_PAGE_ACCESS_TOKEN=EAASHynQdn7kBQxr5...
FACEBOOK_PAGE_ID=61585659193997

# ⚠️ Instagram (Fill these if you want Instagram posting)
INSTAGRAM_USER_ID=your_instagram_id
INSTAGRAM_ACCESS_TOKEN=your_instagram_token

# Mock Mode (true = test mode, false = live posting)
SOCIAL_MOCK_MODE=false
```

---

## 📖 **Quick Commands Reference**

| کام | Command |
|-----|---------|
| **Test run** | `python test_facebook_instagram.py` |
| **Complete example** | `python social_post_summary_example.py` |
| **API server start** | `python social_mcp_server_v2.py` |
| **API docs** | Open `http://localhost:8002/docs` |

---

## 💡 **Python Code Examples**

### Facebook Post:
```python
from facebook_instagram_integration import FacebookInstagramIntegration
import asyncio

async def post_fb():
    integration = FacebookInstagramIntegration()
    result = await integration.post_to_facebook(
        message="🎉 Hello from AI Employee Vault!"
    )
    print(f"Post ID: {result['post_id']}")

asyncio.run(post_fb())
```

### Generate Summary:
```python
async def get_summary():
    integration = FacebookInstagramIntegration()
    summary = await integration.generate_facebook_summary()
    
    print(f"Total Posts: {summary['total_posts']}")
    print(f"Total Reactions: {summary['total_reactions']}")
    print(f"Average Engagement: {summary['average_engagement']}")

asyncio.run(get_summary())
```

---

## ❓ **Troubleshooting**

### Problem: "Module not found"
**Solution:**
```bash
pip install httpx python-dotenv fastapi uvicorn pydantic
```

### Problem: "Invalid Access Token"
**Solution:**
1. Graph API Explorer میں token verify کریں
2. Token regenerate کریں
3. `.env` میں صحیح token ڈالیں

### Problem: Instagram not working
**Solution:**
1. Instagram Business Account بنائیں
2. Facebook Page سے connect کریں
3. `.env` میں `INSTAGRAM_USER_ID` اور `INSTAGRAM_ACCESS_TOKEN` ڈالیں

---

## ✅ **Verification Checklist**

- [ ] `python test_facebook_instagram.py` run ہوا
- [ ] `python social_post_summary_example.py` run ہوا
- [ ] Facebook post successful (mock or live)
- [ ] Summary generate ہوئی
- [ ] (Optional) API server start ہوا

---

## 🎉 **You're Ready!**

آپ کا integration تیار ہے! اب آپ:
- ✅ Facebook پر post کر سکتے ہیں
- ✅ Instagram پر post کر سکتے ہیں
- ✅ Summaries generate کر سکتے ہیں
- ✅ Analytics دیکھ سکتے ہیں

---

**📧 Support:** Troubleshooting section دیکھیں یا API error messages پڑھیں

**📚 Additional Resources:**
- Full Documentation: `FACEBOOK_INSTAGRAM_INTEGRATION.md`
- Facebook Graph API: https://developers.facebook.com/docs/graph-api
- Instagram Graph API: https://developers.facebook.com/docs/instagram-api
