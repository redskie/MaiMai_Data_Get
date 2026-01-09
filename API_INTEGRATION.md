# MaiMai DX Player Data API - Integration Guide

## 📋 Overview

This API fetches MaiMai DX player data using friend codes. It returns player IGN (In-Game Name), rating, trophy/title, and icon URL in a machine-readable JSON format optimized for automation.

**Base URL:** `https://maimai-data-get.onrender.com`

---

## 🚀 Quick Start

### Simple Request
```bash
GET https://maimai-data-get.onrender.com/api/player/101680566000997
```

### Response
```json
{
  "success": true,
  "friend_code": "101680566000997",
  "ign": "PlayerName",
  "rating": "15248",
  "trophy": "maimai Master",
  "icon_url": "https://maimaidx-eng.com/maimai-mobile/img/Icon/xxx.png"
}
```

---

## 📡 API Endpoints

### 1. Get Player Data (Single)

**Endpoint:** `GET /api/player/<friend_code>`

**Parameters:**
- `friend_code` (string, required): 15-digit MaiMai friend code

**Response (Success):**
```json
{
  "success": true,
  "friend_code": "101680566000997",
  "ign": "PlayerName",
  "rating": "15248",
  "trophy": "maimai Master",
  "icon_url": "https://maimaidx-eng.com/maimai-mobile/img/Icon/xxx.png"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Player not found or invalid friend code"
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid friend code format
- `500`: Server error or authentication failure

---

### 2. Batch Request (Multiple Players)

**Endpoint:** `POST /api/batch`

**Request Body:**
```json
{
  "friend_codes": [
    "101680566000997",
    "101232330856982",
    "103456789012345"
  ]
}
```

**Constraints:**
- Maximum 10 friend codes per request
- Minimum 1 friend code required

**Response:**
```json
{
  "success": true,
  "count": 3,
  "results": [
    {
      "success": true,
      "friend_code": "101680566000997",
      "ign": "Player1",
      "rating": "15248",
      "trophy": "maimai Master",
      "icon_url": "https://..."
    },
    {
      "success": true,
      "friend_code": "101232330856982",
      "ign": "Player2",
      "rating": "14500",
      "trophy": "Legend",
      "icon_url": "https://..."
    },
    {
      "success": false,
      "error": "Player not found or invalid friend code"
    }
  ]
}
```

---

### 3. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "session_valid": true,
  "last_login": "2026-01-10T12:34:56.789",
  "uptime": "operational"
}
```

---

## 💻 Code Examples

### Python (requests)
```python
import requests

# Single player
response = requests.get(
    "https://maimai-data-get.onrender.com/api/player/101680566000997"
)
data = response.json()

if data["success"]:
    print(f"IGN: {data['ign']}")
    print(f"Rating: {data['rating']}")
    print(f"Trophy: {data['trophy']}")
else:
    print(f"Error: {data['error']}")

# Batch request
response = requests.post(
    "https://maimai-data-get.onrender.com/api/batch",
    json={"friend_codes": ["101680566000997", "101232330856982"]}
)
data = response.json()

for result in data["results"]:
    if result["success"]:
        print(f"{result['ign']}: {result['rating']}")
```

### JavaScript (fetch)
```javascript
// Single player
async function getPlayerData(friendCode) {
    const response = await fetch(
        `https://maimai-data-get.onrender.com/api/player/${friendCode}`
    );
    const data = await response.json();
    
    if (data.success) {
        console.log('IGN:', data.ign);
        console.log('Rating:', data.rating);
        console.log('Trophy:', data.trophy);
    } else {
        console.error('Error:', data.error);
    }
}

// Batch request
async function getBatchData(friendCodes) {
    const response = await fetch(
        'https://maimai-data-get.onrender.com/api/batch',
        {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({friend_codes: friendCodes})
        }
    );
    const data = await response.json();
    
    data.results.forEach(result => {
        if (result.success) {
            console.log(`${result.ign}: ${result.rating}`);
        }
    });
}

// Usage
getPlayerData('101680566000997');
getBatchData(['101680566000997', '101232330856982']);
```

### cURL
```bash
# Single player
curl https://maimai-data-get.onrender.com/api/player/101680566000997

# Batch request
curl -X POST https://maimai-data-get.onrender.com/api/batch \
  -H "Content-Type: application/json" \
  -d '{"friend_codes":["101680566000997","101232330856982"]}'
```

### Node.js (axios)
```javascript
const axios = require('axios');

// Single player
async function getPlayer(friendCode) {
    try {
        const response = await axios.get(
            `https://maimai-data-get.onrender.com/api/player/${friendCode}`
        );
        
        if (response.data.success) {
            console.log('IGN:', response.data.ign);
            console.log('Rating:', response.data.rating);
        }
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

// Batch request
async function getBatch(friendCodes) {
    try {
        const response = await axios.post(
            'https://maimai-data-get.onrender.com/api/batch',
            { friend_codes: friendCodes }
        );
        
        response.data.results.forEach(result => {
            if (result.success) {
                console.log(`${result.ign}: ${result.rating}`);
            }
        });
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}
```

---

## 🔄 Response Fields Explained

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `success` | boolean | Whether the request was successful | `true` |
| `friend_code` | string | The requested friend code | `"101680566000997"` |
| `ign` | string | In-Game Name (player name) | `"PlayerName"` |
| `rating` | string | Player rating (DX Rating) | `"15248"` |
| `trophy` | string or null | Player trophy/title | `"maimai Master"` |
| `icon_url` | string or null | URL to player icon image | `"https://..."` |
| `error` | string | Error message (only when success=false) | `"Session expired"` |

---

## ⚠️ Error Handling

### Common Errors

**Invalid Friend Code:**
```json
{
  "success": false,
  "error": "Invalid friend code format"
}
```

**Player Not Found:**
```json
{
  "success": false,
  "error": "Player not found or invalid friend code"
}
```

**Session Expired:**
```json
{
  "success": false,
  "error": "Session expired"
}
```
*The API will automatically re-login and retry once.*

**Authentication Failed:**
```json
{
  "success": false,
  "error": "Failed to authenticate"
}
```

**Batch Limit Exceeded:**
```json
{
  "success": false,
  "error": "Maximum 10 friend codes per request"
}
```

### Recommended Error Handling Pattern

```python
import requests
import time

def get_player_with_retry(friend_code, max_retries=3):
    """Get player data with automatic retry on failure"""
    
    for attempt in range(max_retries):
        try:
            response = requests.get(
                f"https://maimai-data-get.onrender.com/api/player/{friend_code}",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    return data
                elif "Session expired" in data.get("error", ""):
                    # Wait and retry on session expiration
                    time.sleep(5)
                    continue
                else:
                    # Other errors - don't retry
                    return data
            else:
                # Server error - retry
                time.sleep(2)
                continue
                
        except requests.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return {"success": False, "error": "Request timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return {"success": False, "error": "Max retries exceeded"}
```

---

## ⏱️ Performance & Limits

### Response Times
- **First request (cold start):** 30-60 seconds (free tier)
- **Subsequent requests:** 2-5 seconds
- **Batch requests:** ~3-8 seconds per player

### Rate Limits
- No explicit rate limit currently
- Recommended: **Max 10 requests/minute** for stability
- Batch endpoint: **Max 10 friend codes per request**

### Best Practices
1. **Cache responses** - Player data doesn't change frequently
2. **Use batch endpoint** - More efficient for multiple players
3. **Implement retry logic** - Handle cold starts gracefully
4. **Add timeouts** - Set 30-60s timeout for first request, 15s for others

---

## 🔐 CORS & Security

### CORS
- **CORS enabled** for all origins
- Supports all standard HTTP methods
- Safe to call from browser/frontend

### Authentication
- No API key required (currently)
- Public endpoint for read-only access
- Backend handles MaiMai authentication automatically

---

## 🐛 Troubleshooting

### Issue: Request times out
**Solution:** First request after idle may take 30-60s. Use longer timeout:
```python
requests.get(url, timeout=60)
```

### Issue: "Session expired" errors
**Solution:** API automatically handles this. If persistent, wait 5 minutes and retry.

### Issue: "Player not found"
**Solution:** Verify friend code is correct (15 digits). Some private profiles may be inaccessible.

### Issue: Getting `null` for trophy
**Solution:** Player may not have a trophy set. This is normal.

---

## 📊 Usage Examples for Automation

### Discord Bot Integration
```python
import discord
from discord.ext import commands
import requests

bot = commands.Bot(command_prefix='!')

@bot.command()
async def maimai(ctx, friend_code: str):
    """Get MaiMai player data"""
    
    response = requests.get(
        f"https://maimai-data-get.onrender.com/api/player/{friend_code}",
        timeout=60
    )
    data = response.json()
    
    if data["success"]:
        embed = discord.Embed(title=data["ign"], color=0xFF69B4)
        embed.add_field(name="Rating", value=data["rating"], inline=True)
        embed.add_field(name="Trophy", value=data.get("trophy", "None"), inline=True)
        if data.get("icon_url"):
            embed.set_thumbnail(url=data["icon_url"])
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Error: {data['error']}")
```

### Web Scraper / Data Collection
```python
import requests
import pandas as pd
import time

def collect_player_data(friend_codes):
    """Collect data for multiple players efficiently"""
    
    # Use batch endpoint for efficiency
    batch_size = 10
    all_results = []
    
    for i in range(0, len(friend_codes), batch_size):
        batch = friend_codes[i:i+batch_size]
        
        response = requests.post(
            "https://maimai-data-get.onrender.com/api/batch",
            json={"friend_codes": batch},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            all_results.extend([
                r for r in data["results"] if r["success"]
            ])
        
        time.sleep(2)  # Respectful rate limiting
    
    # Convert to DataFrame
    df = pd.DataFrame(all_results)
    return df[["ign", "rating", "trophy", "friend_code"]]

# Usage
codes = ["101680566000997", "101232330856982", ...]
df = collect_player_data(codes)
df.to_csv("maimai_players.csv", index=False)
```

### Telegram Bot
```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

async def maimai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /maimai <friend_code>")
        return
    
    friend_code = context.args[0]
    await update.message.reply_text("Fetching data...")
    
    response = requests.get(
        f"https://maimai-data-get.onrender.com/api/player/{friend_code}",
        timeout=60
    )
    data = response.json()
    
    if data["success"]:
        message = f"""
🎮 **{data['ign']}**
⭐ Rating: {data['rating']}
🏆 Trophy: {data.get('trophy', 'None')}
🆔 Friend Code: {data['friend_code']}
        """
        await update.message.reply_text(message)
    else:
        await update.message.reply_text(f"❌ Error: {data['error']}")

# Setup
app = Application.builder().token("YOUR_TOKEN").build()
app.add_handler(CommandHandler("maimai", maimai_command))
app.run_polling()
```

---

## 📝 Important Notes for AI/Automation

### Data Types
- All fields return **strings** (not integers)
- `rating` is a string like `"15248"`, not a number
- Convert to int/float if needed: `int(data['rating'])`

### Null Values
- `trophy` and `icon_url` may be `null`
- Always check: `data.get('trophy', 'N/A')`

### Success Flag
- **Always check** `success` field first:
```python
if data["success"]:
    # Process data
else:
    # Handle error
```

### Batch Processing
- Results array matches input order
- Some may succeed while others fail
- Each result has its own `success` flag

### Cold Start Handling
```python
# Good: Handle cold start
response = requests.get(url, timeout=60)

# Bad: Will timeout on cold start
response = requests.get(url, timeout=10)
```

---

## 🆘 Support

**Issues:** https://github.com/redskie/MaiMai_Data_Get/issues  
**Repository:** https://github.com/redskie/MaiMai_Data_Get

---

## 📜 License & Terms

- **Free to use** for personal and commercial projects
- **No authentication required**
- **No rate limiting** (but please be respectful)
- **No warranty** - Use at your own risk
- Data belongs to SEGA / MaiMai DX

---

## 🔄 Changelog

### v2.0.0 (2026-01-10)
- ✨ Replaced Selenium with pure requests (no browser needed)
- ✨ Added `trophy` field to response
- ✨ Added `icon_url` field to response
- ⚡ Improved response time and stability
- 📝 Better error messages
- 🌐 Works on any free hosting platform

### v1.0.0 (2026-01-08)
- 🎉 Initial release
- Basic player data fetching (IGN + rating)
