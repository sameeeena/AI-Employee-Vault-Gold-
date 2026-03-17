# 🔄 MULTI-MCP SERVER ARCHITECTURE

**Multiple MCP Servers for Different Action Types**

**Status:** ✅ COMPLETE | **Version:** 2.0.0 | **Date:** 2026-03-10

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Server Configuration](#server-configuration)
4. [Action Types by Domain](#action-types-by-domain)
5. [Quick Start](#quick-start)
6. [API Reference](#api-reference)
7. [Cross-Domain Integration](#cross-domain-integration)
8. [Monitoring & Health Checks](#monitoring--health-checks)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project implements a **multi-domain MCP (Model Context Protocol) architecture** where each business domain has its own dedicated MCP server with specialized tools and actions.

### Benefits:

- ✅ **Separation of Concerns** - Each domain handles its own actions
- ✅ **Scalability** - Easy to add new domains
- ✅ **Independent Deployment** - Servers can be started/stopped independently
- ✅ **Domain-Specific Tools** - Each server has specialized tools for its domain
- ✅ **Cross-Domain Integration** - Servers can communicate for complex workflows

---

## 🏗️ Architecture

### Server Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS DOMAIN                               │
│              (Business MCP Server - Port 8004)                  │
│                                                                  │
│  Tools: meetings, CRM, sales_pipeline, contracts, projects      │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   PERSONAL   │    │  ACCOUNTING  │    │ SOCIAL MEDIA │
│  (Port 8003) │    │  (Port 8001) │    │  (Port 8002) │
│              │    │              │    │              │
│ appointments │    │  invoicing   │    │   facebook   │
│  reminders   │    │   expenses   │    │  instagram   │
│    travel    │    │   reports    │    │   twitter    │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## ⚙️ Server Configuration

### MCP Servers

| Domain | Server File | Port | Action Types |
|--------|-------------|------|--------------|
| **Accounting** | `accounting_mcp_server.py` | 8001 | Invoicing, Expenses, Reports, Payments |
| **Social Media** | `social_mcp_server_v2.py` | 8002 | Facebook, Instagram, Twitter, Analytics |
| **Personal** | `personal_mcp_server.py` | 8003 | Appointments, Reminders, Travel, Tasks |
| **Business** | `business_mcp_server.py` | 8004 | Meetings, CRM, Sales, Projects, Contracts |

### Configuration Files

Each server has its own configuration in `mcp_config/`:

- `accounting_mcp_config.json`
- `social_mcp_config.json`
- `personal_mcp_config.json`
- `business_mcp_config.json`

---

## 🎯 Action Types by Domain

### 1. **Accounting Domain** (Port 8001)

**Server:** `accounting_mcp_server.py`

**Action Types:**
- `create_invoice` - Create new invoice
- `record_expense` - Record business expense
- `generate_report` - Generate financial report
- `process_payment` - Process payment
- `get_account_balance` - Get account balance
- `reconcile_transaction` - Reconcile bank transaction

**Example:**
```python
# Create invoice
result = await client.post("http://localhost:8001/api/create_invoice", json={
    "customer": "ABC Corp",
    "amount": 5000,
    "due_date": "2026-04-01"
})
```

---

### 2. **Social Media Domain** (Port 8002)

**Server:** `social_mcp_server_v2.py`

**Action Types:**
- `post_message` - Post to social platform
- `get_metrics` - Get engagement metrics
- `generate_summary` - Generate analytics summary
- `schedule_post` - Schedule post for later
- `get_content_calendar` - Get content calendar

**Platforms:**
- Facebook
- Instagram
- Twitter/X
- LinkedIn

**Example:**
```python
# Post to Facebook
result = await client.post("http://localhost:8002/api/post_message", json={
    "platform": "facebook",
    "message": "Hello World! 🚀"
})
```

---

### 3. **Personal Domain** (Port 8003)

**Server:** `personal_mcp_server.py`

**Action Types:**
- `schedule_appointment` - Schedule personal appointment
- `set_reminder` - Set reminder
- `plan_travel` - Plan travel itinerary
- `create_personal_task` - Create personal task
- `get_calendar` - Get personal calendar

**Example:**
```python
# Schedule appointment
result = await client.post("http://localhost:8003/api/schedule_appointment", json={
    "title": "Doctor Appointment",
    "datetime": "2026-03-15T10:00:00",
    "location": "City Hospital"
})
```

---

### 4. **Business Domain** (Port 8004)

**Server:** `business_mcp_server.py`

**Action Types:**
- `schedule_meeting` - Schedule business meeting
- `update_crm` - Update CRM activity
- `update_sales_pipeline` - Update sales pipeline
- `create_project` - Create new project
- `manage_contract` - Manage contract
- `flag_financial_task` - Flag task for accounting
- `flag_marketing_task` - Flag task for social media

**Example:**
```python
# Schedule meeting
result = await client.post("http://localhost:8004/api/schedule_meeting", json={
    "title": "Board Meeting",
    "datetime": "2026-03-20T14:00:00",
    "participants": ["john@example.com", "jane@example.com"]
})
```

---

## 🚀 Quick Start

### Start All MCP Servers

```bash
# Using the manager
python mcp_server_manager.py start

# Or individually
python accounting_mcp_server.py &
python social_mcp_server_v2.py &
python personal_mcp_server.py &
python business_mcp_server.py &
```

### Check Health Status

```bash
python mcp_server_manager.py health
```

### Stop All Servers

```bash
python mcp_server_manager.py stop
```

### Start Specific Server

```bash
# Start only Accounting server
python mcp_server_manager.py start --domain Accounting
```

---

## 📖 API Reference

### Common Endpoints

All servers expose these common endpoints:

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Domain MCP Server",
  "timestamp": "2026-03-10T12:00:00"
}
```

#### List Tools
```http
GET /api/tools
```

**Response:**
```json
[
  {
    "name": "tool_name",
    "description": "Tool description",
    "parameters": {...}
  }
]
```

#### Call Tool
```http
POST /api/call_tool
```

**Request:**
```json
{
  "tool": "tool_name",
  "params": {...}
}
```

---

## 🔗 Cross-Domain Integration

### Integration Flows

#### Business → Accounting
When a business deal is closed, automatically flag for invoicing:

```python
# In Business MCP Server
await client.post("http://localhost:8001/api/flag_financial_task", json={
    "task_id": "deal_123",
    "content": "Closed deal with ABC Corp - $50,000",
    "source_domain": "Business"
})
```

#### Business → Social Media
When a product launches, automatically create social media posts:

```python
# In Business MCP Server
await client.post("http://localhost:8002/api/flag_marketing_task", json={
    "task_id": "launch_456",
    "content": "New product launch next week",
    "source_domain": "Business"
})
```

#### Personal → Accounting
When travel is booked, automatically record as expense:

```python
# In Personal MCP Server
await client.post("http://localhost:8001/api/record_expense", json={
    "category": "Travel",
    "amount": 500,
    "description": "Business trip to client"
})
```

---

## 📊 Monitoring & Health Checks

### Check Individual Server Health

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
python mcp_server_manager.py health
```

**Output:**
```
======================================================================
MCP SERVER STATUS
======================================================================
Timestamp: 2026-03-10T12:00:00
----------------------------------------------------------------------

Domain          Status       Running    Port     URL
----------------------------------------------------------------------
Accounting      ✅ healthy   Yes        8001     http://localhost:8001
Social Media    ✅ healthy   Yes        8002     http://localhost:8002
Personal        ✅ healthy   Yes        8003     http://localhost:8003
Business        ✅ healthy   Yes        8004     http://localhost:8004
```

---

## 🔧 Troubleshooting

### Problem: Server Won't Start

**Solution:**
```bash
# Check if port is in use
netstat -ano | findstr :8001

# Kill the process or change port
taskkill /F /PID <process_id>
```

---

### Problem: Health Check Fails

**Solution:**
```bash
# Check server logs
type logs\accounting_log.md
type logs\social_log.md

# Restart server
python mcp_server_manager.py stop
python mcp_server_manager.py start
```

---

### Problem: Cross-Domain Communication Fails

**Solution:**
1. Ensure both servers are running
2. Check firewall settings
3. Verify correct ports in configuration
4. Check CORS settings

---

## 📁 File Structure

```
AI Employee Vault [Gold]/
├── mcp_server.py                      # Base MCP server
├── mcp_server_manager.py              # Server manager
├── accounting_mcp_server.py           # Accounting domain server
├── social_mcp_server_v2.py            # Social media domain server
├── personal_mcp_server.py             # Personal domain server
├── business_mcp_server.py             # Business domain server
├── mcp_config/
│   ├── mcp_server_config.json        # Base config
│   ├── accounting_mcp_config.json    # Accounting config
│   ├── social_mcp_config.json        # Social config
│   ├── personal_mcp_config.json      # Personal config
│   └── business_mcp_config.json      # Business config
├── logs/
│   ├── accounting_log.md             # Accounting logs
│   ├── social_log.md                 # Social logs
│   ├── personal_log.md               # Personal logs
│   └── business_log.md               # Business logs
└── MULTI_MCP_SERVERS.md              # This documentation
```

---

## ✅ Verification Checklist

- [ ] All 4 MCP servers created
- [ ] Each server has unique port
- [ ] Configuration files created
- [ ] Health endpoints working
- [ ] Cross-domain integration implemented
- [ ] Documentation complete
- [ ] All servers can start/stop independently
- [ ] Manager can control all servers

---

## 🎉 Summary

Your multi-MCP server architecture is complete with:

- **4 Domain-Specific Servers** (Accounting, Social, Personal, Business)
- **Centralized Management** via `mcp_server_manager.py`
- **Cross-Domain Integration** for complex workflows
- **Health Monitoring** for all servers
- **Independent Scaling** - each domain can scale separately

**Ready for production use!** 🚀
