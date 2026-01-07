# Complete Render.com Deployment Guide
## MaiMai Data API Deployment

This guide will help you deploy your MaiMai automation as a web API on Render.com.

---

## Prerequisites

- [x] GitHub account
- [x] Render.com account (free, no credit card needed)
- [x] Your MaiMai credentials (SEGA ID & password)
- [x] Project files ready (all files created in this directory)

---

## Step 1: Prepare Your Project

### 1.1 Create `requirements.txt`

Create a file listing all Python dependencies:

```txt
flask==3.0.0
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.16.0
gunicorn==21.2.0
```

### 1.2 Create `app.py` (Flask API)

This will be your main API server file (I'll create this separately).

### 1.3 Create `render.yaml` (Optional but recommended)

```yaml
services:
  - type: web
    name: maimai-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SEGA_ID
        value: your-sega-id-here
      - key: PASSWORD
        value: your-password-here
```

---

## Step 2: Push to GitHub

### 2.1 Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit - MaiMai API"
```

### 2.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create new repository (e.g., "maimai-api")
3. Don't initialize with README (you already have files)

### 2.3 Push Your Code

```bash
git remote add origin https://github.com/YOUR-USERNAME/maimai-api.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy to Render.com

### 3.1 Sign Up

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended for easy integration)

### 3.2 Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select your `maimai-api` repository

### 3.3 Configure Service

**Basic Settings:**
- **Name:** `maimai-api` (or your choice)
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch:** `main`
- **Root Directory:** Leave blank (unless in subfolder)

**Build Settings:**
- **Runtime:** Python 3
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```
  gunicorn app:app
  ```

**Instance Type:**
- Select **Free** (for now)

### 3.4 Add Environment Variables

Click "Advanced" → "Add Environment Variable":

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `SEGA_ID` | `your-sega-id-here` |
| `PASSWORD` | `your-password-here` |

⚠️ **Important:** Replace with your actual credentials!

### 3.5 Deploy

1. Click "Create Web Service"
2. Render will start building your app
3. Wait 5-10 minutes for first deploy
4. Watch the logs for any errors

---

## Step 4: Install Chrome/Selenium on Render

Render doesn't have Chrome by default. Add these to your `requirements.txt`:

```txt
selenium==4.16.0
webdriver-manager==4.0.1
```

And add this to start of your `app.py`:

```python
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return options
```

**OR use Render's buildpack (recommended):**

Add this file: `render-build.sh`

```bash
#!/bin/bash
# Install Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
apt-get update
apt-get install -y google-chrome-stable

# Install Python deps
pip install -r requirements.txt
```

Then in Render dashboard, change Build Command to:
```
chmod +x render-build.sh && ./render-build.sh
```

---

## Step 5: Test Your Deployment

### 5.1 Get Your URL

After deployment, Render gives you a URL like:
```
https://maimai-api.onrender.com
```

### 5.2 Test Endpoints

**Health Check:**
```bash
curl https://maimai-api.onrender.com/
```

**Get Player Data:**
```bash
curl https://maimai-api.onrender.com/api/player/101680566000997
```

**Expected Response:**
```json
{
  "success": true,
  "friend_code": "101680566000997",
  "name": "Player Name",
  "rating": "15248"
}
```

---

## Step 6: Monitor & Maintain

### 6.1 View Logs

In Render dashboard:
- Go to your service
- Click "Logs" tab
- Monitor for errors

### 6.2 Auto-Deploy

Render automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update code"
git push
```

Render will rebuild and redeploy automatically!

### 6.3 Handle Cold Starts

**Free tier limitation:** Service sleeps after 15min inactivity.

**Solutions:**
1. **Upgrade to paid** ($7/month) - no sleep
2. **Use cron-job.org** - ping your API every 10min to keep it awake
3. **Accept 30s delay** on first request after idle

---

## Step 7: Use in Your Frontend

### JavaScript Example:

```javascript
async function getPlayerData(friendCode) {
    try {
        const response = await fetch(
            `https://maimai-api.onrender.com/api/player/${friendCode}`
        );
        const data = await response.json();
        
        if (data.success) {
            console.log('Name:', data.name);
            console.log('Rating:', data.rating);
        } else {
            console.error('Error:', data.error);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}

// Usage
getPlayerData('101680566000997');
```

---

## Troubleshooting

### Issue: Build fails

**Check:**
- `requirements.txt` has all dependencies
- Python version is compatible (use 3.11)
- No syntax errors in code

### Issue: Selenium/Chrome not working

**Solution:**
- Use `render-build.sh` to install Chrome
- Add `--no-sandbox` and `--headless` options
- Check Render logs for specific Chrome errors

### Issue: Authentication fails

**Check:**
- Environment variables are set correctly
- SEGA_ID and PASSWORD are correct
- Cookies are being saved and loaded properly

### Issue: Cold start takes too long

**Solutions:**
- Upgrade to paid plan ($7/month)
- Use external monitoring to keep alive
- Cache session cookies longer

### Issue: 503 Service Unavailable

**Causes:**
- Free tier spinning down (wait 30s)
- Build failed (check logs)
- Start command incorrect

---

## Cost Breakdown

### Free Tier
- ✅ 750 hours/month
- ✅ Enough for ~1000 requests/month
- ⚠️ Cold starts after 15min idle

### Paid Tier ($7/month)
- ✅ Always on (no cold starts)
- ✅ Unlimited hours
- ✅ Better performance
- ✅ Custom domains

---

## Security Notes

⚠️ **Important:**

1. **Never commit credentials to GitHub**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Add rate limiting**
   - Prevent abuse
   - Use Flask-Limiter

3. **Add authentication** (optional)
   - API keys for your frontend
   - Prevents unauthorized access

---

## Next Steps

1. Create `app.py` with Flask API endpoints
2. Test locally first
3. Push to GitHub
4. Deploy to Render
5. Test live API
6. Integrate with your frontend

---

## Useful Commands

```bash
# Test locally
python app.py

# Check if requirements.txt is complete
pip freeze > requirements.txt

# Test production-like with gunicorn
gunicorn app:app

# Push updates
git add .
git commit -m "Update"
git push
```

---

## Support Resources

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **Selenium Docs:** https://selenium-python.readthedocs.io
- **Flask Docs:** https://flask.palletsprojects.com

---

## Ready to Deploy?

Next, I'll create the Flask API (`app.py`) that works perfectly with this deployment guide!

Would you like me to create the Flask API file now?
