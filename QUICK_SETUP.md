# Quick Setup Guide - KuGou Widget with Real-Time Sync

> **Goal:** Display your real Kugou listening history on your GitHub profile in 15 minutes.

---

## Prerequisites

- GitHub account
- Vercel account (free)
- Kugou Music account (Chinese music streaming service)
- Basic command line knowledge

---

## Part 1: Deploy This Widget (5 minutes)

### 1. Fork and deploy this repository

```bash
# Fork on GitHub, then clone
git clone https://github.com/YOUR_USERNAME/kugou-widget.git
cd kugou-widget

# Deploy to Vercel
npm i -g vercel
vercel login
vercel --prod
```

**Save your widget URL:** `https://kugou-widget-YOUR_ID.vercel.app`

### 2. Test it works

```bash
curl "https://kugou-widget-YOUR_ID.vercel.app/health"
# Should return: {"status": "healthy", ...}

curl "https://kugou-widget-YOUR_ID.vercel.app?user_id=demo"
# Should return an SVG with demo song
```

✅ **Widget deployed!** Now let's connect it to your Kugou account.

---

## Part 2: Deploy KuGouMusicApi (5 minutes)

### 1. Fork and deploy KuGouMusicApi

```bash
# Fork https://github.com/zkhssb/KuGouMusicApi, then clone
git clone https://github.com/YOUR_USERNAME/KuGouMusicApi.git
cd KuGouMusicApi

# Deploy to Vercel
vercel --prod
```

**Save your API URL:** `https://kugou-api-YOUR_ID.vercel.app`

### 2. Test it works

```bash
curl "https://kugou-api-YOUR_ID.vercel.app/health"
# Should return: {"status": "ok"}
```

✅ **KuGouMusicApi deployed!** Now let's login to your Kugou account.

---

## Part 3: Connect Your Kugou Account (5 minutes)

### 1. Login to Kugou via KuGouMusicApi

**Request verification code:**
```bash
curl "https://kugou-api-YOUR_ID.vercel.app/login/code?username=YOUR_PHONE_NUMBER"
# Or use email: username=YOUR_EMAIL@example.com
```

You'll receive a verification code via SMS or email.

**Verify and get credentials:**
```bash
curl "https://kugou-api-YOUR_ID.vercel.app/login/verify?username=YOUR_PHONE_NUMBER&code=123456"
```

**Response example:**
```json
{
  "status": 1,
  "data": {
    "userid": "987654321",
    "token": "abc123def456xyz789...",
    "username": "Your Name"
  }
}
```

📝 **Copy these values:**
- `userid`: `987654321`
- `token`: `abc123def456xyz789...`

### 2. Save credentials to your widget

```bash
curl -X POST https://kugou-widget-YOUR_ID.vercel.app/setup-kugou \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_GITHUB_USERNAME",
    "api_url": "https://kugou-api-YOUR_ID.vercel.app",
    "userid": "987654321",
    "token": "abc123def456xyz789..."
  }'
```

**Success response:**
```json
{
  "success": true,
  "message": "Kugou API credentials saved successfully!",
  "widget_url": "https://kugou-widget-YOUR_ID.vercel.app?user_id=YOUR_GITHUB_USERNAME&theme=dark",
  "next_steps": [...]
}
```

✅ **Credentials saved!** Your widget is now connected to your Kugou account.

---

## Part 4: Add to GitHub Profile (1 minute)

### 1. Edit your GitHub profile README

```bash
# Clone your profile repo (YOUR_USERNAME/YOUR_USERNAME)
git clone https://github.com/YOUR_USERNAME/YOUR_USERNAME.git
cd YOUR_USERNAME

# Edit README.md
nano README.md
```

### 2. Add this line anywhere in your README.md:

```markdown
## 🎵 Now Playing on Kugou

![Kugou Music](https://kugou-widget-YOUR_ID.vercel.app?user_id=YOUR_GITHUB_USERNAME&theme=dark)
```

### 3. Commit and push

```bash
git add README.md
git commit -m "Add Kugou music widget"
git push
```

### 4. View your profile

Visit: `https://github.com/YOUR_USERNAME`

🎉 **Done!** Your GitHub profile now shows your real-time Kugou listening history!

---

## Themes and Customization

### Available Themes

**Dark theme (default):**
```markdown
![Kugou](https://kugou-widget-YOUR_ID.vercel.app?user_id=YOUR_USERNAME&theme=dark)
```

**Light theme:**
```markdown
![Kugou](https://kugou-widget-YOUR_ID.vercel.app?user_id=YOUR_USERNAME&theme=light)
```

### Custom Size

```markdown
![Kugou](https://kugou-widget-YOUR_ID.vercel.app?user_id=YOUR_USERNAME&theme=dark&width=500&height=150)
```

---

## How It Works

```
┌─────────────────┐
│ You play song   │
│ on Kugou app    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ KuGouMusicApi   │ ← You deployed this
│ (Node.js)       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Python Widget   │ ← You deployed this
│ Fetches history │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ GitHub Profile  │ ← Shows SVG
│ README.md       │
└─────────────────┘
```

**Update frequency:**
- Widget fetches from KuGouMusicApi every time someone views your profile
- KuGouMusicApi shows your recent listening history
- Data is cached in Firebase for fast loading

---

## Troubleshooting

### Widget shows demo song instead of my music

**Check if credentials are saved:**
```bash
curl "https://kugou-widget-YOUR_ID.vercel.app/test?user_id=YOUR_GITHUB_USERNAME"
```

Look for: `"kugou_api": "Configured"`

If not configured, run Part 3 Step 2 again.

### KuGouMusicApi returns error

**Token might be expired (after ~30 days).**

Solution: Re-run Part 3 to get fresh credentials.

### Widget not updating

**GitHub caches images.**

Solutions:
1. Wait 5 minutes for cache to expire
2. Add `?cache_bust=123` to URL and change number each time
3. Hard refresh your GitHub profile (Ctrl+F5 or Cmd+Shift+R)

---

## Optional: Automatic Sync

Want to sync every 5 minutes automatically?

### Setup cron job:

```bash
# Download sync script
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/kugou-widget/main/sync_kugou_listening.py
chmod +x sync_kugou_listening.py

# Test it
export WIDGET_URL="https://kugou-widget-YOUR_ID.vercel.app"
export USER_ID="YOUR_GITHUB_USERNAME"
./sync_kugou_listening.py

# Add to cron
crontab -e

# Add this line (sync every 5 minutes):
*/5 * * * * cd /path/to/kugou-widget && WIDGET_URL="https://..." USER_ID="..." ./sync_kugou_listening.py >> /tmp/kugou-sync.log 2>&1
```

---

## Need More Help?

- **Detailed guide:** [KUGOU_API_INTEGRATION.md](KUGOU_API_INTEGRATION.md)
- **Manual updates:** [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Song presets:** [SONGS.md](SONGS.md)
- **Open issue:** https://github.com/YOUR_USERNAME/kugou-widget/issues

---

## Complete Example (Copy-Paste Ready)

Replace these values:
- `YOUR_USERNAME` → Your GitHub username
- `YOUR_WIDGET_ID` → Your widget Vercel deployment ID
- `YOUR_API_ID` → Your KuGouMusicApi Vercel deployment ID
- `YOUR_PHONE` → Your Kugou phone number
- `VERIFICATION_CODE` → Code from SMS

```bash
# 1. Deploy widget
git clone https://github.com/YOUR_USERNAME/kugou-widget.git
cd kugou-widget
vercel --prod
# Note the URL: https://kugou-widget-YOUR_WIDGET_ID.vercel.app

# 2. Deploy KuGouMusicApi
git clone https://github.com/YOUR_USERNAME/KuGouMusicApi.git
cd KuGouMusicApi
vercel --prod
# Note the URL: https://kugou-api-YOUR_API_ID.vercel.app

# 3. Login to Kugou
curl "https://kugou-api-YOUR_API_ID.vercel.app/login/code?username=YOUR_PHONE"
# Check SMS for code
curl "https://kugou-api-YOUR_API_ID.vercel.app/login/verify?username=YOUR_PHONE&code=VERIFICATION_CODE"
# Note: userid and token from response

# 4. Save credentials
curl -X POST https://kugou-widget-YOUR_WIDGET_ID.vercel.app/setup-kugou \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_USERNAME",
    "api_url": "https://kugou-api-YOUR_API_ID.vercel.app",
    "userid": "PASTE_USERID_HERE",
    "token": "PASTE_TOKEN_HERE"
  }'

# 5. Add to GitHub README
echo '## 🎵 Now Playing
![Kugou](https://kugou-widget-YOUR_WIDGET_ID.vercel.app?user_id=YOUR_USERNAME&theme=dark)' >> README.md

# 6. Commit and push
git add README.md
git commit -m "Add Kugou widget"
git push
```

---

**Time to complete:** ~15 minutes  
**Difficulty:** Easy (just copy-paste commands)  
**Result:** Real-time Kugou listening history on your GitHub profile! 🎵✨
