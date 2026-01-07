# How the MaiMai Data API Works
## Complete Project Workflow Explanation

---

## Overview

This project automates fetching player data from the MaiMai DX website using web scraping and provides it through a REST API.

---

## Architecture Diagram

```
┌─────────────────┐
│  User's Website │
│  (GitHub Pages) │
└────────┬────────┘
         │ HTTP Request
         │ GET /api/player/101680566000997
         ▼
┌─────────────────────────┐
│   Flask API Server      │
│   (Render.com)          │
│                         │
│  1. Check Session       │
│  2. Login if needed     │
│  3. Fetch data          │
│  4. Parse HTML          │
│  5. Return JSON         │
└────────┬────────────────┘
         │ Selenium + Cookies
         │
         ▼
┌─────────────────────────┐
│  MaiMai DX Website      │
│  maimaidx-eng.com       │
│                         │
│  (Protected content)    │
└─────────────────────────┘
```

---

## Example Scenario: Fetching Player Data

### Scenario:
A user visits your website and enters friend code `101680566000997` to look up a player.

---

### Step-by-Step Process:

#### **Step 1: User Makes Request**

User's website sends HTTP request:
```javascript
// Frontend JavaScript
fetch('https://maimai-api.onrender.com/api/player/101680566000997')
  .then(response => response.json())
  .then(data => console.log(data));
```

**What happens:**
- Browser sends GET request to your API
- Request includes friend code in URL

---

#### **Step 2: API Receives Request**

Flask receives the request at endpoint:
```python
@app.route('/api/player/<friend_code>')
def api_player(friend_code):
    # friend_code = "101680566000997"
```

**What happens:**
- API validates the friend code format
- Extracts friend code from URL: `101680566000997`
- Checks if it's valid (numbers only)

---

#### **Step 3: Session Check**

API checks if we have valid authentication:
```python
def ensure_logged_in():
    # Check if cookies exist and are still valid
    if check_session_valid():
        return True  # Already logged in!
    else:
        return perform_login()  # Need to login
```

**What happens:**
- Loads `cookies.json` from disk
- Makes test request to MaiMai with cookies
- If redirected to login page → session expired
- If successful → session still valid

**Two paths:**

**Path A: Session Valid ✅**
```
Cookies exist → Test request → Success → Continue to Step 4
```

**Path B: Session Expired ⚠️**
```
Cookies expired → Trigger auto-login → Continue to Step 4
```

---

#### **Step 4: Auto-Login (if needed)**

If session expired, Selenium logs in automatically:

```python
def perform_login():
    # 1. Open headless Chrome browser
    driver = webdriver.Chrome(options=options)
    
    # 2. Navigate to login page
    driver.get("https://lng-tgk-aime-gw.am-all.net/common_auth/login?...")
    
    # 3. Click SEGA ID button
    sega_button.click()
    
    # 4. Enter credentials
    driver.find_element(By.ID, "sid").send_keys("trid001")
    driver.find_element(By.ID, "password").send_keys("password")
    
    # 5. Check terms checkbox
    driver.find_element(By.ID, "agree").click()
    
    # 6. Click login button
    driver.find_element(By.ID, "btnSubmit").click()
    
    # 7. Wait for redirect to MaiMai homepage
    # 8. Extract all cookies from browser
    # 9. Save cookies to cookies.json
    # 10. Close browser
```

**What happens:**
- Chrome opens invisibly (headless mode)
- Navigates through login flow automatically
- Saves authentication cookies
- Takes ~6-8 seconds total

**Timeline:**
```
0s    → Start Chrome
1.5s  → Page loaded
2.3s  → SEGA ID clicked, form expanded
3.0s  → Credentials entered
3.5s  → Checkbox checked
4.0s  → Login clicked
6.5s  → Redirected, cookies saved
7.0s  → Browser closed
```

---

#### **Step 5: Fetch Player Data**

With valid session, fetch the player page:

```python
def get_player_data(friend_code):
    # Build URL
    url = f"https://maimaidx-eng.com/maimai-mobile/friend/search/searchUser/?friendCode={friend_code}"
    
    # Create session with cookies
    session = requests.Session()
    for name, value in cookies.items():
        session.cookies.set(name, value)
    
    # Make authenticated request
    response = session.get(url)
```

**What happens:**
- Constructs URL with friend code: `https://maimaidx-eng.com/maimai-mobile/friend/search/searchUser/?friendCode=101680566000997`
- Attaches authentication cookies to request
- MaiMai website recognizes valid session
- Returns player page HTML

**Example HTML received:**
```html
<div class="name_block">ＢＭＣ☆ＭＡＲＸ</div>
<div class="rating_block">15248</div>
```

---

#### **Step 6: Parse HTML**

Extract player data from HTML:

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')

# Find player name
name_element = soup.find('div', class_='name_block')
player_name = name_element.text.strip()  # "ＢＭＣ☆ＭＡＲＸ"

# Find rating
rating_element = soup.find('div', class_='rating_block')
rating = rating_element.text.strip()  # "15248"
```

**What happens:**
- BeautifulSoup parses HTML into searchable structure
- Finds `<div class="name_block">` → extracts text
- Finds `<div class="rating_block">` → extracts text
- Cleans up whitespace

---

#### **Step 7: Return JSON Response**

API formats data and returns to user:

```python
return jsonify({
    "success": True,
    "friend_code": "101680566000997",
    "name": "ＢＭＣ☆ＭＡＲＸ",
    "rating": "15248"
})
```

**Response sent to user:**
```json
{
  "success": true,
  "friend_code": "101680566000997",
  "name": "ＢＭＣ☆ＭＡＲＸ",
  "rating": "15248"
}
```

---

#### **Step 8: Display to User**

Frontend receives and displays data:

```javascript
// User's website JavaScript
fetch('https://maimai-api.onrender.com/api/player/101680566000997')
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      document.getElementById('playerName').textContent = data.name;
      document.getElementById('rating').textContent = data.rating;
      // Shows: "ＢＭＣ☆ＭＡＲＸ - Rating: 15248"
    }
  });
```

**What user sees:**
```
Player: ＢＭＣ☆ＭＡＲＸ
Rating: 15248
```

---

## Complete Timeline

### First Request (No Session):
```
User Request → API Receives (0s)
              ↓
Check Session → Invalid (0.1s)
              ↓
Auto-Login → Chrome opens → Login flow → Save cookies (6-8s)
              ↓
Fetch Data → Parse HTML (1-2s)
              ↓
Return JSON → User sees result (9-11s total)
```

### Subsequent Requests (Valid Session):
```
User Request → API Receives (0s)
              ↓
Check Session → Valid (0.1s)
              ↓
Fetch Data → Parse HTML (1-2s)
              ↓
Return JSON → User sees result (2-3s total)
```

---

## Key Components Explained

### 1. **Cookies (Session Management)**

**What they are:**
- Small pieces of data that prove you're logged in
- Like a ticket stub that shows you've been admitted

**How we use them:**
- Saved in `cookies.json` after login
- Attached to every request to MaiMai
- Valid for ~6 hours, then re-login needed

**Example cookie:**
```json
{
  "name": "_session_id",
  "value": "abc123xyz789",
  "domain": ".maimaidx-eng.com"
}
```

### 2. **Selenium (Browser Automation)**

**What it is:**
- Controls a real Chrome browser programmatically
- Can click buttons, fill forms, just like a human

**When we use it:**
- Only for logging in (once every 6 hours)
- Not used for fetching player data (too slow)

**Why headless:**
- No visible browser window
- Runs faster on servers
- Lower resource usage

### 3. **BeautifulSoup (HTML Parsing)**

**What it is:**
- Library that understands HTML structure
- Makes finding elements easy

**Example:**
```python
# Without BeautifulSoup (hard):
html.index('<div class="rating_block">') 
# Returns: 12458

# With BeautifulSoup (easy):
soup.find('div', class_='rating_block').text
# Returns: "15248"
```

### 4. **Flask (Web Server)**

**What it is:**
- Lightweight Python web framework
- Handles HTTP requests and responses

**What it does:**
```python
@app.route('/api/player/<code>')  # URL pattern
def handler(code):                # Your function
    return jsonify(data)          # JSON response
```

---

## Error Handling

### Scenario: Session Expired Mid-Request

```
User Request → Check session → Valid ✅
              ↓
Fetch data → Gets redirected to login ❌
              ↓
Detect failure → Auto re-login → Retry fetch ✅
              ↓
Success → Return data
```

### Scenario: Invalid Friend Code

```
User Request: /api/player/abc123 (invalid)
              ↓
Validate → Not all digits ❌
              ↓
Return error: "Invalid friend code format"
```

### Scenario: MaiMai Website Down

```
User Request → Check session → Valid ✅
              ↓
Fetch data → Connection timeout ❌
              ↓
Catch exception → Return error JSON
```

---

## Security & Performance

### Security:
- ✅ Credentials stored as environment variables (not in code)
- ✅ Cookies never exposed to frontend
- ✅ `.gitignore` prevents committing secrets
- ✅ CORS enabled for your domain only

### Performance:
- ⚡ Session cached for 6 hours (no repeated logins)
- ⚡ Direct HTTP requests (fast, no browser overhead)
- ⚡ Optimized login flow (6-8s instead of 15s)
- ⚡ Multiple requests share same session

### Limitations (Free Tier):
- ⚠️ Cold start: 30s delay after 15min idle
- ⚠️ 750 hours/month limit
- ⚠️ Shared resources (slower under load)

---

## Real-World Usage Examples

### Example 1: Single Player Lookup
```bash
curl https://maimai-api.onrender.com/api/player/101680566000997
```

### Example 2: Batch Lookup
```bash
curl -X POST https://maimai-api.onrender.com/api/batch \
  -H "Content-Type: application/json" \
  -d '{"friend_codes": ["101680566000997", "101232330856982"]}'
```

### Example 3: Health Check
```bash
curl https://maimai-api.onrender.com/health
```

---

## Summary

**In simple terms:**

1. **User wants data** → Asks your API
2. **API checks login** → Uses saved cookies
3. **If not logged in** → Browser logs in automatically (6-8s)
4. **If logged in** → Fetch player page (1-2s)
5. **Parse HTML** → Extract name and rating
6. **Return JSON** → User gets clean data

**Why this approach?**
- ✅ MaiMai requires login (no public API)
- ✅ Selenium handles complex login flow
- ✅ Cookies reused for efficiency
- ✅ API makes it easy for frontend to use
- ✅ Deployed on cloud (accessible anywhere)

**The magic:**
- Your users don't see the complexity
- They just get instant player data
- No manual login needed
- Works from any website/app

---

Ready to deploy? Follow the [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)!
