# kugou-widget

A serverless widget to showcase Kugou user's now playing track.

> ⚠️ **Important**: This project uses unofficial Kugou APIs for educational purposes only. The API may break with Kugou updates. For production use, consider using Spotify or Last.fm instead.

## 🚀 Quick Start (Works Immediately!)

**Want to see it working now?** Use demo mode:

```markdown
![Kugou Demo](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark)
```

This shows rotating demo songs and works without any setup.

## Features

- 🎵 **Three modes**: Demo data, Manual updates, or Full API integration
- 🎨 **Customizable SVG** with light/dark themes  
- ⚡ **Serverless deployment** with Vercel
- 🔄 **Firebase integration** for credential storage
- 🛡️ **Secure token management**
- 📱 **Mobile-friendly** responsive design
- ⚠️ **Realistic expectations** - shows "recently played" not true "now playing"

## Reality Check: Limitations

### ❌ What Doesn't Work
- **True "Now Playing"**: Kugou doesn't expose real-time currently playing
- **Official API**: Uses reverse-engineered unofficial endpoints  
- **Automatic Updates**: No push notifications when songs change
- **Easy Setup**: Requires significant reverse engineering for full functionality

### ✅ What Actually Works
- **Demo Mode**: Works immediately with sample data
- **Manual Updates**: Update songs via API call
- **Custom Themes**: Light/dark themes with customization
- **Recent History**: Shows last played track (if you extract credentials)

## Quick Demo

![Demo Widget](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app/test?theme=dark)

## Four Ways to Use This

### 1. 🎬 Demo Mode (Works Now!)
Perfect for testing or showcasing the widget:

```markdown
![Kugou Widget](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark)
```

**Pros:** Works immediately, no setup  
**Cons:** Shows demo data, not your actual music

### 2. 🎵 KuGouMusicApi Integration (Recommended!)
**NEW!** Use the [KuGouMusicApi Node.js service](https://github.com/zkhssb/KuGouMusicApi) for real-time listening history:

```markdown
![Kugou Music](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_ID&theme=dark)
```

**Architecture:**
```
Your Kugou Account → KuGouMusicApi (Node.js) → This Widget → GitHub Profile
```

**Pros:** 
- ✅ Real Kugou listening history
- ✅ Reliable authentication handled by Node.js service
- ✅ Automatic updates from your Kugou account
- ✅ No complex Python authentication required

**Setup:** See [KUGOU_API_INTEGRATION.md](KUGOU_API_INTEGRATION.md) for complete guide

**Quick Setup:**
1. Deploy [KuGouMusicApi](https://github.com/zkhssb/KuGouMusicApi) to Vercel
2. Login to get your `userid` and `token`
3. Save credentials: `POST /setup-kugou`
4. Done! Widget shows real-time listening history

### 3. 🔄 Manual Update Mode (Semi-Automated) 
Update your current song via API call:

```bash
curl -X POST https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app/update \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your_id", 
    "song_name": "青花瓷",
    "artist_name": "周杰伦",
    "cover_url": "https://image.url"
  }'
```

Then use: `![Music](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=your_id)`

**Pros:** Shows your actual music, works reliably  
**Cons:** Manual updates required

### 4. 🔧 Direct API Mode (Advanced/Not Recommended)
Extract credentials directly from Kugou app:

**Pros:** No intermediary service  
**Cons:** Complex authentication, may break anytime

**Recommendation:** Use KuGouMusicApi integration (#2) instead!

## Step-by-Step Deployment

### Option A: Automatic Deployment (Recommended)

1. **Fork this repository** on GitHub

2. **Set up GitHub Actions secrets** (see [DEPLOYMENT.md](DEPLOYMENT.md)):
   - `VERCEL_TOKEN` - Your Vercel CLI token
   - `VERCEL_ORG_ID` - Your Vercel organization ID  
   - `VERCEL_PROJECT_ID` - Your Vercel project ID
   - `VERCEL_PROJECT_DOMAIN` - Your project domain (optional)

3. **Push to main branch** - automatic deployment via GitHub Actions:
   ```bash
   git add .
   git commit -m "Deploy Kugou widget"
   git push origin main
   ```

4. **Test immediately:**
   ```
   https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo
   ```

**Done!** Automatic deployments on every push to main.

### Option B: Manual Deployment (5 minutes)

1. **Fork this repository** on GitHub

2. **Deploy to Vercel:**
   ```bash
   npm i -g vercel
   vercel login
   vercel --prod
   ```

3. **Test immediately:**
   ```
   https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo
   ```

4. **Add to GitHub README:**
   ```markdown
   ![Kugou Music](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark)
   ```

**Done!** You now have a working widget with demo data.

### Option C: KuGouMusicApi Integration (Real-Time Sync!)

**NEW!** Connect to real Kugou listening history via [KuGouMusicApi](https://github.com/zkhssb/KuGouMusicApi).

See complete guide: **[KUGOU_API_INTEGRATION.md](KUGOU_API_INTEGRATION.md)**

**Quick steps:**

1. **Deploy KuGouMusicApi:**
   ```bash
   git clone https://github.com/zkhssb/KuGouMusicApi.git
   cd KuGouMusicApi
   vercel --prod
   # Save your API URL: https://your-kugou-api.vercel.app
   ```

2. **Login to Kugou:**
   ```bash
   curl "https://your-kugou-api.vercel.app/login/code?username=YOUR_PHONE"
   curl "https://your-kugou-api.vercel.app/login/verify?username=YOUR_PHONE&code=123456"
   # Save: userid and token
   ```

3. **Connect to widget:**
   ```bash
   curl -X POST https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app/setup-kugou \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "your_github_username",
       "api_url": "https://your-kugou-api.vercel.app",
       "userid": "123456789",
       "token": "abc123..."
     }'
   ```

4. **Add to GitHub README:**
   ```markdown
   ![Kugou Music](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=your_github_username&theme=dark)
   ```

**Result:** Widget now shows your real-time Kugou listening history! 🎵

**How it works:**
```
Your Kugou Account 
    ↓ (plays music)
KuGouMusicApi (Node.js on Vercel)
    ↓ (fetches history)
Python Widget (this repo)
    ↓ (generates SVG)
GitHub Profile README
```

For detailed instructions, troubleshooting, and automatic sync setup, see **[KUGOU_API_INTEGRATION.md](KUGOU_API_INTEGRATION.md)**.

### Option D: Add Manual Updates (10 minutes)

1. **Complete Option A or B first**

2. **Set up Firebase (optional, for persistence):**
   - Create [Firebase project](https://console.firebase.google.com)
   - Enable Realtime Database  
   - Generate service account key
   - Add to Vercel environment variables:
     - `FIREBASE_CREDENTIALS`: Paste entire JSON
     - `FIREBASE_DATABASE_URL`: Your database URL

3. **Update songs manually:**
   ```bash
   curl -X POST https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app/update \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "my_music",
       "song_name": "Current Song", 
       "artist_name": "Current Artist",
       "cover_url": "https://album-art-url.jpg"
     }'
   ```

4. **Update README to use your ID:**
   ```markdown
   ![My Music](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=my_music&theme=dark)
   ```

**Result:** Widget shows your manually updated current song.

### Option E: Full API Integration (2-4 hours)

⚠️ **Advanced users only** - requires reverse engineering

1. **Extract Kugou credentials:**
   - Install Kugou mobile app
   - Use network analysis tools (Burp Suite, mitmproxy)
   - Extract: `userid`, `token`, `dfid`, `mid`, `uuid`
   - Or use existing tools like [KuGouMusicApi](https://github.com/MakcRe/KuGouMusicApi)

2. **Store in Firebase:**
   ```json
   {
     "users": {
       "your_user_id": {
         "userid": "extracted_userid",
         "token": "extracted_token", 
         "dfid": "device_fingerprint",
         "mid": "machine_id",
         "uuid": "unique_id",
         "expires_at": 1699999999999
       }
     }
   }
   ```

3. **Widget will attempt to fetch from Kugou API**

**Warning:** This may stop working anytime Kugou updates their app.

## Usage Examples

### Basic Widget
```
https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo
```

### Customized Widget  
```
https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark&width=500&height=150&show_album=false
```

### Query Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `user_id` | Your user ID (required) | - | String |
| `theme` | Color theme | `light` | `light`, `dark` |
| `width` | Widget width | `400` | Number (px) |
| `height` | Widget height | `120` | Number (px) |  
| `show_album` | Show album art | `true` | `true`, `false` |

## API Endpoints

### Main Endpoints

- `GET /` - Main SVG widget endpoint
- `GET /health` - Service health check  
- `GET /test` - Test widget with sample data
- `GET /login` - Setup instructions and options
- `POST /update` - Manually update current song (requires Firebase)
- `POST /setup-kugou` - **NEW!** Configure KuGouMusicApi credentials for real-time sync

### Endpoint Details

**Main Widget: `GET /`**
```
GET /?user_id=demo&theme=dark&width=400&height=120&show_album=true
```

**KuGou API Setup: `POST /setup-kugou`** (NEW!)
```bash
curl -X POST /setup-kugou \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your_github_username",
    "api_url": "https://your-kugou-api.vercel.app",
    "userid": "123456789",
    "token": "abc123..."
  }'
```
See [KUGOU_API_INTEGRATION.md](KUGOU_API_INTEGRATION.md) for complete setup guide.

**Manual Update: `POST /update`**
```bash
curl -X POST /update \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your_id",
    "song_name": "Song Name",
    "artist_name": "Artist Name", 
    "cover_url": "https://cover.jpg"
  }'
```

**Health Check: `GET /health`**
```json
{
  "status": "healthy",
  "firebase_connected": true,
  "version": "1.0.0"
}
```

## Local Development & Testing

### Test Locally

1. **Clone and install:**
```bash
git clone https://github.com/YOUR_USERNAME/kugou-widget.git
cd kugou-widget
pip install -r api/requirements.txt
```

2. **Run locally:**
```bash
cd api && python index.py
# Or use Vercel CLI: vercel dev
```

3. **Test endpoints:**
```bash
# Test widget
curl http://localhost:5000/test

# Health check  
curl http://localhost:5000/health

# Demo widget
curl "http://localhost:5000?user_id=demo&theme=dark"
```

### Deploy and Test

1. **Deploy:**
```bash
vercel --prod
```

2. **Test deployment:**
```bash
# Health check
curl https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app/health

# Demo widget
curl "https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo"
```

3. **Add to GitHub README:**
```markdown
![Kugou Music](https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark)
```

## Troubleshooting

### Common Issues

**"Service temporarily unavailable"**
- Check Vercel function logs: `vercel logs`
- Verify deployment: `curl /health`
- Try demo mode first: `?user_id=demo`

**"Error loading widget"**  
- Firebase credentials missing/invalid
- Network connectivity issues
- Try test endpoint: `/test`

**"No song data"**
- For demo mode: Should always work
- For manual mode: Call `/update` first  
- For API mode: Check Firebase data structure

### Debugging Steps

1. **Test deployment health:**
   ```bash
   curl https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app/health
   ```

2. **Test with demo data:**
   ```bash
   curl "https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo"
   ```

3. **Check Vercel logs:**
   ```bash
   vercel logs
   ```

4. **Verify Firebase connection:**
   ```bash
   curl https://kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app/login
   ```

## Limitations & Challenges

### Technical Limitations

❌ **No Real-Time "Now Playing"**: Kugou doesn't expose this endpoint. Widget shows most recent track from listening history.

❌ **Unofficial API**: Can break anytime Kugou updates their app.

❌ **Complex Authentication**: Requires AES-256 encryption, RSA keys, MD5 signing.

❌ **Manual Token Management**: No automated refresh like Spotify OAuth.

❌ **Rate Limiting**: API may have undocumented rate limits.

### Legal Considerations

⚖️ **Terms of Service**: Using unofficial APIs may violate Kugou's ToS.

⚖️ **Educational Use Only**: This project is for learning purposes.

⚖️ **No Commercial Use**: Don't use this commercially.

## Troubleshooting

### Common Issues

**"Missing user_id parameter"**
- Add `?user_id=YOUR_ID` to the URL

**"Service temporarily unavailable"** 
- Check Firebase credentials
- Verify Kugou tokens are valid
- Check Vercel function logs

**"Error loading widget"**
- Tokens may be expired
- API endpoints may have changed
- Network connectivity issues

### Debugging

1. Check Vercel function logs
2. Test `/health` endpoint  
3. Verify Firebase database structure
4. Test with `/test` endpoint first

## Comparison: Kugou vs Spotify

| Aspect | Spotify | Kugou |
|--------|---------|-------|
| **Setup Time** | 5 minutes | 2-4 hours |
| **API Type** | Official OAuth2 | Unofficial + encryption |
| **Real-time** | ✅ True "now playing" | ❌ Recent history only |
| **Stability** | ✅ Highly stable | ❌ May break anytime |
| **Maintenance** | ✅ Zero maintenance | ❌ High maintenance |
| **Legal** | ✅ Commercial friendly | ❌ Educational only |

## Recommended Alternatives

### 1. Spotify (Recommended)
- Use [spotify-github-profile](https://github.com/kittinan/spotify-github-profile)
- Official API, 5-minute setup
- Real-time updates

### 2. Last.fm Integration
- Set up Last.fm scrobbling from Kugou
- Use Last.fm's official API
- More stable than direct Kugou integration

### 3. Manual Updates
- Create static SVG
- Update manually when songs change
- No API complexity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Areas for contribution:**
- Improved authentication flow
- Better error handling
- Additional themes
- API stability improvements

## Security Notes

🔒 **Never commit real credentials** to version control

🔒 **Use environment variables** for all secrets

🔒 **Rotate tokens regularly** if possible

🔒 **Monitor for API changes** that might break authentication

## License

MIT License - see LICENSE file for details.

**Disclaimer**: This project is not affiliated with Kugou Music. Use at your own risk and in accordance with Kugou's Terms of Service.

---

*For a simpler, more reliable solution, consider using [Spotify widgets](https://github.com/kittinan/spotify-github-profile) instead.*
