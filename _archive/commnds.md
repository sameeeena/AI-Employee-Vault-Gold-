# 🚀 Permanent Commands - Silver AI Employee

## 🏦 Accounting Commands (NEW!)

### Start Accounting Server:
```bash
accounting start
```

### Test Accounting System:
```bash
accounting test
```

### Check Status:
```bash
accounting status
```

### Stop Accounting Server:
```bash
accounting stop
```

### Create Invoice (API):
```bash
curl -X POST http://localhost:8000/create_invoice ^
  -H "Content-Type: application/json" ^
  -d "{\"partner_id\": 9, \"product_ids\": [1], \"quantities\": [1.0], \"prices\": [100.0]}"
```

### Get Profit & Loss (API):
```bash
curl -X POST http://localhost:8000/fetch_profit_loss ^
  -H "Content-Type: application/json" ^
  -d "{\"date_from\": \"2026-01-01\", \"date_to\": \"2026-12-31\"}"
```

**Documentation:** `ACCOUNTING_COMPLETE.md`

---

## 📧 Email Command (Sends + Tracks)

### Usage:
```bash
email recipient@example.com "Subject" "Message"
```

### Examples:
```bashp
# Send test email
email sameena02134@gmail.com "Test" "Hello from AI Employee!"

# Send meeting reminder
email client@company.com "Meeting Tomorrow" "Our meeting is at 2 PM"

# Send update
email boss@company.com "Project Update" "Project completed successfully"
```

### What Happens:
1. ✅ Email is sent
2. ✅ Task created in `Inbox/`
3. ✅ Task flows: Inbox → Needs_Action → Done
4. ✅ Dashboard updates automatically

---

## 📱 WhatsApp Command (Sends + Tracks)

### Usage:
```bash
whatsapp +923222208301 "Message" "Project Name"
```

### Examples:
```bash
# Send test WhatsApp
whatsapp +923222208301 "Hello from AI Employee!" "My Project"

# Send meeting reminder
whatsapp +919876543210 "Meeting at 2 PM tomorrow" "Reminders"

# Send update
whatsapp +923001234567 "Project completed successfully" "Updates"
```

### What Happens:
1. ✅ WhatsApp message is sent
2. ✅ Task created in `Inbox/`
3. ✅ Task flows: Inbox → Needs_Action → Done
4. ✅ Dashboard updates automatically

---

## 🏃 Start System

### Start All Components:
```bash
start_system.bat
```

This opens 3 windows:
- File Watcher (monitors Inbox)
- Orchestrator (processes tasks)
- Dashboard (shows metrics)

---

## 📊 Dashboard Commands

### Update Dashboard:
```bash
python dashboard_updater.py --action update
```

### View Status:
```bash
python dashboard_updater.py --action status
```

### Export Metrics:
```bash
python dashboard_updater.py --action export --output metrics.json
```

---

## 📁 File Lifecycle

```
External Input (Email/WhatsApp)
        ↓
Inbox (raw ingestion)
        ↓
Needs_Action (processing queue)
        ↓
Done (completed tasks)
        ↓
Dashboard (status reflection)
```

---

## 🔧 Quick Troubleshooting

### Email not sending?
```bash
# Check Gmail App Password
# Get from: https://myaccount.google.com/apppasswords
# Update in .env: SMTP_PASSWORD=xxxx xxxx xxxx xxxx
```

### WhatsApp not sending?
```bash
# Make sure you're logged into WhatsApp Web
# Go to: https://web.whatsapp.com
# Scan QR code if needed
```

### Task not moving?
```bash
# Make sure these are running:
python filesystem_watcher.py
python orchestrator_simple.py
```

### Dashboard not updating?
```bash
python dashboard_updater.py --action update
```

---

**All commands ready to use!** 🎉
python email_send.py recipient@example.com "Subject" "Message"
python email_send.py sameena02134@gmail.com "Test Mail" "Hello from AI Employee"
     
# Send WhatsApp with full tracking
whatsapp +923222208301 "Message" "Project Name"
      
 # Check system status
python dashboard_updater.py --action status

