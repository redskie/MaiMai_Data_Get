"""
Flask API for MaiMai Player Data
Production-ready API server for Render.com deployment
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Configuration
COOKIE_FILE = "cookies.json"
SESSION_TIMEOUT = timedelta(hours=6)  # Re-login after 6 hours
last_login_time = None
login_lock = threading.Lock()

# Load credentials from environment variables
SEGA_ID = os.environ.get('SEGA_ID')
PASSWORD = os.environ.get('PASSWORD')

def load_cookies():
    """Load cookies from file"""
    if not os.path.exists(COOKIE_FILE):
        return None
    
    try:
        with open(COOKIE_FILE, 'r') as f:
            cookie_data = json.load(f)
            
        if isinstance(cookie_data, list):
            cookies = {}
            for cookie in cookie_data:
                cookies[cookie['name']] = cookie['value']
            return cookies
        else:
            return cookie_data
    except Exception as e:
        print(f"Error loading cookies: {e}")
        return None

def save_cookies(cookies):
    """Save cookies to file"""
    try:
        cookie_list = []
        for name, value in cookies.items():
            cookie_list.append({
                'name': name,
                'value': value,
                'domain': '.maimaidx-eng.com',
                'path': '/',
                'secure': False,
                'httpOnly': False
            })
        
        with open(COOKIE_FILE, 'w') as f:
            json.dump(cookie_list, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving cookies: {e}")
        return False

def check_session_valid():
    """Check if current session is still valid"""
    cookies = load_cookies()
    if not cookies:
        return False
    
    try:
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.maimaidx-eng.com', path='/')
        
        response = session.get('https://maimaidx-eng.com/maimai-mobile/', timeout=10)
        
        if "login" in response.url.lower() or "auth" in response.url.lower():
            return False
        
        return response.status_code == 200 and "maimaidx-eng.com" in response.url
    except:
        return False

def perform_login():
    """Perform automated login using pure requests (no browser needed)"""
    global last_login_time
    
    print("Starting automated login with requests...")
    
    try:
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
        
        # Step 1: Get login page
        print("[1/3] Fetching login page...")
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
            print(f"Failed to fetch login page: {initial_response.status_code}")
            return False
        
        # Step 2: Parse form and submit credentials
        print("[2/3] Submitting credentials...")
        soup = BeautifulSoup(initial_response.text, 'html.parser')
        form = soup.find('form')
        
        if not form:
            print("Could not find login form")
            return False
        
        login_data = {
            'retention': '1',
            'sid': SEGA_ID,
            'password': PASSWORD
        }
        
        form_action = form.get('action', '/common_auth/login/sid/')
        if not form_action.startswith('http'):
            form_action = 'https://lng-tgk-aime-gw.am-all.net' + form_action
        
        login_response = session.post(
            form_action,
            data=login_data,
            allow_redirects=True,
            timeout=15
        )
        
        # Step 3: Check if login successful
        print("[3/3] Verifying login...")
        if 'maimaidx-eng.com' in login_response.url:
            print("Login successful - reached MaiMai site!")
            
            # Extract and save cookies
            cookie_list = []
            for cookie in session.cookies:
                cookie_list.append({
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path if cookie.path else '/',
                    'secure': cookie.secure if hasattr(cookie, 'secure') else False,
                    'httpOnly': cookie.has_nonstandard_attr('HttpOnly') if hasattr(cookie, 'has_nonstandard_attr') else False
                })
            
            save_cookies(cookie_list)
            last_login_time = datetime.now()
            
            print(f"Saved {len(cookie_list)} cookies")
            return True
        else:
            print(f"Login failed - ended at: {login_response.url}")
            return False
            
    except Exception as e:
        print(f"Login error: {e}")
        return False

def ensure_logged_in():
    """Ensure we have a valid session, login if needed"""
    global last_login_time
    
    with login_lock:
        # Check if we need to re-login
        if last_login_time and datetime.now() - last_login_time < SESSION_TIMEOUT:
            if check_session_valid():
                return True
        
        # Need to login
        return perform_login()

def get_player_data(friend_code):
    """Fetch player data from MaiMai"""
    cookies = load_cookies()
    if not cookies:
        return {"success": False, "error": "No session available"}
    
    url = f"https://maimaidx-eng.com/maimai-mobile/friend/search/searchUser/?friendCode={friend_code}"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    
    for name, value in cookies.items():
        session.cookies.set(name, value, domain='.maimaidx-eng.com', path='/')
    
    try:
        response = session.get(url, timeout=10, allow_redirects=True)
        
        if "login" in response.url.lower() or "auth" in response.url.lower():
            return {"success": False, "error": "Session expired"}
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        name_element = soup.find('div', class_='name_block')
        player_name = name_element.text.strip() if name_element else "Unknown"
        
        rating_element = soup.find('div', class_='rating_block')
        rating = rating_element.text.strip() if rating_element else "N/A"
        
        return {
            "success": True,
            "friend_code": friend_code,
            "name": player_name,
            "rating": rating
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# API Routes

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "MaiMai Player Data API",
        "version": "1.0.0",
        "endpoints": {
            "player_data": "/api/player/<friend_code>",
            "health": "/health",
            "login": "/api/login"
        }
    })

@app.route('/health')
def health():
    """Detailed health check"""
    session_valid = check_session_valid()
    return jsonify({
        "status": "healthy",
        "session_valid": session_valid,
        "last_login": last_login_time.isoformat() if last_login_time else None
    })

@app.route('/api/login', methods=['POST'])
def api_login():
    """Force re-login endpoint"""
    success = perform_login()
    if success:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "error": "Login failed"}), 500

@app.route('/api/player/<friend_code>')
def api_player(friend_code):
    """Get player data by friend code"""
    
    # Validate friend code
    if not friend_code or not friend_code.isdigit():
        return jsonify({
            "success": False,
            "error": "Invalid friend code format"
        }), 400
    
    # Ensure we're logged in
    if not ensure_logged_in():
        return jsonify({
            "success": False,
            "error": "Failed to authenticate"
        }), 500
    
    # Get player data
    result = get_player_data(friend_code)
    
    # If session expired, try to re-login once
    if not result["success"] and "expired" in result.get("error", "").lower():
        if perform_login():
            result = get_player_data(friend_code)
    
    if result["success"]:
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/api/batch', methods=['POST'])
def api_batch():
    """Get data for multiple friend codes"""
    data = request.get_json()
    
    if not data or 'friend_codes' not in data:
        return jsonify({
            "success": False,
            "error": "Missing friend_codes in request body"
        }), 400
    
    friend_codes = data['friend_codes']
    
    if not isinstance(friend_codes, list) or len(friend_codes) == 0:
        return jsonify({
            "success": False,
            "error": "friend_codes must be a non-empty array"
        }), 400
    
    if len(friend_codes) > 10:
        return jsonify({
            "success": False,
            "error": "Maximum 10 friend codes per request"
        }), 400
    
    # Ensure logged in
    if not ensure_logged_in():
        return jsonify({
            "success": False,
            "error": "Failed to authenticate"
        }), 500
    
    # Fetch all player data
    results = []
    for code in friend_codes:
        result = get_player_data(code)
        results.append(result)
    
    return jsonify({
        "success": True,
        "count": len(results),
        "results": results
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

# Initialize on startup
if __name__ == '__main__':
    print("Starting MaiMai API Server...")
    print(f"SEGA ID: {SEGA_ID}")
    
    # Try to login on startup
    print("Performing initial login...")
    if perform_login():
        print("Initial login successful!")
    else:
        print("Initial login failed - will retry on first request")
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
