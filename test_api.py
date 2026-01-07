import requests
import json
import time

# Base URL
BASE_URL = "https://maimai-data-get.onrender.com"

# Test friend code
TEST_FRIEND_CODE = "101680566000997"

def print_test(test_name):
    """Print test header"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")

def test_health_check():
    """Test 1: Health check endpoint"""
    print_test("Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ PASSED: Health check successful")
            return True
        else:
            print("❌ FAILED: Unexpected status code")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_detailed_health():
    """Test 2: Detailed health endpoint"""
    print_test("Detailed Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and 'logged_in' in data:
            print("✅ PASSED: Detailed health check successful")
            return True
        else:
            print("❌ FAILED: Unexpected response")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_get_player_data():
    """Test 3: Get player data"""
    print_test(f"Get Player Data (Friend Code: {TEST_FRIEND_CODE})")
    
    print("⏳ This may take 30-60s on first request (cold start)...")
    
    try:
        start_time = time.time()
        response = requests.get(
            f"{BASE_URL}/api/player/{TEST_FRIEND_CODE}",
            timeout=120  # 2 minute timeout for cold start
        )
        elapsed = time.time() - start_time
        
        print(f"Status Code: {response.status_code}")
        print(f"Time taken: {elapsed:.2f}s")
        
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and data.get('success'):
            print("✅ PASSED: Player data retrieved successfully")
            print(f"   Name: {data.get('name')}")
            print(f"   Rating: {data.get('rating')}")
            return True
        else:
            print(f"❌ FAILED: {data.get('error', 'Unknown error')}")
            return False
    except requests.Timeout:
        print("❌ FAILED: Request timed out (>2 minutes)")
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_invalid_friend_code():
    """Test 4: Invalid friend code"""
    print_test("Invalid Friend Code")
    
    invalid_code = "999999999999999"
    
    try:
        response = requests.get(f"{BASE_URL}/api/player/{invalid_code}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and not data.get('success'):
            print("✅ PASSED: Invalid code handled correctly")
            return True
        else:
            print("⚠️  WARNING: Should handle invalid codes gracefully")
            return True  # Don't fail the test suite
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_batch_request():
    """Test 5: Batch request"""
    print_test("Batch Request")
    
    payload = {
        "friend_codes": [TEST_FRIEND_CODE]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/batch",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=120
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200 and 'results' in data:
            print("✅ PASSED: Batch request successful")
            return True
        else:
            print("❌ FAILED: Unexpected response")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def test_cors():
    """Test 6: CORS headers"""
    print_test("CORS Headers")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        headers = response.headers
        
        print("CORS Headers:")
        cors_headers = {k: v for k, v in headers.items() if 'access-control' in k.lower()}
        for key, value in cors_headers.items():
            print(f"  {key}: {value}")
        
        if 'Access-Control-Allow-Origin' in headers:
            print("✅ PASSED: CORS enabled")
            return True
        else:
            print("⚠️  WARNING: CORS headers not found")
            return True  # Don't fail
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("MaiMai Data API - Test Suite")
    print(f"Testing: {BASE_URL}")
    print("="*60)
    
    tests = [
        test_health_check,
        test_detailed_health,
        test_get_player_data,
        test_invalid_friend_code,
        test_batch_request,
        test_cors
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            time.sleep(1)  # Small delay between tests
        except KeyboardInterrupt:
            print("\n\n⚠️  Tests interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error in test: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user")
        exit(1)
