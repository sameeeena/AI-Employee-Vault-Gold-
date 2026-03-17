# 🏦 Odoo Accounting - Quick Start Guide

## ✅ Current Status

| Component | Status | Details |
|-----------|--------|---------|
| Odoo 19+ Running | ✅ YES | Port 8069 |
| Database | ✅ YES | `odoo_db` |
| Authentication | ✅ YES | UID: 2 |
| MCP Server | ✅ YES | Port 8000 |
| **Accounting Module** | ❌ **NEEDS INSTALL** | Install from Apps menu |

---

## 📦 Step: Install Accounting Module

### **1. Open Odoo Apps**
I've already opened it in your browser. If not, go to:
```
http://localhost:8069/web/apps
```

### **2. Login**
- **Email**: `sameena02134@gmail.com`
- **Password**: `admin`

### **3. Search & Install**
1. In the Apps search bar, type: **Invoicing**
2. Find the **"Invoicing"** app (by Odoo)
3. Click the **"Install"** button
4. Wait 30-60 seconds for installation

### **4. Verify**
After installation:
- You should see an **"Invoicing"** menu in the top bar
- Click it to see the accounting dashboard

---

## 🚀 Start Accounting MCP Server

### **Using Batch File:**
```bash
start_accounting.bat
```

### **Manual:**
```bash
# Set credentials
set ODOO_USERNAME=sameena02134@gmail.com
set ODOO_PASSWORD=admin

# Start server
python accounting_mcp_server.py
```

Server will start on: `http://localhost:8000`

---

## 🧪 Test the System

### **1. Check Health**
```bash
curl http://localhost:8000/health
```

### **2. Run Test Suite**
```bash
python test_accounting.py
```

### **3. Check Modules**
```bash
python check_odoo_modules.py
```

---

## 📡 API Endpoints (After Accounting Module is Installed)

### Create Invoice
```bash
curl -X POST http://localhost:8000/create_invoice ^
  -H "Content-Type: application/json" ^
  -d "{\"partner_id\": 9, \"product_ids\": [1], \"quantities\": [1.0], \"prices\": [100.0]}"
```

### Record Expense
```bash
curl -X POST http://localhost:8000/record_expense ^
  -H "Content-Type: application/json" ^
  -d "{\"partner_id\": 9, \"product_id\": 1, \"quantity\": 1.0, \"price_unit\": 50.0, \"account_id\": 1}"
```

### Get Profit & Loss
```bash
curl -X POST http://localhost:8000/fetch_profit_loss ^
  -H "Content-Type: application/json" ^
  -d "{\"date_from\": \"2026-01-01\", \"date_to\": \"2026-03-04\"}"
```

---

## 🔧 Commands Reference

| Command | Description |
|---------|-------------|
| `start_accounting.bat` | Start MCP server with correct credentials |
| `accounting.bat` | Show help for accounting commands |
| `python check_odoo_modules.py` | Check installed Odoo modules |
| `python test_accounting.py` | Run test suite |

---

## 📝 What Happens After Installing Accounting Module

Once you install the **Invoicing** app:

1. **New models available**:
   - `account.move` - Invoices, Bills, Journal Entries
   - `account.journal` - Sales, Purchase, Bank journals
   - `account.account` - Chart of accounts
   - `account.payment.term` - Payment terms

2. **MCP Server endpoints will work**:
   - ✅ `/create_invoice` - Create customer invoices
   - ✅ `/record_expense` - Record vendor bills
   - ✅ `/fetch_profit_loss` - Get P&L statement
   - ✅ `/fetch_balance_sheet` - Get balance sheet

3. **Sample data** (optional):
   - Go to Settings → Developers → Load Demo Data
   - Or create manual: Customers, Products, Journals

---

## 🎯 Next Steps

1. **[ ] Install Invoicing app** (see above)
2. **[ ] Restart MCP server** after installation
3. **[ ] Run test suite** to verify
4. **[ ] Create first test invoice**

---

## 🔐 Credentials

| System | Username | Password |
|--------|----------|----------|
| Odoo Login | `sameena02134@gmail.com` | `admin` |
| Database | `openpg` | `openpgpwd` |
| MCP Server Config | `sameena02134@gmail.com` | `admin` |

---

## 📚 Documentation

- `ODOO_ACCOUNTING_SETUP.md` - Full setup guide
- `accounting_mcp_server.py` - Server source code
- `test_accounting.py` - Test suite
- `check_odoo_modules.py` - Module checker

---

**Last Updated:** 2026-03-04  
**Status:** 🟡 Waiting for Accounting Module Installation
