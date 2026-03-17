"""
Direct Facebook Live Post Test - No user input required
"""

import httpx
import json
import sys
import os
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul')
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("FACEBOOK LIVE POSTING TEST")
print("=" * 70)
print()

# Test message
message = f"Hello from AI Employee Vault! Testing live Facebook post at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} #TestPost #FacebookIntegration"

print(f"Message: {message}")
print()
print("Posting to Facebook...")
print("-" * 70)

try:
    # Post to Facebook via MCP Server
    response = httpx.post(
        "http://localhost:8002/api/post_message",
        json={
            "platform": "facebook",
            "message": message
        },
        timeout=30.0
    )
    
    result = response.json()
    
    print()
    print("RESPONSE:")
    print(json.dumps(result, indent=2, default=str))
    print()
    
    if result.get("success"):
        print("SUCCESS! Facebook post published!")
        print()
        data = result.get("data", {})
        print(f"   Post ID: {data.get('post_id')}")
        print(f"   Timestamp: {data.get('timestamp')}")
        print()
        print("Check your Facebook Page to see the post!")
    else:
        print("FAILED! Post was not published.")
        print(f"   Error: {result.get('error', 'Unknown error')}")
        
except httpx.TimeoutException:
    print("TIMEOUT! Request timed out.")
except Exception as e:
    print(f"ERROR: {str(e)}")

print()
print("=" * 70)
print("Test completed!")
print("=" * 70)
