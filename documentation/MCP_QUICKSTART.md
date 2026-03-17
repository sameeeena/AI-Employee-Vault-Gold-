# 🚀 MULTI-MCP SERVERS - QUICK START GUIDE

**Get started with multiple MCP servers for different action types in 5 minutes!**

---

## ⚡ Quick Commands

### Start All MCP Servers

```bash
# Using Orchestrator (Recommended)
python mcp_orchestrator.py start

# Or using Manager
python mcp_server_manager.py start
```

### Check Status

```bash
python mcp_orchestrator.py status
```

### Stop All Servers

```bash
python mcp_orchestrator.py stop
```

---

## 📋 What You Get

### 4 Domain-Specific MCP Servers:

| Domain | Port | Purpose | Key Actions |
|--------|------|---------|-------------|
| **Accounting** | 8001 | Financial operations | Invoice, Expense, Reports |
| **Social Media** | 8002 | Social posting | Facebook, Instagram, Twitter |
| **Personal** | 8003 | Personal tasks | Appointments, Reminders |
| **Business** | 8004 | Business ops | Meetings, CRM, Sales |

---

## 🎯 Usage Examples

### Example 1: Post to Social Media

```python
import httpx

# Post to Facebook
response = httpx.post("http://localhost:8002/api/post_message", json={
    "platform": "facebook",
    "message": "Hello from AI Employee Vault! 🚀"
})

print(response.json())
```

### Example 2: Create Invoice

```python
import httpx

# Create invoice (Accounting domain)
response = httpx.post("http://localhost:8001/api/create_invoice", json={
    "customer": "ABC Corp",
    "amount": 5000,
    "description": "Consulting services"
})

print(response.json())
```

### Example 3: Schedule Meeting

```python
import httpx

# Schedule meeting (Business domain)
response = httpx.post("http://localhost:8004/api/schedule_meeting", json={
    "title": "Board Meeting",
    "datetime": "2026-03-20T14:00:00",
    "participants": ["john@example.com"]
})

print(response.json())
```

### Example 4: Using Orchestrator (Smart Routing)

```python
import httpx

# Orchestrator automatically routes to correct domain
response = httpx.post("http://localhost:8000/api/execute_action", json={
    "action_type": "invoice",  # Automatically routed to Accounting
    "params": {
        "customer": "XYZ Ltd",
        "amount": 3000
    }
})

print(response.json())
```

---

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │  ORCHESTRATOR   │
                    │   (Port 8000)   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  ACCOUNTING  │    │   BUSINESS   │    │   PERSONAL   │
│  (Port 8001) │    │  (Port 8004) │    │  (Port 8003) │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                    ┌──────────────┐
                    │ SOCIAL MEDIA │
                    │  (Port 8002) │
                    └──────────────┘
```

---

## 🔧 Configuration

### Server Configuration File

Edit `mcp_config/mcp_orchestrator_config.json` to:
- Add/remove servers
- Change ports
- Configure routing rules
- Adjust timeouts

### Environment Variables

Set in `.env`:

```bash
# Accounting Domain
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=admin

# Social Media Domain
FACEBOOK_PAGE_ACCESS_TOKEN=your_token
FACEBOOK_PAGE_ID=your_page_id
INSTAGRAM_USER_ID=your_ig_id

# SMTP (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_password
```

---

## 📊 Health Monitoring

### Check Individual Server

```bash
# Accounting
curl http://localhost:8001/health

# Social Media
curl http://localhost:8002/health

# Personal
curl http://localhost:8003/health

# Business
curl http://localhost:8004/health
```

### Check All Servers

```bash
python mcp_orchestrator.py health
```

**Output:**
```
======================================================================
MCP ORCHESTRATOR STATUS
======================================================================
Timestamp: 2026-03-10T12:00:00
----------------------------------------------------------------------

Domain          Status       Port     Tools
----------------------------------------------------------------------
Accounting      ✅ healthy   8001     create_invoice, record_expense...
Social Media    ✅ healthy   8002     post_message, get_metrics...
Personal        ✅ healthy   8003     schedule_appointment, set_reminder...
Business        ✅ healthy   8004     schedule_meeting, update_crm...
```

---

## 🔄 Action Routing

The orchestrator automatically routes actions to the correct domain:

| Action Type | Routed To | Example |
|-------------|-----------|---------|
| `invoice` | Accounting | Create invoice |
| `expense` | Accounting | Record expense |
| `post` | Social Media | Post to Facebook |
| `meeting` | Business | Schedule meeting |
| `appointment` | Personal | Doctor appointment |

**Example:**
```python
# These are automatically routed to correct domain
POST /api/execute_action {"action_type": "invoice", ...}    → Accounting
POST /api/execute_action {"action_type": "post", ...}       → Social Media
POST /api/execute_action {"action_type": "meeting", ...}    → Business
```

---

## 🧪 Testing

### Test All Servers

```bash
# Start all servers
python mcp_orchestrator.py start

# Check health
python mcp_orchestrator.py health

# Test individual endpoints
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
```

### Test with Web Interface

Each server has a web interface:

- Accounting: http://localhost:8001
- Social Media: http://localhost:8002
- Personal: http://localhost:8003
- Business: http://localhost:8004

Open in browser to test tools interactively!

---

## 📁 File Structure

```
AI Employee Vault [Gold]/
├── mcp_orchestrator.py              # Main orchestrator
├── mcp_server_manager.py            # Server manager
├── mcp_server.py                    # Base MCP server
├── accounting_mcp_server.py         # Accounting domain
├── social_mcp_server_v2.py          # Social Media domain
├── personal_mcp_server.py           # Personal domain
├── business_mcp_server.py           # Business domain
├── mcp_config/
│   └── mcp_orchestrator_config.json # Configuration
├── logs/
│   ├── mcp_orchestrator_log.md     # Orchestrator logs
│   ├── accounting_log.md           # Accounting logs
│   ├── social_log.md               # Social logs
│   ├── personal_log.md             # Personal logs
│   └── business_log.md             # Business logs
└── MULTI_MCP_SERVERS.md            # Full documentation
```

---

## ⚠️ Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
netstat -ano | findstr :8001

# Kill the process
taskkill /F /PID <process_id>
```

### Server Won't Start

```bash
# Check Python syntax
python -m py_compile accounting_mcp_server.py

# Check dependencies
pip install fastapi uvicorn httpx python-dotenv pydantic
```

### Health Check Fails

1. Ensure server is running: `python mcp_orchestrator.py status`
2. Check logs: `type logs\accounting_log.md`
3. Restart server: `python mcp_orchestrator.py stop` then `start`

---

## 🎯 Next Steps

1. **Start all servers:**
   ```bash
   python mcp_orchestrator.py start
   ```

2. **Check health:**
   ```bash
   python mcp_orchestrator.py health
   ```

3. **Test with web interface:**
   - Open http://localhost:8002 (Social Media)
   - Try posting to Facebook

4. **Read full documentation:**
   - `MULTI_MCP_SERVERS.md` for detailed docs

---

## 📞 Quick Reference

| Command | Description |
|---------|-------------|
| `python mcp_orchestrator.py start` | Start all servers |
| `python mcp_orchestrator.py stop` | Stop all servers |
| `python mcp_orchestrator.py status` | Check status |
| `python mcp_orchestrator.py health` | Health check |
| `python mcp_server_manager.py start` | Alternative start |
| `curl http://localhost:8001/health` | Check Accounting |
| `curl http://localhost:8002/health` | Check Social Media |

---

**🎉 You're ready to use multiple MCP servers!**

For detailed documentation, see `MULTI_MCP_SERVERS.md`
