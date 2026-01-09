"""
Test script to analyze MaiMai login flow without browser
We'll try to replicate the authentication using pure requests
"""

import requests
from bs4 import BeautifulSoup
import json

# SEGA Authentication URL
LOGIN_URL = "https://lng-tgk-aime-gw.am-all.net/common_auth/login"
CALLBACK_URL = "https://maimaidx-eng.com/maimai-mobile/"

def analyze_login_flow():
    """Analyze the login flow to understand required parameters"""
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    })
    
    print("="*60)
    print("Analyzing MaiMai Login Flow")
    print("="*60)
    
    # Step 1: Get initial login page
    print("\n[1] Fetching login page...")
    params = {
        'site_id': 'maimaidxex',
        'redirect_url': 'https://maimaidx-eng.com/maimai-mobile/',
        'back_url': 'https://maimai.sega.com/'
    }
    
    response = session.get(LOGIN_URL, params=params, allow_redirects=True)
    print(f"    Status: {response.status_code}")
    print(f"    Final URL: {response.url}")
    
    # Parse the page to find form fields
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for form
    form = soup.find('form')
    if form:
        print(f"\n[2] Found form: {form.get('action')}")
        print(f"    Method: {form.get('method')}")
        
        # Find all input fields
        inputs = form.find_all('input')
        print(f"\n[3] Form fields found:")
        for inp in inputs:
            name = inp.get('name', 'N/A')
            input_type = inp.get('type', 'text')
            value = inp.get('value', '')
            print(f"    - {name}: type={input_type}, value={value[:50] if value else 'empty'}")
    
    # Check for any hidden tokens or CSRF
    hidden_inputs = soup.find_all('input', {'type': 'hidden'})
    print(f"\n[4] Hidden fields:")
    for inp in hidden_inputs:
        print(f"    - {inp.get('name')}: {inp.get('value', '')[:50]}")
    
    # Save cookies
    print(f"\n[5] Cookies received:")
    for cookie in session.cookies:
        print(f"    - {cookie.name}: {cookie.value[:50]}")
    
    return session, response

def attempt_login_with_requests(sega_id, password):
    """Attempt to login using pure requests (no browser)"""
    
    print("\n" + "="*60)
    print("Attempting Login with Requests Library")
    print("="*60)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    
    # Try to access the SEGA ID login directly
    print("\n[1] Accessing SEGA ID login...")
    
    # This might be the actual SEGA ID login endpoint
    sega_login_url = "https://id.sega.jp/idp/Authn/Login"
    
    # Try to post credentials
    login_data = {
        'sid': sega_id,
        'password': password,
        # We might need additional fields like tokens
    }
    
    print(f"[2] Posting credentials to SEGA ID...")
    try:
        response = session.post(sega_login_url, data=login_data, allow_redirects=True)
        print(f"    Status: {response.status_code}")
        print(f"    Final URL: {response.url}")
        
        # Check if we got redirected to MaiMai
        if 'maimaidx-eng.com' in response.url:
            print("\n✅ Successfully reached MaiMai site!")
            
            # Save cookies
            cookies = session.cookies.get_dict()
            print(f"\n[3] Cookies obtained: {len(cookies)} cookies")
            for name, value in cookies.items():
                print(f"    - {name}")
            
            return True, session.cookies
        else:
            print(f"\n❌ Did not reach MaiMai site")
            print(f"    Stuck at: {response.url}")
            return False, None
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False, None

if __name__ == "__main__":
    print("\n🔍 MaiMai Login Flow Analyzer\n")
    
    # First, analyze the flow
    session, response = analyze_login_flow()
    
    print("\n\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("1. Review the form fields above")
    print("2. Identify required fields for login")
    print("3. Try to replicate login with requests library")
    print("\nPress Enter to continue with login attempt...")
    input()
    
    # Attempt login
    SEGA_ID = "trid001"
    PASSWORD = "104625140040Aaa"
    
    success, cookies = attempt_login_with_requests(SEGA_ID, PASSWORD)
    
    if success:
        print("\n✅ Login successful! Can proceed without Selenium.")
    else:
        print("\n❌ Login failed. May need to analyze further.")
