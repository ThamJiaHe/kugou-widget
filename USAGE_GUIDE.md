# 🎵 Kugou Widget Usage Guide

Your Kugou "Now Playing" widget is live! Here's how to use it.

## 🚀 Quick Start (3 Minutes)

### Step 1: Add to Your GitHub Profile

1. **Create/Edit your profile README:**
   ```bash
   # If you don't have a profile repo yet, create one
   # Repo name MUST match your username
   cd ~/
   git clone https://github.com/YOUR_USERNAME/YOUR_USERNAME.git
   cd YOUR_USERNAME
   
   # Or just edit on GitHub web interface
   ```

2. **Add this to your README.md:**
   ```markdown
   ## 🎵 Currently Listening To
   
   <div align="center">
     <img src="https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark" alt="Kugou Now Playing" width="500"/>
   </div>
   ```

3. **Commit and push:**
   ```bash
   git add README.md
   git commit -m "Add Kugou now playing widget"
   git push
   ```

4. **View your profile:** Visit `github.com/YOUR_USERNAME` - You'll see the widget!

---

## 🎯 Setup Your Own User ID (Not Demo)

### Option 1: Using Firebase Console (Easiest)

1. **Open Firebase Console:**
   - Go to your Firebase project
   - Click "Realtime Database" in left sidebar
   - Click "Data" tab

2. **Create your user node:**
   - Click `+` next to `/users`
   - Name: `YOUR_GITHUB_USERNAME` (use your actual GitHub username)
   - Click `+` to add child: `current_song`
   - Add these fields:
     ```
     name: "晴天"
     artist: "周杰伦"
     cover: "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"
     updated_at: 1731575100000
     ```

3. **Update your README:**
   ```markdown
   <img src="https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_GITHUB_USERNAME&theme=dark" alt="Kugou Now Playing" width="500"/>
   ```

### Option 2: Using the Update Script (Recommended)

1. **Configure the script:**
   Edit `update_song.py` and change:
   ```python
   USER_ID = "YOUR_GITHUB_USERNAME"  # Change this!
   ```

2. **Install dependencies:**
   ```bash
   pip install requests
   ```

3. **Update your first song:**
   ```bash
   python update_song.py "晴天" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"
   ```

4. **Update your README with your user ID**

---

## 🎨 Customization Options

### Theme Options

**Dark Theme (Default):**
```markdown
<img src="https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_ID&theme=dark" width="500"/>
```

**Light Theme:**
```markdown
<img src="https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_ID&theme=light" width="500"/>
```

**Auto-Switch Theme (GitHub Dark/Light Mode):**
```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" 
          srcset="https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_ID&theme=dark">
  <source media="(prefers-color-scheme: light)" 
          srcset="https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_ID&theme=light">
  <img alt="Kugou Now Playing" 
       src="https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_ID&theme=dark" 
       width="500">
</picture>
```

### Size Options

```markdown
<!-- Small (400px) -->
<img src="..." width="400"/>

<!-- Medium (500px) - Recommended -->
<img src="..." width="500"/>

<!-- Large (600px) -->
<img src="..." width="600"/>

<!-- Extra Large (800px) -->
<img src="..." width="800"/>
```

### Advanced Parameters

Add these to the URL:

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `user_id` | string | required | Your unique user ID |
| `theme` | `light`, `dark` | `light` | Color theme |
| `width` | number | `400` | Widget width in pixels |
| `height` | number | `120` | Widget height in pixels |
| `show_album` | `true`, `false` | `true` | Show album art |

**Example with all parameters:**
```
https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=YOUR_ID&theme=dark&width=600&height=150&show_album=true
```

---

## 🔄 Updating Your Song

### Method 1: Using update_song.py (Easiest)

```bash
# Basic update
python update_song.py "Song Name" "Artist Name"

# With album art
python update_song.py "晴天" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"

# See SONGS.md for ready-to-use commands
```

### Method 2: Using curl (Command Line)

```bash
curl -X POST https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app/update \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_USERNAME",
    "song_name": "晴天",
    "artist_name": "周杰伦",
    "cover_url": "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"
  }'
```

### Method 3: Direct Firebase Edit

1. Open Firebase Console → Realtime Database
2. Navigate to `users/YOUR_USERNAME/current_song`
3. Click pencil icon to edit
4. Update `name`, `artist`, `cover` fields
5. Widget updates instantly!

---

## 📋 Workflow Examples

### Daily Music Update Workflow

**Morning:**
```bash
python update_song.py "晴天" "周杰伦"
```

**Afternoon:**
```bash
python update_song.py "告白气球" "周杰伦"
```

**Evening:**
```bash
python update_song.py "夜曲" "周杰伦"
```

### Quick Switch Between Favorites

Create a shell script `quick_songs.sh`:
```bash
#!/bin/bash
case $1 in
  1) python update_song.py "晴天" "周杰伦" "https://..." ;;
  2) python update_song.py "青花瓷" "周杰伦" "https://..." ;;
  3) python update_song.py "稻香" "周杰伦" "https://..." ;;
  *) echo "Usage: ./quick_songs.sh [1-3]" ;;
esac
```

Use: `./quick_songs.sh 1`

---

## 🎵 Popular Songs Ready to Use

See [SONGS.md](./SONGS.md) for a complete list of Jay Chou songs with album art URLs.

**Quick favorites:**
```bash
# Top 5 Jay Chou Songs
python update_song.py "晴天" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"
python update_song.py "告白气球" "周杰伦" "https://imge.kugou.com/stdmusic/240/20170418/20170418173403349763.jpg"
python update_song.py "青花瓷" "周杰伦" "https://imge.kugou.com/stdmusic/240/20160818/20160818112845056710.jpg"
python update_song.py "稻香" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150719/20150719205742894772.jpg"
python update_song.py "七里香" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120645762966.jpg"
```

---

## 🔧 Troubleshooting

### Widget Not Showing

**Check:**
1. ✅ Is the Vercel URL correct in your README?
2. ✅ Is your user_id spelled correctly?
3. ✅ Did you create the user in Firebase?
4. ✅ Try the demo first: `?user_id=demo`

**Test widget URL directly:**
```
https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo
```

### Song Not Updating

**Check:**
1. ✅ Firebase rules allow writes
2. ✅ user_id matches between script and Firebase
3. ✅ Check script output for errors
4. ✅ Verify Firebase data was updated

**View Firebase data:**
```
https://console.firebase.google.com/project/YOUR_PROJECT/database/data
```

### Image Not Loading

**Check:**
1. ✅ Use HTTPS URLs (not HTTP)
2. ✅ Test image URL in browser
3. ✅ Kugou CDN works best: `imge.kugou.com`
4. ✅ Try without image first (use default)

---

## 💡 Pro Tips

### 1. Create Keyboard Shortcuts

**Mac: Use Automator/Alfred**
```applescript
-- Create Quick Action in Automator
tell application "Terminal"
    do script "cd ~/kugou-widget && python update_song.py 'Song' 'Artist'"
end tell
```

### 2. Add to VS Code Tasks

`.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Update Kugou Widget",
      "type": "shell",
      "command": "python",
      "args": ["update_song.py", "${input:song}", "${input:artist}"],
      "presentation": {
        "reveal": "always"
      }
    }
  ],
  "inputs": [
    {
      "id": "song",
      "type": "promptString",
      "description": "Song name"
    },
    {
      "id": "artist",
      "type": "promptString",
      "description": "Artist name"
    }
  ]
}
```

### 3. Create a Web Interface

Build a simple HTML page to update songs via browser!

### 4. Schedule Updates

Use cron to rotate through favorite songs:
```bash
# Crontab: Rotate songs every 6 hours
0 */6 * * * cd ~/kugou-widget && python rotate_songs.py
```

---

## 🌟 Showcase Ideas

### Creative Uses

**1. Music Mood Board:**
```markdown
## My Current Vibe 🎵

<img src="...?user_id=YOUR_ID&theme=dark" width="500"/>

> Currently vibing to this masterpiece!
```

**2. Multiple Widgets:**
```markdown
## My Music Journey 🎶

**Now Playing:**
<img src="...?user_id=now_playing" width="400"/>

**Recently Played:**
<img src="...?user_id=recent" width="400"/>
```

**3. Themed Sections:**
```markdown
## 🌙 Night Time Playlist

<img src="...?user_id=night_songs&theme=dark" width="500"/>

## ☀️ Morning Motivation

<img src="...?user_id=morning_songs&theme=light" width="500"/>
```

---

## 📊 Monitoring

### Check Widget Health

```bash
# Health check endpoint
curl https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app/health

# Check your user data
curl https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app/user/YOUR_USERNAME
```

### View Logs

```bash
# View Vercel deployment logs
vercel logs

# Or view in dashboard
https://vercel.com/dashboard
```

---

## 🚀 Advanced: Auto-Update (Future)

### Option 1: Kugou Desktop Watcher

Build a local script that watches Kugou desktop app and auto-updates (advanced, requires reverse engineering).

### Option 2: Last.fm Integration

Scrobble to Last.fm → Fetch from Last.fm API → Update widget (easier, but requires Last.fm account).

### Option 3: Manual is Perfect!

For most users, **manual updates take 30 seconds** and give you full control. Perfect for showing off your favorite songs!

---

## 📚 Additional Resources

- **Main README:** [README.md](./README.md) - Full project documentation
- **Songs Database:** [SONGS.md](./SONGS.md) - Ready-to-use songs with album art
- **Update Script:** [update_song.py](./update_song.py) - Easy song updates
- **Deployment Guide:** [DEPLOYMENT.md](./DEPLOYMENT.md) - Technical setup details

---

## ✅ Quick Checklist

- [ ] Widget added to GitHub profile README
- [ ] Created my user ID in Firebase  
- [ ] Configured update_song.py with my username
- [ ] Updated widget with my favorite song
- [ ] Tested widget appears on my profile
- [ ] Bookmarked quick update commands from SONGS.md

---

**🎉 Congratulations! Your widget is live!**

Update it whenever you listen to new music and show off your taste! 🎵
