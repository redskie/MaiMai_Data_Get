"""
Simple test client for MaiMai Data API
Send test requests and display responses
"""

import requests
import json
import time
import sys

# API Configuration
BASE_URL = "https://maimai-data-get.onrender.com"

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_request(friend_code):
    """Send a test request to the API"""
    print_header(f"Testing Friend Code: {friend_code}")
    
    print(f"📤 Sending request to: {BASE_URL}/api/player/{friend_code}")
    print("⏳ Waiting for response...\n")
    
    try:
        start_time = time.time()
        
        response = requests.get(
            f"{BASE_URL}/api/player/{friend_code}",
            timeout=120
        )
        
        elapsed = time.time() - start_time
        
        # Print response details
        print(f"⏱️  Response time: {elapsed:.2f}s")
        print(f"📊 Status Code: {response.status_code}")
        print(f"\n📄 Response Body:")
        print("-" * 60)
        
        try:
            data = response.json()
            print(json.dumps(data, indent=2))
            
            # Pretty print if successful
            if data.get('success'):
                print("\n" + "="*60)
                print("✅ SUCCESS!")
                print(f"👤 Player Name: {data.get('name')}")
                print(f"⭐ Rating: {data.get('rating')}")
                print("="*60)
            else:
                print("\n" + "="*60)
                print(f"❌ ERROR: {data.get('error')}")
                print("="*60)
                
        except json.JSONDecodeError:
            print(response.text)
            print("\n❌ Response is not valid JSON")
        
        return response.status_code == 200
        
    except requests.Timeout:
        print("❌ Request timed out (>120 seconds)")
        return False
    except requests.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return False
    except KeyboardInterrupt:
        print("\n\n⚠️  Request cancelled by user")
        return False

def test_health():
    """Test the health endpoint"""
    print_header("Health Check")
    
    try:
        print(f"📤 Checking: {BASE_URL}/health")
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"\n📄 Response:")
        print("-" * 60)
        print(json.dumps(response.json(), indent=2))
        print()
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

def main():
    """Main function"""
    print("\n" + "="*60)
    print("  MaiMai Data API - Test Client")
    print("="*60)
    
    if len(sys.argv) > 1:
        # Use friend code from command line
        friend_code = sys.argv[1]
        test_request(friend_code)
    else:
        # Interactive mode
        print("\nOptions:")
        print("1. Test friend code: 101232330856982")
        print("2. Test friend code: 101680566000997")
        print("3. Enter custom friend code")
        print("4. Health check")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            test_request("101232330856982")
        elif choice == "2":
            test_request("101680566000997")
        elif choice == "3":
            custom_code = input("Enter friend code: ").strip()
            if custom_code:
                test_request(custom_code)
            else:
                print("❌ Invalid friend code")
        elif choice == "4":
            test_health()
        elif choice == "5":
            print("Goodbye!")
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
