# MaiMai DX Player Data API

🎮 A lightweight REST API to fetch MaiMai DX player data (IGN, rating, trophy, icon) using friend codes.

## 🚀 Live API

**Base URL:** `https://maimai-data-get.onrender.com`

## ✨ Features

- ✅ **No browser required** - Pure Python requests
- ✅ **Fast & lightweight** - 2-5 second response time
- ✅ **Batch requests** - Fetch up to 10 players at once
- ✅ **CORS enabled** - Use from any frontend
- ✅ **Auto-retry** - Handles session expiration automatically
- ✅ **Free hosting** - Works on any platform

## 📡 Quick Start

```bash
# Get player data
curl https://maimai-data-get.onrender.com/api/player/101680566000997

# Response
{
  "success": true,
  "friend_code": "101680566000997",
  "ign": "PlayerName",
  "rating": "15248",
  "trophy": "maimai Master",
  "icon_url": "https://..."
}
```

## 📚 Documentation

**Complete integration guide:** [API_INTEGRATION.md](API_INTEGRATION.md)

Includes:
- Detailed endpoint documentation
- Code examples (Python, JavaScript, Node.js, cURL)
- Error handling patterns
- Automation examples (Discord bots, web scrapers, Telegram bots)
- Performance tips and best practices

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SEGA_ID="your_sega_id"
export PASSWORD="your_password"

# Run locally
python app.py
```

## 🌐 Deploy to Render

1. Fork this repository
2. Create new Web Service on Render
3. Connect your GitHub repository
4. Set environment variables: `SEGA_ID` and `PASSWORD`
5. Deploy!

## 📊 Response Format

```json
{
  "success": boolean,
  "friend_code": "string",
  "ign": "string",
  "rating": "string",
  "trophy": "string|null",
  "icon_url": "string|null",
  "error": "string (only if success=false)"
}
```

## 🔗 Endpoints

- `GET /` - API documentation
- `GET /api/player/<friend_code>` - Get single player
- `POST /api/batch` - Get multiple players (max 10)
- `GET /health` - Health check

## 📝 License

MIT - Free to use for personal and commercial projects

## 🙏 Credits

Data from [MaiMai DX](https://maimaidx-eng.com) by SEGA
