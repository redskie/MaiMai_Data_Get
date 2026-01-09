"""
MaiMai Login without Selenium - Pure requests approach
This eliminates the need for Chrome/ChromeDriver
"""

import requests
from bs4 import BeautifulSoup
import json
import time

def login_with_requests(sega_id, password):
    """
    Login to MaiMai using pure requests (no browser needed)
    
    Args:
        sega_id: SEGA ID username
        password: SEGA ID password
        
    Returns:
        dict: Cookies if successful, None if failed
    """
    
    print("Starting login with requests (no browser)...")
    
    # Create session to persist cookies
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    try:
        # Step 1: Get login page to establish session
        print("[1/4] Fetching login page...")
        login_params = {
            'site_id': 'maimaidxex',
            'redirect_url': 'https://maimaidx-eng.com/maimai-mobile/',
            'back_url': 'https://maimai.sega.com/'
        }
        
        initial_response = session.get(
            'https://lng-tgk-aime-gw.am-all.net/common_auth/login',
            params=login_params,
            timeout=15
        )
        
        if initial_response.status_code != 200:
            print(f"❌ Failed to fetch login page: {initial_response.status_code}")
            return None
        
        # Step 2: Parse any hidden fields or tokens
        soup = BeautifulSoup(initial_response.text, 'html.parser')
        form = soup.find('form')
        
        if not form:
            print("❌ Could not find login form")
            return None
        
        # Step 3: Submit login credentials
        print("[2/4] Submitting credentials...")
        
        login_data = {
            'retention': '1',
            'sid': sega_id,
            'password': password
        }
        
        # Get form action URL
        form_action = form.get('action', '/common_auth/login/sid/')
        if not form_action.startswith('http'):
            form_action = 'https://lng-tgk-aime-gw.am-all.net' + form_action
        
        # Submit login form
        login_response = session.post(
            form_action,
            data=login_data,
            allow_redirects=True,
            timeout=15
        )
        
        print(f"    Response status: {login_response.status_code}")
        print(f"    Final URL: {login_response.url}")
        
        # Step 4: Check if we reached MaiMai site
        if 'maimaidx-eng.com' in login_response.url:
            print("[3/4] ✅ Reached MaiMai site!")
            
            # Step 5: Make sure we get MaiMai cookies by accessing the home page
            print("[4/5] Fetching MaiMai home page for cookies...")
            maimai_response = session.get(
                'https://maimaidx-eng.com/maimai-mobile/',
                timeout=15
            )
            
            print(f"    Status: {maimai_response.status_code}")
            
            # Extract ALL cookies from the session (including from different domains)
            cookie_list = []
            for cookie in session.cookies:
                # Only keep MaiMai-related cookies
                if 'maimaidx' in cookie.domain or 'am-all.net' in cookie.domain:
                    cookie_list.append({
                        'name': cookie.name,
                        'value': cookie.value,
                        'domain': cookie.domain,
                        'path': cookie.path if cookie.path else '/',
                        'secure': cookie.secure if hasattr(cookie, 'secure') else False,
                        'httpOnly': cookie.has_nonstandard_attr('HttpOnly') if hasattr(cookie, 'has_nonstandard_attr') else False
                    })
            
            print(f"[5/5] Got {len(cookie_list)} cookies")
            for c in cookie_list:
                print(f"    - {c['name']}: domain={c['domain']}")
            
            print("✅ Login successful!")
            return cookie_list
            
        else:
            print(f"❌ Login failed - did not reach MaiMai")
            print(f"    Ended at: {login_response.url}")
            
            # Check for error messages
            soup = BeautifulSoup(login_response.text, 'html.parser')
            error = soup.find('div', class_='error') or soup.find('p', class_='error-message')
            if error:
                print(f"    Error message: {error.text.strip()}")
            
            return None
            
    except requests.Timeout:
        print("❌ Request timed out")
        return None
    except Exception as e:
        print(f"❌ Error during login: {str(e)}")
        return None

def save_cookies(cookies, filename='cookies.json'):
    """Save cookies to file"""
    try:
        with open(filename, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"💾 Cookies saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to save cookies: {e}")
        return False

def test_session(cookies):
    """Test if cookies work"""
    print("\nTesting session...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Set cookies
    for cookie in cookies:
        session.cookies.set(
            cookie['name'],
            cookie['value'],
            domain=cookie['domain'],
            path=cookie['path']
        )
    
    # Try to access MaiMai home
    try:
        response = session.get('https://maimaidx-eng.com/maimai-mobile/', timeout=10)
        
        if response.status_code == 200 and 'login' not in response.url.lower():
            print("✅ Session is valid!")
            return True
        else:
            print("❌ Session expired or invalid")
            return False
    except Exception as e:
        print(f"❌ Error testing session: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  MaiMai Login - No Browser Required")
    print("="*60 + "\n")
    
    SEGA_ID = "trid001"
    PASSWORD = "104625140040Aaa"
    
    # Attempt login
    cookies = login_with_requests(SEGA_ID, PASSWORD)
    
    if cookies:
        # Save cookies
        save_cookies(cookies)
        
        # Test session
        test_session(cookies)
        
        print("\n" + "="*60)
        print("✅ SUCCESS - Can use requests instead of Selenium!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ FAILED - May need additional work")
        print("="*60)
