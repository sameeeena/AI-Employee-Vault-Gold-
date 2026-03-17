"""
Social MCP Server Test Script
Tests Facebook and Instagram integration
"""
import httpx
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://localhost:8001"

def check_credentials():
    """Check if credentials are configured"""
    print("\n" + "=" * 60)
    print("  CHECKING CREDENTIALS")
    print("=" * 60)
    
    creds = {
        'FACEBOOK_APP_ID': os.getenv('FACEBOOK_APP_ID'),
        'FACEBOOK_APP_SECRET': os.getenv('FACEBOOK_APP_SECRET'),
        'FACEBOOK_ACCESS_TOKEN': os.getenv('FACEBOOK_ACCESS_TOKEN'),
        'FACEBOOK_PAGE_ID': os.getenv('FACEBOOK_PAGE_ID'),
        'INSTAGRAM_ACCESS_TOKEN': os.getenv('INSTAGRAM_ACCESS_TOKEN'),
        'INSTAGRAM_USER_ID': os.getenv('INSTAGRAM_USER_ID')
    }
    
    all_present = True
    for key, value in creds.items():
        if value:
            masked = value[:10] + '...' if len(value) > 10 else value
            print(f"  [OK] {key}: {masked}")
        else:
            print(f"  [MISSING] {key}")
            all_present = False
    
    return all_present

def test_health():
    """Test health endpoint"""
    print("\n" + "=" * 60)
    print("  TEST 1: HEALTH CHECK")
    print("=" * 60)
    
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=10)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        if response.status_code == 200:
            print("  [OK] Server is healthy")
            return True
        else:
            print("  [FAIL] Server returned error")
            return False
    except Exception as e:
        print(f"  [FAIL] Could not connect: {e}")
        print("  Make sure server is running: python social_mcp_server.py")
        return False

def test_facebook_post():
    """Test Facebook post"""
    print("\n" + "=" * 60)
    print("  TEST 2: FACEBOOK POST")
    print("=" * 60)
    
    payload = {
        "platform": "facebook",
        "message": f"Test post from AI Employee - {os.getenv('COMPUTERNAME', 'TEST')}"
    }
    
    try:
        response = httpx.post(f"{BASE_URL}/post_message", json=payload, timeout=30)
        result = response.json()
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print(f"  [OK] Facebook post created! ID: {result['data']['post_id']}")
            return result['data']['post_id']
        else:
            print(f"  [FAIL] {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return None

def test_instagram_post():
    """Test Instagram post"""
    print("\n" + "=" * 60)
    print("  TEST 3: INSTAGRAM POST")
    print("=" * 60)
    
    # Use a placeholder image
    payload = {
        "platform": "instagram",
        "message": f"Test post from AI Employee - {os.getenv('COMPUTERNAME', 'TEST')}",
        "image_url": "https://via.placeholder.com/600x400.png?text=Test+Image"
    }
    
    try:
        response = httpx.post(f"{BASE_URL}/post_message", json=payload, timeout=30)
        result = response.json()
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print(f"  [OK] Instagram post created! ID: {result['data']['post_id']}")
            return result['data']['post_id']
        else:
            print(f"  [FAIL] {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return None

def test_engagement_metrics(post_id, platform='facebook'):
    """Test engagement metrics"""
    print("\n" + "=" * 60)
    print(f"  TEST 4: ENGAGEMENT METRICS ({platform})")
    print("=" * 60)
    
    if not post_id:
        print("  [SKIP] No post ID provided")
        return None
    
    payload = {
        "platform": platform,
        "post_id": post_id
    }
    
    try:
        response = httpx.post(f"{BASE_URL}/fetch_engagement_metrics", json=payload, timeout=30)
        result = response.json()
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(result, indent=2)[:500]}")
        
        if result.get('success'):
            print(f"  [OK] Metrics retrieved successfully")
            return result['data']
        else:
            print(f"  [WARN] {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return None

def test_summary(post_id, platform='facebook'):
    """Test summary generation"""
    print("\n" + "=" * 60)
    print(f"  TEST 5: GENERATE SUMMARY ({platform})")
    print("=" * 60)
    
    if not post_id:
        print("  [SKIP] No post ID provided")
        return None
    
    payload = {
        "platform": platform,
        "post_id": post_id
    }
    
    try:
        response = httpx.post(f"{BASE_URL}/generate_post_summary", json=payload, timeout=30)
        result = response.json()
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print(f"  [OK] Summary generated successfully")
            return result['data']
        else:
            print(f"  [WARN] {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"  [FAIL] Error: {e}")
        return None

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("   SOCIAL MEDIA MCP SERVER - TEST SUITE")
    print("=" * 70)
    
    # Check credentials first
    creds_ok = check_credentials()
    
    if not creds_ok:
        print("\n" + "=" * 70)
        print("  [WARNING] Some credentials are missing!")
        print("  Please update .env file with Facebook/Instagram credentials")
        print("  See: SOCIAL_MEDIA_QUICKSTART.md for setup guide")
        print("=" * 70)
        proceed = input("\nContinue with tests anyway? (y/n): ")
        if proceed.lower() != 'y':
            exit(0)
    
    # Run tests
    results = []
    
    # Test 1: Health
    health_ok = test_health()
    results.append(("Health Check", health_ok))
    
    if not health_ok:
        print("\n[ERROR] Server not running. Start with: python social_mcp_server.py")
        exit(1)
    
    # Test 2: Facebook Post
    fb_post_id = test_facebook_post()
    results.append(("Facebook Post", fb_post_id is not None))
    
    # Test 3: Instagram Post
    ig_post_id = test_instagram_post()
    results.append(("Instagram Post", ig_post_id is not None))
    
    # Wait a moment for engagement data to populate
    if fb_post_id or ig_post_id:
        print("\n[INFO] Waiting 5 seconds for engagement data...")
        import time
        time.sleep(5)
        
        # Test 4: Engagement Metrics (Facebook)
        if fb_post_id:
            metrics = test_engagement_metrics(fb_post_id, 'facebook')
            results.append(("Facebook Metrics", metrics is not None))
            
            # Test 5: Summary (Facebook)
            if metrics:
                summary = test_summary(fb_post_id, 'facebook')
                results.append(("Facebook Summary", summary is not None))
    
    # Summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[OK] PASS" if result else "[FAIL]"
        print(f"  {status} - {name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    print("=" * 70)
    
    if passed == total:
        print("\n  [SUCCESS] All tests passed! Social media integration is working!")
    else:
        print(f"\n  [WARNING] {total - passed} test(s) need attention")
        print("  Check credentials in .env file")
        print("  See: SOCIAL_MEDIA_SETUP.md for troubleshooting")
    
    print("=" * 70 + "\n")
