# 🏦 Odoo Accounting MCP Integration

## 📋 Overview

This system integrates with **Odoo Community 19+** (self-hosted, local) via an MCP server using Odoo's JSON-RPC APIs to perform accounting operations.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACCOUNTING INTEGRATION                        │
└─────────────────────────────────────────────────────────────────┘

Your Commands (CLI)
        ↓
accounting.bat
        ↓
Accounting MCP Server (FastAPI)
        ↓
Odoo JSON-RPC API
        ↓
Odoo Community 19+ (Local)
        ↓
PostgreSQL Database
```

---

## 📦 Prerequisites

### 1. **Odoo Community 19+** (Self-hosted)

#### Option A: Docker (Recommended)
```bash
# Install Docker Desktop: https://www.docker.com/products/docker-desktop/

# Pull and run Odoo 19
docker pull odoo:19.0
docker run -p 8069:8069 --name odoo -d odoo:19.0
```

#### Option B: Windows Installer
1. Download: https://github.com/odoo/odoo/releases/tag/19.0
2. Download PostgreSQL: https://www.postgresql.org/download/windows/
3. Run Odoo installer
4. Start Odoo service

---

### 2. **Configure Odoo Database**

1. **Access Odoo**: `http://localhost:8069`
2. **Login**:
   - Email: `sameena02134@gmail.com`
   - Password: `admin`
3. **Install Accounting Module** (REQUIRED):
   - Click **"Apps"** in the top menu (or go to `http://localhost:8069/web/apps`)
   - In the search bar, type: **Invoicing**
   - Find **"Invoicing"** app (by Odoo)
   - Click **"Install"** button
   - Wait for installation to complete
   
   **Alternative**: Install **"Accounting"** (full-featured, enterprise)
   - Search for: **Accounting**
   - Click **"Install"**

4. **Verify Installation**:
   - After installation, you should see:
     - **Invoicing** menu (or **Accounting** menu)
     - Dashboard with financial metrics

---

### 3. **Python Dependencies**

```bash
pip install -r requirements.txt
```

Required packages:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `httpx` - Async HTTP client
- `pydantic` - Data validation
- `aiofiles` - Async file operations

---

## 🚀 Quick Start

### **Step 1: Start Odoo**
```bash
# If using Docker
docker start odoo

# If using Windows installer
# Odoo should auto-start as a service
```

### **Step 2: Verify Odoo is Running**
```bash
# Open browser: http://localhost:8069
# Or use curl:
curl http://localhost:8069
```

### **Step 3: Update `.env` File**

Ensure these are set correctly:
```env
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
```

### **Step 4: Start Accounting MCP Server**
```bash
accounting start
```

Or directly:
```bash
python accounting_mcp_server.py
```

Server will start on: `http://localhost:8000`

---

## 📡 API Endpoints

### **1. Health Check**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{"status": "healthy", "timestamp": "2026-03-04T..."}
```

---

### **2. Create Invoice**
```bash
curl -X POST http://localhost:8000/create_invoice ^
  -H "Content-Type: application/json" ^
  -d "{\"partner_id\": 1, \"product_ids\": [1], \"quantities\": [1.0], \"prices\": [100.0], \"reference\": \"INV-001\"}"
```

**Response:**
```json
{
  "success": true,
  "data": {"invoice_id": 123},
  "request_id": "abc123"
}
```

---

### **3. Record Expense**
```bash
curl -X POST http://localhost:8000/record_expense ^
  -H "Content-Type: application/json" ^
  -d "{\"partner_id\": 1, \"product_id\": 1, \"quantity\": 1.0, \"price_unit\": 50.0, \"account_id\": 1, \"reference\": \"EXP-001\"}"
```

**Response:**
```json
{
  "success": true,
  "data": {"expense_id": 456},
  "request_id": "def456"
}
```

---

### **4. Fetch Profit & Loss**
```bash
curl -X POST http://localhost:8000/fetch_profit_loss ^
  -H "Content-Type: application/json" ^
  -d "{\"date_from\": \"2026-01-01\", \"date_to\": \"2026-03-04\"}"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "period": "2026-01-01 to 2026-03-04",
    "total_income": 10000.0,
    "total_expenses": 5000.0,
    "net_profit": 5000.0,
    "income_details": [...],
    "expense_details": [...]
  }
}
```

---

### **5. Fetch Balance Sheet**
```bash
curl -X POST http://localhost:8000/fetch_balance_sheet ^
  -H "Content-Type: application/json" ^
  -d "{\"date_from\": \"2026-01-01\", \"date_to\": \"2026-03-04\"}"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "as_of_date": "2026-03-04",
    "total_assets": 50000.0,
    "total_liabilities": 20000.0,
    "total_equity": 30000.0,
    "assets_details": [...],
    "liabilities_details": [...],
    "equity_details": [...]
  }
}
```

---

## 🔧 Commands

| Command | Description |
|---------|-------------|
| `accounting start` | Start the Accounting MCP Server |
| `accounting test` | Test API endpoints |
| `accounting status` | Check server health |

---

## 📝 Logging

All API calls are logged to: `logs/accounting_log.md`

Log includes:
- Request timestamp
- Model and method called
- Request parameters
- Response data
- Errors (if any)

---

## 🔐 Authentication Flow

1. Server starts → Authenticates with Odoo
2. Gets UID (user ID) from Odoo
3. Uses UID for all subsequent API calls
4. Auto-re-authenticates if session expires

---

## 🧪 Testing

### Full Test Flow:
```bash
# 1. Start Odoo (Docker)
docker start odoo

# 2. Start Accounting MCP Server
accounting start

# 3. In another terminal, test health
accounting status

# 4. Test create invoice
curl -X POST http://localhost:8000/create_invoice ^
  -H "Content-Type: application/json" ^
  -d "{\"partner_id\": 1, \"product_ids\": [1], \"quantities\": [1.0], \"prices\": [100.0]}"

# 5. Check logs
type logs\accounting_log.md
```

---

## 📊 Odoo Models Used

| Model | Purpose |
|-------|---------|
| `account.move` | Invoices, Expenses, Journal Entries |
| `account.move.line` | Invoice/Expense line items |
| `account.account` | Chart of accounts |
| `res.partner` | Customers/Vendors |
| `product.product` | Products/Services |

---

## 🛠️ Troubleshooting

### **Odoo Connection Failed**
```bash
# Check if Odoo is running
docker ps | findstr odoo

# Or check port 8069
netstat -an | findstr 8069
```

### **Authentication Failed**
- Verify credentials in `.env`
- Check Odoo database name
- Reset Odoo admin password if needed

### **Module Not Found**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### **Invoice Creation Fails**
- Ensure partner exists in Odoo: `res.partner` model
- Ensure products exist: `product.product` model
- Check Odoo logs for detailed errors

---

## 🔗 Integration with Existing System

The Accounting MCP Server can be integrated with your existing automation:

### Example: Email → Accounting Task
```
Email received → Orchestrator → Accounting MCP → Odoo Invoice
```

### Example: WhatsApp → Expense Report
```
WhatsApp message → Orchestrator → Accounting MCP → Odoo Expense
```

---

## 📚 Additional Resources

- **Odoo JSON-RPC Docs**: https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html
- **Odoo Community**: https://www.odoo.com/forum/community-1
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---

## ✅ Setup Checklist

- [ ] Odoo 19+ installed and running
- [ ] Database `odoo_db` created
- [ ] Accounting/Invoicing module installed
- [ ] `.env` credentials updated
- [ ] Python dependencies installed
- [ ] Accounting MCP Server starts successfully
- [ ] Health check endpoint responds
- [ ] Test invoice created successfully
- [ ] Logs are being written

---

**Last Updated:** 2026-03-04  
**Status:** 🟡 Ready for Setup  
**Version:** 1.0.0
