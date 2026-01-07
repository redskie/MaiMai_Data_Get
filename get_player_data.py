import requests
from bs4 import BeautifulSoup
import json
import os

def load_cookies(cookie_file="cookies.json"):
    """
    Load cookies from JSON file and convert to requests format.
    
    Args:
        cookie_file (str): Path to the cookie file
        
    Returns:
        dict: Cookies formatted for requests library
    """
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r') as f:
            cookie_data = json.load(f)
            
            # Handle both formats: list of cookie objects or simple dict
            if isinstance(cookie_data, list):
                # New format with full cookie attributes
                cookies = {}
                for cookie in cookie_data:
                    cookies[cookie['name']] = cookie['value']
                return cookies
            else:
                # Old format: simple dict
                return cookie_data
    return {}

def get_player_rating(friend_code, cookies=None):
    """
    Fetch player's basic data from MaiMai DX using their friend code.
    
    Args:
        friend_code (str): The player's MaiMai friend code
        cookies (dict): Authentication cookies (optional)
        
    Returns:
        dict: Player data including name and rating
    """
    # Construct the URL with the friend code
    url = f"https://maimaidx-eng.com/maimai-mobile/friend/search/searchUser/?friendCode={friend_code}"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    # Set headers to mimic a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    # Load cookies if provided
    if cookies:
        # Convert cookies to proper format for requests
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.maimaidx-eng.com', path='/')
    
    try:
        # Make GET request with session
        response = session.get(url, allow_redirects=True)
        
        # Check if we got redirected to login (means cookies expired)
        if "login" in response.url.lower() or "auth" in response.url.lower():
            return {
                "success": False,
                "error": "Authentication failed - cookies may have expired. Please run auto_login.py again."
            }
        
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract player name
        name_element = soup.find('div', class_='name_block')
        player_name = name_element.text.strip() if name_element else "Unknown"
        
        # Extract rating from rating_block class
        rating_element = soup.find('div', class_='rating_block')
        rating = rating_element.text.strip() if rating_element else "N/A"
        
        return {
            "success": True,
            "friend_code": friend_code,
            "name": player_name,
            "rating": rating
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error parsing data: {str(e)}"
        }

def main():
    print("=== MaiMai DX Player Data Fetcher ===\n")
    
    # Try to load existing cookies
    cookies = load_cookies()
    
    if not cookies:
        print("❌ No cookies found!")
        print("\nYou need to login first. Run:")
        print("  python auto_login.py")
        print("\nThis will login and save your session cookies automatically.")
        return
    else:
        print(f"✓ Loaded {len(cookies)} cookies from cookies.json")
    
    # Get friend code from user
    friend_code = input("\nEnter MaiMai Friend Code: ").strip()
    
    if not friend_code:
        print("Error: Friend code cannot be empty!")
        return
    
    print(f"\nFetching data for friend code: {friend_code}...")
    
    # Get player data
    result = get_player_rating(friend_code, cookies)
    
    # Display results
    if result["success"]:
        print("\n=== Player Data ===")
        print(f"Friend Code: {result['friend_code']}")
        print(f"Name: {result['name']}")
        print(f"Rating: {result['rating']}")
    else:
        print(f"\n❌ Error: {result['error']}")
        if "auth" in result['error'].lower() or "expired" in result['error'].lower():
            print("\n💡 Tip: Your session has expired. Run:")
            print("  python auto_login.py")
            print("\nto login again and refresh your cookies.")

if __name__ == "__main__":
    main()
