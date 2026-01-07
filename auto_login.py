"""
Automated login script that interacts with the MaiMai website organically.
Performs the exact login sequence: SEGA ID button -> credentials -> checkbox -> login
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time

def automated_login(sega_id, password, headless=False):
    """
    Performs automated login to MaiMai DX website.
    
    Args:
        sega_id (str): Your SEGA ID
        password (str): Your password
        headless (bool): Run browser in headless mode (invisible)
    
    Returns:
        bool: True if login successful, False otherwise
    """
    driver = None
    
    try:
        # Setup Edge browser
        print("=== MaiMai DX Automated Login ===\n")
        print("Starting Edge browser...")
        
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        
        # Performance optimizations
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--dns-prefetch-disable')
        options.page_load_strategy = 'eager'  # Don't wait for all resources
        
        driver = webdriver.Edge(options=options)
        wait = WebDriverWait(driver, 10)  # Reduced from 20 to 10 seconds
        
        # Step 1: Navigate to login page and wait for it to fully load
        login_url = "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/"
        print(f"\n[Step 1] Navigating to login page...")
        driver.get(login_url)
        
        print("  ⏳ Waiting for page to load...")
        time.sleep(1.5)  # Reduced from 3 to 1.5 seconds
        
        # Step 2: Click "SEGA ID" button to expand the login form
        print("\n[Step 2] Looking for 'SEGA ID' button...")
        try:
            # The SEGA ID button is a span inside an accordion
            sega_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "span.c-button--openid--segaId")
            ))
            
            print("  ✓ Found SEGA ID button")
            print("  👆 Clicking to expand login form...")
            sega_button.click()
            time.sleep(0.8)  # Reduced from 2 to 0.8 seconds for accordion
            
        except Exception as e:
            print(f"  ⚠ Could not click SEGA ID button: {e}")
            print("  → The form may already be expanded")
        
        # Step 3: Enter SEGA ID and password
        print("\n[Step 3] Entering credentials...")
        
        # Find SEGA ID input field by ID
        print("  📝 Looking for SEGA ID input field...")
        try:
            sega_id_input = wait.until(EC.presence_of_element_located(
                (By.ID, "sid")
            ))
            print("  ✓ Found SEGA ID field (id='sid')")
            sega_id_input.clear()
            print(f"  ⌨️  Typing SEGA ID: {sega_id}")
            sega_id_input.send_keys(sega_id)
            time.sleep(0.2)  # Reduced from 0.5 to 0.2 seconds
        except Exception as e:
            print(f"  ✗ Could not find SEGA ID input: {e}")
            return False
        
        # Find password input field by ID
        print("  📝 Looking for password input field...")
        try:
            password_input = wait.until(EC.presence_of_element_located(
                (By.ID, "password")
            ))
            print("  ✓ Found password field (id='password')")
            password_input.clear()
            print("  ⌨️  Typing password: " + "*" * len(password))
            password_input.send_keys(password)
            time.sleep(0.2)  # Reduced from 0.5 to 0.2 seconds
        except Exception as e:
            print(f"  ✗ Could not find password input: {e}")
            return False
        
        # Step 4: Tick the terms of service checkbox
        print("\n[Step 4] Looking for terms of service checkbox...")
        try:
            # Wait for the form to be visible
            time.sleep(0.3)  # Reduced from 1 to 0.3 seconds
            
            # The checkbox has id="agree" inside div#agree-maimaidxex
            # There are multiple elements with id="agree", we need the visible one
            checkboxes = driver.find_elements(By.ID, "agree")
            
            checkbox_clicked = False
            for checkbox in checkboxes:
                try:
                    # Check if checkbox is visible and not already checked
                    if checkbox.is_displayed() and not checkbox.is_selected():
                        print("  ✓ Found terms checkbox")
                        print("  ☑️  Ticking terms of service checkbox...")
                        # Try to click with JavaScript in case it's hidden by label
                        driver.execute_script("arguments[0].click();", checkbox)
                        checkbox_clicked = True
                        time.sleep(0.2)  # Reduced from 0.5 to 0.2 seconds
                        break
                except:
                    continue
            
            if not checkbox_clicked:
                # Try clicking the label instead
                try:
                    label = driver.find_element(By.CSS_SELECTOR, "label.c-form__label--bg.agree")
                    if label.is_displayed():
                        print("  ✓ Found terms checkbox label")
                        print("  ☑️  Clicking terms checkbox via label...")
                        label.click()
                        checkbox_clicked = True
                        time.sleep(0.2)  # Reduced from 0.5 to 0.2 seconds
                except:
                    pass
            
            if checkbox_clicked:
                print("  ✓ Checkbox ticked successfully")
            else:
                print("  ⚠ Could not tick checkbox - may already be checked")
        
        except Exception as e:
            print(f"  ⚠ Could not tick checkbox: {e}")
            print("  → Continuing anyway")
        
        # Step 5: Click Login button
        print("\n[Step 5] Looking for Login button...")
        try:
            login_button = wait.until(EC.element_to_be_clickable(
                (By.ID, "btnSubmit")
            ))
            
            if login_button:
                print("  ✓ Found Login button (id='btnSubmit')")
                print("  👆 Clicking Login button...")
                login_button.click()
                
                # Wait for navigation
                print("\n  ⏳ Waiting for login to complete...")
                time.sleep(2.5)  # Reduced from 5 to 2.5 seconds
                
                # Check if we're on the maimai page
                current_url = driver.current_url
                print(f"\n  Current URL: {current_url}")
                
                if "maimaidx-eng.com" in current_url:
                    print("\n✅ LOGIN SUCCESSFUL!")
                    
                    # Capture cookies with full details
                    print("\n💾 Saving session cookies...")
                    cookies = driver.get_cookies()
                    
                    # Save full cookie details (needed for proper session management)
                    cookie_list = []
                    for cookie in cookies:
                        cookie_list.append({
                            'name': cookie['name'],
                            'value': cookie['value'],
                            'domain': cookie.get('domain', ''),
                            'path': cookie.get('path', '/'),
                            'secure': cookie.get('secure', False),
                            'httpOnly': cookie.get('httpOnly', False),
                            'expiry': cookie.get('expiry', None)
                        })
                    
                    with open('cookies.json', 'w') as f:
                        json.dump(cookie_list, f, indent=2)
                    
                    print(f"  ✓ Saved {len(cookie_list)} cookies with full attributes")
                    print("\n  Key cookies captured:")
                    for cookie in cookie_list:
                        if cookie['domain'] and 'maimai' in cookie['domain'].lower():
                            print(f"    - {cookie['name']} (domain: {cookie['domain']})")
                    
                    # Keep browser open briefly
                    print("\n✓ You can now use get_player_data.py")
                    time.sleep(1)  # Reduced from 3 to 1 second
                    
                    return True
                else:
                    print("\n⚠ May not have logged in successfully")
                    print("  Check the browser window for any errors")
                    input("  Press Enter to close browser...")
                    return False
            else:
                print("  ✗ Could not find Login button")
                return False
                
        except Exception as e:
            print(f"  ✗ Error clicking login: {e}")
            return False
        
    except Exception as e:
        print(f"\n✗ Error during login: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print("\nClosing browser...")
            time.sleep(1)  # Reduced from 2 to 1 second
            driver.quit()

if __name__ == "__main__":
    # Your credentials
    SEGA_ID = "trid001"
    PASSWORD = "104625140040Aaa"
    
    print("Starting automated login with your credentials...\n")
    
    success = automated_login(SEGA_ID, PASSWORD, headless=False)
    
    if success:
        print("\n" + "="*60)
        print("✅ LOGIN COMPLETE!")
        print("="*60)
        print("\nYou can now run:")
        print("  python get_player_data.py")
        print("\nTo fetch player data using any friend code.")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ LOGIN FAILED")
        print("="*60)
        print("\nPlease check:")
        print("  - Your credentials are correct")
        print("  - The website is accessible")
        print("  - Your internet connection")
        print("="*60)
