"""
MaiMai Data Access Manager
Handles login and provides easy access to all tools
"""

import subprocess
import sys
import os
import json
import requests

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header"""
    print("="*60)
    print(" "*15 + "MaiMai Data Access Manager")
    print("="*60)
    print()

def check_existing_session():
    """Check if there's a valid existing MaiMai session"""
    cookie_file = "cookies.json"
    
    # Check if cookies file exists
    if not os.path.exists(cookie_file):
        return False
    
    try:
        # Load cookies
        with open(cookie_file, 'r') as f:
            cookie_data = json.load(f)
        
        if not cookie_data:
            return False
        
        # Convert cookies to dict format
        cookies = {}
        if isinstance(cookie_data, list):
            for cookie in cookie_data:
                cookies[cookie['name']] = cookie['value']
        else:
            cookies = cookie_data
        
        # Test the session with a simple MaiMai page
        test_url = "https://maimaidx-eng.com/maimai-mobile/"
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        })
        
        # Set cookies
        for name, value in cookies.items():
            session.cookies.set(name, value, domain='.maimaidx-eng.com', path='/')
        
        # Make test request
        response = session.get(test_url, timeout=10, allow_redirects=True)
        
        # If we got redirected to login page, session is invalid
        if "login" in response.url.lower() or "auth" in response.url.lower():
            return False
        
        # If we got a successful response on the maimai domain, session is valid
        if response.status_code == 200 and "maimaidx-eng.com" in response.url:
            return True
        
        return False
        
    except Exception as e:
        # If any error occurs, assume session is invalid
        return False

def run_auto_login():
    """Run the auto login script"""
    print("🔐 Starting MaiMai login process...\n")
    print("-"*60)
    
    try:
        # Run auto_login.py and wait for it to complete
        result = subprocess.run(
            [sys.executable, "auto_login.py"],
            check=False,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print("-"*60)
        
        if result.returncode == 0:
            print("\n✅ Login completed successfully!")
            return True
        else:
            print("\n⚠️  Login process finished with warnings.")
            response = input("\nDo you want to continue anyway? (y/n): ").strip().lower()
            return response == 'y'
            
    except Exception as e:
        print(f"\n❌ Error during login: {e}")
        return False

def show_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("What would you like to do?")
    print("="*60)
    print()
    print("  [1] Get Player Data (by friend code)")
    print("  [2] Parse Webpage (extract elements from any URL)")
    print("  [3] Re-login (refresh authentication)")
    print("  [4] Exit")
    print()

def run_get_player_data():
    """Run the get player data script"""
    clear_screen()
    print_header()
    print("📊 Player Data Fetcher\n")
    print("-"*60)
    
    try:
        subprocess.run(
            [sys.executable, "get_player_data.py"],
            check=False,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    input("\nPress Enter to return to menu...")

def run_parse_webpage():
    """Run the webpage parser script"""
    clear_screen()
    print_header()
    print("🔍 Webpage Parser\n")
    print("-"*60)
    
    try:
        subprocess.run(
            [sys.executable, "parse_webpage.py"],
            check=False,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    input("\nPress Enter to return to menu...")

def main():
    """Main application flow"""
    clear_screen()
    print_header()
    
    # Step 1: Check existing session
    print("Step 1: Checking Authentication Status")
    print("-"*60)
    print("Verifying existing session...\n")
    
    session_valid = check_existing_session()
    
    if session_valid:
        print("✅ Valid session found! Already logged in.")
        print("   Skipping login process...\n")
        login_success = True
    else:
        print("⚠️  No valid session found.")
        print("   Starting login process...\n")
        login_success = run_auto_login()
        
        if not login_success:
            print("\n❌ Cannot proceed without successful authentication.")
            input("\nPress Enter to exit...")
            return
    
    # Step 2: Main menu loop
    while True:
        clear_screen()
        print_header()
        print("✅ Authenticated successfully!")
        show_menu()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            run_get_player_data()
        elif choice == '2':
            run_parse_webpage()
        elif choice == '3':
            clear_screen()
            print_header()
            login_success = run_auto_login()
            if not login_success:
                print("\n⚠️  Re-login failed, but continuing with existing session...")
                input("\nPress Enter to continue...")
        elif choice == '4':
            clear_screen()
            print_header()
            print("👋 Thank you for using MaiMai Data Access Manager!")
            print("\nGoodbye!\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")
