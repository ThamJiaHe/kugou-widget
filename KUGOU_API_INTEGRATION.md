# KuGou Music API Integration Guide

This guide shows you how to connect your widget to **real Kugou listening history** using the KuGouMusicApi Node.js service.

## Architecture

```
Your Kugou Account 
    ↓
KuGouMusicApi (Node.js on Vercel) 
    ↓
Python Widget (this repo)
    ↓
GitHub Profile README
```

The KuGouMusicApi handles authentication and provides a clean REST API. Your Python widget calls it to get real-time listening data.

---

## Step 1: Deploy KuGouMusicApi to Vercel

### Fork and Deploy

1. **Fork the KuGouMusicApi repository:**
   - Go to: https://github.com/zkhssb/KuGouMusicApi
   - Click "Fork" to create your own copy

2. **Deploy to Vercel:**
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/KuGouMusicApi.git
   cd KuGouMusicApi
   
   # Deploy
   vercel --prod
   ```

3. **Save your API URL:**
   - After deployment, Vercel will show: `https://your-kugou-api.vercel.app`
   - Save this URL - you'll need it later!

---

## Step 2: Login to Your Kugou Account via KuGouMusicApi

### Get Authentication Credentials

Use curl to login and get your `userid` and `token`:

```bash
# Replace YOUR_API_URL with your deployed URL
curl "https://YOUR_API_URL/login/code?username=YOUR_PHONE_OR_EMAIL"
```

This will send a verification code to your phone/email.

Then verify with the code:

```bash
curl "https://YOUR_API_URL/login/verify?username=YOUR_PHONE_OR_EMAIL&code=123456"
```

**Response example:**
```json
{
  "status": 1,
  "data": {
    "userid": "123456789",
    "token": "abc123def456...",
    "username": "your_name"
  }
}
```

**Save these values:**
- `userid` - Your Kugou user ID
- `token` - Your authentication token

---

## Step 3: Save Your Kugou Credentials to Firebase

Now connect your KuGouMusicApi to this widget:

```bash
curl -X POST https://YOUR_WIDGET_URL/setup-kugou \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your_github_username",
    "api_url": "https://your-kugou-api.vercel.app",
    "userid": "123456789",
    "token": "abc123def456..."
  }'
```

**Success response:**
```json
{
  "success": true,
  "message": "Kugou API credentials saved successfully!",
  "widget_url": "https://your-widget-url/?user_id=your_github_username&theme=dark",
  "next_steps": [
    "Your widget will now show real-time listening history from Kugou",
    "Add to your GitHub README to see it in action",
    "Songs update automatically when you play on Kugou"
  ]
}
```

---

## Step 4: Add Widget to GitHub Profile

Add this to your `README.md`:

```markdown
## 🎵 Now Playing on Kugou

![Kugou Music](https://YOUR_WIDGET_URL/?user_id=YOUR_GITHUB_USERNAME&theme=dark)
```

**Available themes:**
- `theme=dark` - Dark mode (default)
- `theme=light` - Light mode

---

## How It Works

### Real-Time Sync Priority

When someone views your GitHub profile:

1. **Try KuGouMusicApi:** Fetches your latest listening history
2. **Fallback to Cache:** If API unavailable, shows cached song
3. **Demo Mode:** If no data, shows demo song

### Data Flow

```python
# Python widget calls your Node.js API
GET https://your-kugou-api.vercel.app/user/recentListening?userid=XXX&token=YYY

# Response from KuGouMusicApi
{
  "data": {
    "list": [
      {
        "fileName": "七里香",
        "singername": "周杰伦",
        "imgUrl": "https://..."
      }
    ]
  }
}

# Widget caches in Firebase and generates SVG
```

---

## Automatic Sync (Optional)

Want to keep your widget always up-to-date? Use the sync script:

### Setup Periodic Sync

1. **Create sync script** (see `sync_kugou_listening.py` below)

2. **Run on schedule:**
   ```bash
   # Using cron (Linux/Mac)
   crontab -e
   
   # Add line: sync every 5 minutes
   */5 * * * * cd /path/to/kugou-widget && python3 sync_kugou_listening.py
   ```

3. **Or use GitHub Actions:**
   ```yaml
   name: Sync Kugou
   on:
     schedule:
       - cron: '*/5 * * * *'  # Every 5 minutes
   jobs:
     sync:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - run: python3 sync_kugou_listening.py
   ```

---

## Troubleshooting

### No Song Showing

**Check credentials:**
```bash
# Verify your token is still valid
curl "https://YOUR_API_URL/user/recentListening?userid=XXX&token=YYY"
```

If expired, re-run Step 2 to get new credentials.

### API Connection Failed

**Test your KuGouMusicApi:**
```bash
curl "https://YOUR_API_URL/health"
```

Should return `{"status": "ok"}`.

### Widget Shows Demo Song

This means:
1. No KuGouMusicApi credentials configured, OR
2. API call failed, OR  
3. No listening history on your Kugou account

Check Firebase credentials with:
```bash
curl "https://YOUR_WIDGET_URL/test?user_id=your_github_username"
```

---

## Maintenance

### Update Token

Tokens may expire after ~30 days. To refresh:

1. Get new token:
   ```bash
   curl "https://YOUR_API_URL/login/code?username=YOUR_PHONE"
   curl "https://YOUR_API_URL/login/verify?username=YOUR_PHONE&code=123456"
   ```

2. Update in Firebase:
   ```bash
   curl -X POST https://YOUR_WIDGET_URL/setup-kugou \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "your_github_username",
       "api_url": "https://your-kugou-api.vercel.app",
       "userid": "123456789",
       "token": "NEW_TOKEN_HERE"
     }'
   ```

### Check Integration Status

```bash
# View current configuration
curl "https://YOUR_WIDGET_URL/test?user_id=your_github_username"

# Response shows:
# - Firebase connection: OK
# - Kugou credentials: Configured ✓
# - Current song: [Song name]
```

---

## Security Notes

- **Tokens are stored securely in Firebase** (not in code)
- Your KuGouMusicApi should be deployed to your own Vercel account
- Never commit tokens to Git repositories
- Tokens are user-specific and cannot access other accounts

---

## Example: Complete Setup

```bash
# 1. Deploy KuGouMusicApi
cd ~/projects
git clone https://github.com/YOUR_USERNAME/KuGouMusicApi.git
cd KuGouMusicApi
vercel --prod
# Output: https://my-kugou-api.vercel.app

# 2. Login to Kugou
curl "https://my-kugou-api.vercel.app/login/code?username=13800138000"
curl "https://my-kugou-api.vercel.app/login/verify?username=13800138000&code=123456"
# Save: userid=987654321, token=xyz789abc...

# 3. Connect to widget
curl -X POST https://kugou-widget.vercel.app/setup-kugou \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "octocat",
    "api_url": "https://my-kugou-api.vercel.app",
    "userid": "987654321",
    "token": "xyz789abc..."
  }'

# 4. Add to GitHub README
echo '![Kugou](https://kugou-widget.vercel.app/?user_id=octocat&theme=dark)' >> README.md
git add README.md
git commit -m "Add Kugou widget"
git push
```

Done! Your GitHub profile now shows real-time Kugou listening history! 🎵

---

## Need Help?

- **KuGouMusicApi Issues:** https://github.com/zkhssb/KuGouMusicApi/issues
- **Widget Issues:** Open issue in this repository
- **Kugou Account:** Contact Kugou support

---

## Advanced: Manual Sync Script

Create `sync_kugou_listening.py`:

```python
#!/usr/bin/env python3
"""
Sync Kugou listening history to Firebase cache
Run this periodically (e.g., every 5 minutes) for always-fresh data
"""

import requests
import os
import sys

# Configuration
WIDGET_URL = os.getenv('WIDGET_URL', 'https://kugou-widget.vercel.app')
USER_ID = os.getenv('USER_ID', 'your_github_username')

def sync_listening_history():
    """Trigger widget to fetch from KuGouMusicApi and update cache"""
    try:
        # Just accessing the widget triggers the sync
        url = f"{WIDGET_URL}/now-playing?user_id={USER_ID}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✓ Synced listening history for {USER_ID}")
            return True
        else:
            print(f"✗ Sync failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Sync error: {e}")
        return False

if __name__ == '__main__':
    success = sync_listening_history()
    sys.exit(0 if success else 1)
```

Make it executable:
```bash
chmod +x sync_kugou_listening.py
```

Run manually:
```bash
export WIDGET_URL="https://your-widget-url.vercel.app"
export USER_ID="your_github_username"
./sync_kugou_listening.py
```

Or schedule with cron:
```bash
crontab -e
# Add:
*/5 * * * * cd /path/to/kugou-widget && WIDGET_URL="https://..." USER_ID="..." ./sync_kugou_listening.py >> /tmp/kugou-sync.log 2>&1
```
