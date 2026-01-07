"""
Parse any webpage to extract forms, inputs, buttons, and other elements.
Generates a unique HTML file for each URL parsed.
Automatically handles MaiMai authentication if needed.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import os

def sanitize_filename(url):
    """Create a safe filename from URL"""
    # Extract domain and path
    clean = re.sub(r'https?://', '', url)
    clean = re.sub(r'[^\w\-_\.]', '_', clean)
    # Truncate if too long
    if len(clean) > 50:
        clean = clean[:50]
    return clean

def is_maimai_url(url):
    """Check if URL is MaiMai-related"""
    maimai_keywords = ['maimaidx', 'maimai', 'lng-tgk-aime-gw.am-all.net']
    url_lower = url.lower()
    return any(keyword in url_lower for keyword in maimai_keywords)

def load_maimai_cookies():
    """Load MaiMai authentication cookies if available"""
    cookie_file = "cookies.json"
    
    if not os.path.exists(cookie_file):
        print("\n⚠️  WARNING: MaiMai-related URL detected but no cookies found!")
        print("   You need to login first. Run:")
        print("     python auto_login.py")
        print("\n   Attempting to fetch without authentication (may fail)...\n")
        return None
    
    try:
        with open(cookie_file, 'r') as f:
            cookie_data = json.load(f)
            
            # Handle both formats: list of cookie objects or simple dict
            if isinstance(cookie_data, list):
                cookies = {}
                for cookie in cookie_data:
                    cookies[cookie['name']] = cookie['value']
                return cookies
            else:
                return cookie_data
    except Exception as e:
        print(f"⚠️  Error loading cookies: {e}")
        return None

def parse_webpage(url):
    """Fetch and parse a webpage to extract element details"""
    
    print("="*60)
    print("WEBPAGE PARSER")
    print("="*60)
    print(f"\nTarget URL: {url}")
    
    # Check if MaiMai-related and load cookies if needed
    cookies = None
    session = requests.Session()
    
    if is_maimai_url(url):
        print("✓ Detected MaiMai-related URL")
        print("  Loading authentication cookies...")
        cookies = load_maimai_cookies()
        
        if cookies:
            print(f"  ✓ Loaded {len(cookies)} cookies")
            # Set cookies in session
            for name, value in cookies.items():
                session.cookies.set(name, value, domain='.maimaidx-eng.com', path='/')
        else:
            print("  ⚠️  No cookies loaded - proceeding without authentication")
    
    print(f"\nFetching page...\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        session.headers.update(headers)
        response = session.get(url, timeout=10, allow_redirects=True)
        
        # Check if redirected to login page
        if "login" in response.url.lower() or "auth" in response.url.lower():
            print("⚠️  REDIRECTED TO LOGIN PAGE!")
            print("   Your session has expired. Please run:")
            print("     python auto_login.py")
            print("\n   Continuing to parse login page...\n")
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("="*60)
        print("FORMS FOUND:")
        print("="*60)
        
        forms = soup.find_all('form')
        if forms:
            for i, form in enumerate(forms, 1):
                print(f"\n[Form {i}]")
                print(f"  Action: {form.get('action', 'N/A')}")
                print(f"  Method: {form.get('method', 'N/A')}")
                print(f"  ID: {form.get('id', 'N/A')}")
                print(f"  Class: {form.get('class', 'N/A')}")
                
                # Find all inputs
                inputs = form.find_all('input')
                if inputs:
                    print(f"\n  Inputs found:")
                    for inp in inputs:
                        inp_type = inp.get('type', 'text')
                        inp_id = inp.get('id', 'N/A')
                        inp_name = inp.get('name', 'N/A')
                        inp_class = inp.get('class', 'N/A')
                        inp_value = inp.get('value', '')
                        
                        print(f"    - Type: {inp_type}")
                        print(f"      ID: {inp_id}")
                        print(f"      Name: {inp_name}")
                        print(f"      Class: {inp_class}")
                        if inp_value:
                            print(f"      Value: {inp_value}")
                        print()
                
                # Find buttons
                buttons = form.find_all('button')
                if buttons:
                    print(f"  Buttons found:")
                    for btn in buttons:
                        btn_type = btn.get('type', 'N/A')
                        btn_id = btn.get('id', 'N/A')
                        btn_name = btn.get('name', 'N/A')
                        btn_class = btn.get('class', 'N/A')
                        btn_text = btn.get_text(strip=True)
                        
                        print(f"    - Type: {btn_type}")
                        print(f"      ID: {btn_id}")
                        print(f"      Name: {btn_name}")
                        print(f"      Class: {btn_class}")
                        print(f"      Text: {btn_text}")
                        print()
        else:
            print("  No forms found on page")
        
        print("\n" + "="*60)
        print("CHECKBOXES FOUND:")
        print("="*60)
        
        checkboxes = soup.find_all('input', {'type': 'checkbox'})
        if checkboxes:
            for i, checkbox in enumerate(checkboxes, 1):
                print(f"\n[Checkbox {i}]")
                print(f"  ID: {checkbox.get('id', 'N/A')}")
                print(f"  Name: {checkbox.get('name', 'N/A')}")
                print(f"  Class: {checkbox.get('class', 'N/A')}")
                print(f"  Value: {checkbox.get('value', 'N/A')}")
                
                # Find associated label
                label = None
                if checkbox.get('id'):
                    label = soup.find('label', {'for': checkbox.get('id')})
                if label:
                    print(f"  Label: {label.get_text(strip=True)[:100]}")
        else:
            print("  No checkboxes found on page")
        
        print("\n" + "="*60)
        print("ALL BUTTONS FOUND:")
        print("="*60)
        
        all_buttons = soup.find_all('button')
        if all_buttons:
            for i, btn in enumerate(all_buttons, 1):
                print(f"\n[Button {i}]")
                print(f"  Tag: button")
                print(f"  ID: {btn.get('id', 'N/A')}")
                print(f"  Class: {btn.get('class', 'N/A')}")
                print(f"  Type: {btn.get('type', 'N/A')}")
                print(f"  Text: {btn.get_text(strip=True)[:50]}")
        else:
            print("  No buttons found on page")
        
        print("\n" + "="*60)
        print("DIVS WITH CLASSES (TOP 20):")
        print("="*60)
        
        divs = soup.find_all('div', class_=True)[:20]
        if divs:
            for i, div in enumerate(divs, 1):
                div_class = ' '.join(div.get('class', []))
                div_id = div.get('id', 'N/A')
                div_text = div.get_text(strip=True)[:50]
                print(f"\n[Div {i}]")
                print(f"  Class: {div_class}")
                print(f"  ID: {div_id}")
                print(f"  Text: {div_text}")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        url_slug = sanitize_filename(url)
        filename = f"parsed_{url_slug}_{timestamp}.html"
        
        # Save full HTML for inspection
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print("\n" + "="*60)
        print(f"✓ Full HTML saved to: {filename}")
        print("="*60)
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error fetching URL: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error parsing page: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n=== Website Parser ===\n")
    print("This tool parses any webpage and extracts:")
    print("  - Forms (action, method, inputs, buttons)")
    print("  - Checkboxes")
    print("  - All buttons")
    print("  - Divs with classes")
    print("  - Saves full HTML to a unique file\n")
    
    url = input("Enter URL to parse: ").strip()
    
    if not url:
        print("Error: URL cannot be empty!")
    elif not url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
    else:
        parse_webpage(url)
