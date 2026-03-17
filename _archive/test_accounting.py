"""
Test script for Accounting MCP Server
"""
import httpx
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Check ===")
    response = httpx.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_authentication():
    """Test if Odoo connection is working"""
    print("\n=== Testing Odoo Connection ===")
    # Try to fetch partners (should work if authenticated)
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                "odoo_db",  # Database name from .env
                2,  # UID (admin typically)
                "admin",  # Password from .env
                "res.partner",
                "search_read",
                [[]],  # No domain - get all
                {"fields": ["name"], "limit": 5}
            ]
        },
        "id": 1
    }
    
    try:
        response = httpx.post("http://localhost:8069/jsonrpc", json=payload)
        result = response.json()
        print(f"Direct Odoo Response: {json.dumps(result, indent=2)}")
        
        if 'error' in result:
            print("[FAIL] Authentication failed - check credentials in .env")
            return False
        elif 'result' in result:
            print(f"[OK] Connected to Odoo! Found {len(result['result'])} partners")
            return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False

def test_create_invoice():
    """Test creating an invoice"""
    print("\n=== Testing Create Invoice ===")
    payload = {
        "partner_id": 1,
        "product_ids": [1],
        "quantities": [1.0],
        "prices": [100.0],
        "reference": "TEST-INV-001"
    }
    
    response = httpx.post(f"{BASE_URL}/create_invoice", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

if __name__ == "__main__":
    print("=" * 60)
    print("ACCOUNTING MCP SERVER - TEST SUITE")
    print("=" * 60)
    
    # Test 1: Health
    health_ok = test_health()
    
    # Test 2: Direct Odoo connection
    odoo_ok = test_authentication()
    
    # Test 3: Create invoice (only if Odoo connected)
    if odoo_ok:
        invoice_ok = test_create_invoice()
    else:
        print("\n[WARN] Skipping invoice test - Odoo not connected")
        invoice_ok = False
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Health Check:      {'[OK] PASS' if health_ok else '[FAIL] FAIL'}")
    print(f"Odoo Connection:   {'[OK] PASS' if odoo_ok else '[FAIL] FAIL'}")
    print(f"Create Invoice:    {'[OK] PASS' if invoice_ok else '[FAIL] FAIL'}")
    print("=" * 60)
