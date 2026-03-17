"""
Create Invoice in Odoo and Fetch Profit & Loss Statement

This script:
1. Creates a sample customer invoice in Odoo
2. Fetches the Profit & Loss statement
"""

import httpx
import json
from datetime import datetime

# Odoo Configuration
ODOO_URL = "http://localhost:8069"
ODOO_DB = "odoo_db"
ODOO_USERNAME = "sameena02134@gmail.com"
ODOO_PASSWORD = "admin"

# Accounting MCP Server
MCP_SERVER_URL = "http://localhost:8000"


def authenticate_odoo():
    """Authenticate with Odoo and get UID"""
    url = f"{ODOO_URL}/jsonrpc"
    
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "common",
            "method": "authenticate",
            "args": [ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {}]
        },
        "id": 1
    }
    
    try:
        response = httpx.post(url, json=payload)
        result = response.json()
        
        if 'result' in result and result['result']:
            uid = result['result']
            print(f"✅ Authentication successful! UID: {uid}")
            return uid
        else:
            print("❌ Authentication failed")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def get_or_create_partner():
    """Get or create a customer partner"""
    url = f"{ODOO_URL}/jsonrpc"
    
    # First, try to find existing partner
    search_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                ODOO_DB,
                2,  # uid
                ODOO_PASSWORD,
                "res.partner",
                "search_read",
                [[["name", "=", "Test Customer"]]],
                {"limit": 1}
            ]
        },
        "id": 2
    }
    
    try:
        response = httpx.post(url, json=search_payload)
        result = response.json()
        
        if result.get('result'):
            partner = result['result'][0]
            print(f"✅ Found existing partner: {partner['name']} (ID: {partner['id']})")
            return partner['id']
        
        # Create new partner if not found
        create_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB,
                    2,
                    ODOO_PASSWORD,
                    "res.partner",
                    "create",
                    [{
                        "name": "Test Customer",
                        "company_type": "company",
                        "email": "customer@example.com",
                        "phone": "+1234567890"
                    }]
                ]
            },
            "id": 3
        }
        
        response = httpx.post(url, json=create_payload)
        result = response.json()
        
        if result.get('result'):
            partner_id = result['result']
            print(f"✅ Created new partner with ID: {partner_id}")
            return partner_id
            
    except Exception as e:
        print(f"❌ Error getting/creating partner: {str(e)}")
    
    return None


def get_or_create_product():
    """Get or create a product"""
    url = f"{ODOO_URL}/jsonrpc"
    
    # First, try to find existing product
    search_payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                ODOO_DB,
                2,
                ODOO_PASSWORD,
                "product.product",
                "search_read",
                [[["name", "=", "Consulting Services"]]],
                {"limit": 1}
            ]
        },
        "id": 4
    }
    
    try:
        response = httpx.post(url, json=search_payload)
        result = response.json()
        
        if result.get('result'):
            product = result['result'][0]
            print(f"✅ Found existing product: {product['name']} (ID: {product['id']})")
            return product['id']
        
        # Create new product if not found
        create_payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB,
                    2,
                    ODOO_PASSWORD,
                    "product.product",
                    "create",
                    [{
                        "name": "Consulting Services",
                        "type": "service",
                        "list_price": 100.0,
                        "standard_price": 50.0,
                        "uom_name": "Hours"
                    }]
                ]
            },
            "id": 5
        }
        
        response = httpx.post(url, json=create_payload)
        result = response.json()
        
        if result.get('result'):
            product_id = result['result']
            print(f"✅ Created new product with ID: {product_id}")
            return product_id
            
    except Exception as e:
        print(f"❌ Error getting/creating product: {str(e)}")
    
    return None


def create_invoice_via_mcp(partner_id, product_id):
    """Create invoice using Accounting MCP Server"""
    url = f"{MCP_SERVER_URL}/create_invoice"
    
    payload = {
        "partner_id": partner_id,
        "product_ids": [product_id],
        "quantities": [5.0],  # 5 hours
        "prices": [150.0],    # $150 per hour
        "reference": f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    }
    
    print(f"\n📝 Creating invoice...")
    print(f"   Partner ID: {partner_id}")
    print(f"   Product ID: {product_id}")
    print(f"   Quantity: 5.0 hours")
    print(f"   Price: $150.00/hour")
    print(f"   Total: $750.00")
    
    try:
        response = httpx.post(url, json=payload, timeout=30)
        result = response.json()
        
        print(f"\n{'✅' if result.get('success') else '❌'} Invoice Creation Result:")
        print(json.dumps(result, indent=2))
        
        if result.get('success'):
            invoice_id = result.get('data', {}).get('invoice_id')
            print(f"\n🎉 Invoice created successfully! ID: {invoice_id}")
            return invoice_id
        else:
            print(f"\n❌ Invoice creation failed: {result.get('error')}")
            return None
            
    except httpx.ConnectError:
        print(f"\n❌ Cannot connect to MCP Server at {MCP_SERVER_URL}")
        print("   Make sure the Accounting MCP Server is running:")
        print("   python accounting_mcp_server.py")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def fetch_profit_loss(date_from, date_to):
    """Fetch Profit & Loss statement from MCP Server"""
    url = f"{MCP_SERVER_URL}/fetch_profit_loss"
    
    payload = {
        "date_from": date_from,
        "date_to": date_to
    }
    
    print(f"\n📊 Fetching Profit & Loss Statement...")
    print(f"   Period: {date_from} to {date_to}")
    
    try:
        response = httpx.post(url, json=payload, timeout=30)
        result = response.json()
        
        print(f"\n{'✅' if result.get('success') else '❌'} Profit & Loss Result:")
        
        if result.get('success'):
            data = result.get('data', {})
            print(f"""
╔══════════════════════════════════════════════════════════╗
║              PROFIT & LOSS STATEMENT                      ║
╠══════════════════════════════════════════════════════════╣
║  Period: {data.get('period', 'N/A'):<46} ║
╠══════════════════════════════════════════════════════════╣
║  Total Income:    ${data.get('total_income', 0):>12,.2f}                      ║
║  Total Expenses:  ${data.get('total_expenses', 0):>12,.2f}                      ║
╠══════════════════════════════════════════════════════════╣
║  NET PROFIT:      ${data.get('net_profit', 0):>12,.2f}                      ║
╠══════════════════════════════════════════════════════════╣
║  Transactions:    {data.get('moves_count', 0):>12}                        ║
╚══════════════════════════════════════════════════════════╝
""")
            
            # Show recent moves
            moves = data.get('moves_summary', [])
            if moves:
                print("\n📋 Recent Transactions:")
                for move in moves[:5]:
                    print(f"   - {move.get('name', 'N/A')} | Date: {move.get('date', 'N/A')} | "
                          f"Type: {move.get('move_type', 'N/A')} | Amount: ${move.get('amount_total', 0):,.2f}")
        else:
            print(f"\n❌ Failed to fetch P&L: {result.get('error')}")
            
        return result
        
    except httpx.ConnectError:
        print(f"\n❌ Cannot connect to MCP Server at {MCP_SERVER_URL}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    print("=" * 60)
    print("  ODOO ACCOUNTING - CREATE INVOICE & PROFIT/LOSS")
    print("=" * 60)
    
    # Step 1: Authenticate with Odoo
    print("\n🔐 Step 1: Authenticating with Odoo...")
    uid = authenticate_odoo()
    
    if not uid:
        print("\n❌ Cannot authenticate with Odoo!")
        print("   Check your credentials in .env file:")
        print(f"   ODOO_URL={ODOO_URL}")
        print(f"   ODOO_DB={ODOO_DB}")
        print(f"   ODOO_USERNAME={ODOO_USERNAME}")
        print("\n   Make sure Odoo is running on port 8069")
        return
    
    # Step 2: Get or create partner
    print("\n👤 Step 2: Getting/Creating customer...")
    partner_id = get_or_create_partner()
    
    if not partner_id:
        print("\n❌ Could not get/create partner")
        return
    
    # Step 3: Get or create product
    print("\n📦 Step 3: Getting/Creating product...")
    product_id = get_or_create_product()
    
    if not product_id:
        print("\n❌ Could not get/create product")
        return
    
    # Step 4: Create invoice via MCP Server
    print("\n💰 Step 4: Creating Invoice...")
    invoice_id = create_invoice_via_mcp(partner_id, product_id)
    
    # Step 5: Fetch Profit & Loss
    print("\n📈 Step 5: Fetching Profit & Loss Statement...")
    today = datetime.now().strftime('%Y-%m-%d')
    first_day_of_year = f"{datetime.now().year}-01-01"
    fetch_profit_loss(first_day_of_year, today)
    
    print("\n" + "=" * 60)
    print("  DONE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
