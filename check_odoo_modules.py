"""
Check Odoo Modules
Check which modules are installed in Odoo
"""
import httpx
import json

URL = "http://localhost:8069"
DB = "odoo_db"
USERNAME = "sameena02134@gmail.com"
PASSWORD = "admin"

def authenticate():
    """Authenticate and get UID"""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "common",
            "method": "authenticate",
            "args": [DB, USERNAME, PASSWORD, {}]
        },
        "id": 1
    }
    response = httpx.post(f"{URL}/jsonrpc", json=payload)
    result = response.json()
    return result.get('result')

def check_module(uid, module_name):
    """Check if a module is installed"""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                DB, uid, PASSWORD,
                "ir.module.module",
                "search_read",
                [[('name', '=', module_name)]],
                {"fields": ["name", "state", "latest_version"]}
            ]
        },
        "id": 2
    }
    response = httpx.post(f"{URL}/jsonrpc", json=payload)
    result = response.json()
    return result.get('result', [])

def check_model(uid, model_name):
    """Check if a model exists"""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "object",
            "method": "execute_kw",
            "args": [
                DB, uid, PASSWORD,
                "ir.model",
                "search_read",
                [[('model', '=', model_name)]],
                {"fields": ["model", "name"]}
            ]
        },
        "id": 3
    }
    response = httpx.post(f"{URL}/jsonrpc", json=payload)
    result = response.json()
    return result.get('result', [])

if __name__ == "__main__":
    print("=" * 60)
    print("ODOO MODULE CHECK")
    print("=" * 60)
    
    uid = authenticate()
    if not uid:
        print("[FAIL] Authentication failed!")
        exit(1)
    
    print(f"[OK] Authenticated as UID: {uid}")
    print()
    
    # Check accounting modules
    print("Checking accounting modules...")
    modules = ['account', 'account_invoice', 'invoicing', 'account_accountant']
    for module in modules:
        result = check_module(uid, module)
        if result:
            state = result[0].get('state', 'unknown')
            version = result[0].get('latest_version', 'N/A')
            print(f"  {module}: {state} (v{version})")
        else:
            print(f"  {module}: NOT FOUND")
    
    print()
    
    # Check accounting models
    print("Checking accounting models...")
    models = ['account.move', 'account.invoice', 'account.journal', 'account.account']
    for model in models:
        result = check_model(uid, model)
        if result:
            print(f"  {model}: EXISTS ({result[0].get('name', 'N/A')})")
        else:
            print(f"  {model}: NOT FOUND")
    
    print()
    print("=" * 60)
    print("RECOMMENDATION:")
    print("=" * 60)
    print("1. Go to: http://localhost:8069")
    print("2. Login with: sameena02134@gmail.com / admin")
    print("3. Go to Apps menu")
    print("4. Search for 'Invoicing' or 'Accounting'")
    print("5. Click 'Install' on the Invoicing app")
    print("=" * 60)
