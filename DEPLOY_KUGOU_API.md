# KuGouMusicApi Deployment Guide

Your widget is successfully deployed at:
**https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app**

Now let's deploy the KuGouMusicApi Node.js service to enable real-time Kugou listening history.

---

## Quick Deploy (5 minutes)

### Option A: Using the Deploy Script (Easiest)

```bash
# Make the script executable
chmod +x deploy_kugou_api.sh

# Run it
./deploy_kugou_api.sh
```

The script will:
1. ✅ Check prerequisites (Node.js, npm, Vercel CLI)
2. ✅ Clone KuGouMusicApi repository
3. ✅ Install dependencies
4. ✅ Deploy to Vercel
5. ✅ Show next steps

---

### Option B: Manual Deployment

#### 1. Clone the Repository

```bash
cd ~
git clone https://github.com/MakcRe/KuGouMusicApi.git
cd KuGouMusicApi
```

#### 2. Install Dependencies

```bash
npm install
```

#### 3. Login to Vercel

```bash
vercel login
```

This will open a browser window to authenticate.

#### 4. Deploy to Production

```bash
vercel --prod
```

**Answer the prompts:**
- Set up and deploy? → **Y**
- Which scope? → Select your account
- Link to existing project? → **N** (create new)
- What's your project name? → `kugou-music-api` (or any name)
- In which directory is your code? → **./** (press Enter)
- Want to modify settings? → **N**

#### 5. Save Your API URL

After deployment completes, you'll see:
```
✅ Production: https://kugou-music-api-xxxxx.vercel.app
```

**Copy and save this URL!** You'll need it in the next steps.

---

## Test Your Deployment

### 1. Health Check

```bash
curl "https://YOUR_API_URL/health"
```

**Expected response:**
```json
{"status": "ok"}
```

### 2. Test an Endpoint

```bash
curl "https://YOUR_API_URL/api/search?keyword=周杰伦"
```

Should return search results for Jay Chou songs.

---

## Connect to Your Widget

### 1. Login to Your Kugou Account

**Request verification code:**
```bash
curl "https://YOUR_API_URL/login/code?username=YOUR_PHONE_NUMBER"
```

Replace:
- `YOUR_API_URL` → Your deployed KuGouMusicApi URL
- `YOUR_PHONE_NUMBER` → Your Kugou account phone number (e.g., 13800138000)

You'll receive an SMS with a verification code.

**Verify and get credentials:**
```bash
curl "https://YOUR_API_URL/login/verify?username=YOUR_PHONE_NUMBER&code=123456"
```

Replace `123456` with the code from your SMS.

**Response example:**
```json
{
  "status": 1,
  "data": {
    "userid": "987654321",
    "token": "abc123def456xyz789abcdef...",
    "username": "Your Name"
  }
}
```

📝 **Copy these values:**
- `userid`: The user ID number
- `token`: The authentication token (long string)

### 2. Save Credentials to Your Widget

```bash
curl -X POST https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app/setup-kugou \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_GITHUB_USERNAME",
    "api_url": "https://YOUR_API_URL",
    "userid": "PASTE_USERID_HERE",
    "token": "PASTE_TOKEN_HERE"
  }'
```

Replace:
- `YOUR_GITHUB_USERNAME` → Your GitHub username
- `YOUR_API_URL` → Your KuGouMusicApi URL from deployment
- `PASTE_USERID_HERE` → The userid from step 1
- `PASTE_TOKEN_HERE` → The token from step 1

**Success response:**
```json
{
  "success": true,
  "message": "Kugou API credentials saved successfully!",
  "widget_url": "https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_GITHUB_USERNAME&theme=dark",
  "next_steps": [
    "Your widget will now show real-time listening history from Kugou",
    "Add to your GitHub README to see it in action",
    "Songs update automatically when you play on Kugou"
  ]
}
```

---

## Add to Your GitHub Profile

### 1. Edit Your Profile README

```bash
# Clone your profile repository
git clone https://github.com/YOUR_USERNAME/YOUR_USERNAME.git
cd YOUR_USERNAME

# Edit README.md
nano README.md
```

### 2. Add This Code

```markdown
## 🎵 Now Playing on Kugou

![Kugou Music](https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_GITHUB_USERNAME&theme=dark)
```

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

### 3. Commit and Push

```bash
git add README.md
git commit -m "Add Kugou music widget"
git push origin main
```

### 4. View Your Profile

Visit: `https://github.com/YOUR_USERNAME`

🎉 **Your profile now shows real-time Kugou listening history!**

---

## Complete Example (Copy-Paste Ready)

Replace these placeholders:
- `YOUR_GITHUB_USERNAME` → Your GitHub username
- `YOUR_PHONE` → Your Kugou phone number
- `YOUR_API_URL` → Will be shown after deployment

```bash
# ========================================
# 1. DEPLOY KUGOU API
# ========================================

cd ~
git clone https://github.com/MakcRe/KuGouMusicApi.git
cd KuGouMusicApi
npm install
vercel --prod

# Save the URL: https://kugou-music-api-xxxxx.vercel.app


# ========================================
# 2. LOGIN TO KUGOU
# ========================================

# Request verification code
curl "https://YOUR_API_URL/login/code?username=YOUR_PHONE"

# Check your SMS for the code, then verify
curl "https://YOUR_API_URL/login/verify?username=YOUR_PHONE&code=123456"

# Copy the userid and token from response


# ========================================
# 3. CONNECT TO WIDGET
# ========================================

curl -X POST https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app/setup-kugou \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_GITHUB_USERNAME",
    "api_url": "https://YOUR_API_URL",
    "userid": "PASTE_USERID_FROM_STEP_2",
    "token": "PASTE_TOKEN_FROM_STEP_2"
  }'


# ========================================
# 4. ADD TO GITHUB PROFILE
# ========================================

# Add this to your GitHub profile README.md:
# ![Kugou](https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_GITHUB_USERNAME&theme=dark)
```

---

## Troubleshooting

### "vercel: command not found"

Install Vercel CLI:
```bash
npm install -g vercel
```

### "npm: command not found"

Install Node.js and npm:
- **Ubuntu/Debian:** `sudo apt install nodejs npm`
- **macOS:** `brew install node`
- **Windows:** Download from https://nodejs.org/

### "Error: Cannot find module"

Ensure dependencies are installed:
```bash
cd KuGouMusicApi
npm install
```

### API Returns 404

Make sure you're using the correct endpoint format:
```
https://YOUR_API_URL/login/code?username=PHONE
```

NOT:
```
https://YOUR_API_URL/api/login/code  ❌ (wrong path)
```

### Widget Still Shows Demo Song

1. **Check credentials are saved:**
   ```bash
   curl "https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app/test?user_id=YOUR_GITHUB_USERNAME"
   ```

2. **Look for:** `"kugou_api": "Configured"`

3. **If not configured,** re-run step 3 (Connect to Widget)

---

## Next Steps

### Test Real-Time Sync

1. **Play a song on Kugou mobile app**
2. **Wait 30 seconds** (for Kugou to register the play)
3. **Refresh your GitHub profile** (Ctrl+F5 or Cmd+Shift+R)
4. **Widget should show your new song!**

### Setup Automatic Sync (Optional)

See: [KUGOU_API_INTEGRATION.md](KUGOU_API_INTEGRATION.md#automatic-sync-optional)

Create a cron job to sync every 5 minutes:
```bash
*/5 * * * * cd /path/to/kugou-widget && ./sync_kugou_listening.py
```

---

## Summary

✅ **Your Widget:** https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app

🔲 **KuGouMusicApi:** Deploy using script or manual steps above

🔲 **Login:** Get userid and token from KuGouMusicApi

🔲 **Connect:** Save credentials to widget via `/setup-kugou`

🔲 **GitHub:** Add widget to your profile README

---

## Need Help?

- **Detailed guide:** [KUGOU_API_INTEGRATION.md](KUGOU_API_INTEGRATION.md)
- **Quick setup:** [QUICK_SETUP.md](QUICK_SETUP.md)
- **Issues:** Open an issue on GitHub

---

**Time to complete:** ~10 minutes  
**Result:** Real-time Kugou listening history on your GitHub profile! 🎵
