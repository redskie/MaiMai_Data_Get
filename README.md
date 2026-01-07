# MaiMai DX Player Data Fetcher

Automation tool to fetch player data from the MaiMai DX website using friend codes.

## Setup

1. Install required packages:
```bash
pip install requests beautifulsoup4 selenium
```

## Usage

### Step 1: Login and Save Session

Run the automated login script:
```bash
python auto_login.py
```

This will:
- Open Edge browser
- Navigate to MaiMai login page
- Click SEGA ID button
- Enter your credentials (already configured)
- Check terms of service checkbox
- Click Login
- Save authentication cookies automatically

### Step 2: Fetch Player Data

Run the data fetcher:
```bash
python get_player_data.py
```

Enter any player's friend code when prompted (e.g., `101232330856982`)

## Files

- `auto_login.py` - Automated login script using Selenium
- `get_player_data.py` - Main script to fetch player data
- `cookies.json` - Stores authentication cookies (created automatically)
- `README.md` - This file

## Example Output

```
=== Player Data ===
Friend Code: 101232330856982
Name: ＢＭＣ☆ＭＡＲＸ
Rating: 15248
```

## Notes

- Cookies expire after some time. If authentication fails, re-run `auto_login.py`
- The script uses your saved credentials for automatic login
- All authentication is handled securely via session cookies
