# Fix Widget Loading Issues

Your widget URL: **https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app**

If the widget isn't loading on GitHub (showing "Kugou Music" alt text instead of the SVG), follow these fixes.

---

## 🔍 Step 1: Diagnose the Problem

Run the diagnostic script:

```bash
chmod +x diagnose_widget.sh
./diagnose_widget.sh
```

This will identify the exact issue. Continue based on the results.

---

## 🔥 Most Common Issue: Firebase Not Connected

### Symptoms
- Health check shows: `"firebase": "error"` or `"firebase": false`
- Widget returns error instead of SVG
- Diagnostic script shows: "❌ Firebase Not Connected"

### Fix: Add Firebase to Vercel

#### 1. Get Firebase Credentials

**Option A: Create New Firebase Project (5 minutes)**

1. Go to https://console.firebase.google.com
2. Click "Add project"
3. Name it: `kugou-widget`
4. Disable Google Analytics (optional)
5. Click "Create project"

**Get the credentials:**

1. Click gear icon ⚙️ → **Project settings**
2. Go to **Service accounts** tab
3. Click **Generate new private key**
4. Download the JSON file (save it!)
5. Note your Database URL (e.g., `https://kugou-widget-xxxxx.firebaseio.com`)

**Enable Realtime Database:**

1. In Firebase Console, click **Build** → **Realtime Database**
2. Click **Create Database**
3. Choose location (closest to you)
4. Start in **test mode** (we'll secure it later)
5. Click **Enable**

#### 2. Add Credentials to Vercel

**Via Vercel CLI (Recommended):**

```bash
# Add Firebase credentials (paste entire JSON)
vercel env add FIREBASE_CREDENTIALS production

# When prompted, paste the ENTIRE content of your service account JSON file
# Example:
# {"type":"service_account","project_id":"kugou-widget-12345",...}

# Add database URL
vercel env add FIREBASE_DATABASE_URL production

# When prompted, enter your Firebase database URL:
# https://kugou-widget-xxxxx.firebaseio.com
```

**Via Vercel Dashboard:**

1. Go to https://vercel.com/dashboard
2. Click your project: **kugou-widget**
3. Go to **Settings** → **Environment Variables**
4. Add two variables:

**Variable 1:**
- **Name:** `FIREBASE_CREDENTIALS`
- **Value:** Paste entire JSON from service account file
- **Environment:** Production (check the box)
- Click **Save**

**Variable 2:**
- **Name:** `FIREBASE_DATABASE_URL`  
- **Value:** `https://kugou-widget-xxxxx.firebaseio.com`
- **Environment:** Production (check the box)
- Click **Save**

#### 3. Redeploy

```bash
cd /workspaces/kugou-widget
vercel --prod
```

Wait for deployment to complete (~30 seconds).

#### 4. Verify Fix

```bash
# Test health endpoint
curl "https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app/health"

# Should show: {"firebase": "connected"}
```

```bash
# Test widget
curl "https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark"

# Should return SVG code starting with: <svg width=...
```

#### 5. Add Demo Data to Firebase

Now add demo song data so the widget has something to display:

1. Go to Firebase Console → **Realtime Database**
2. Click the **+** icon next to the root
3. In **Name**, enter: `users`
4. In **Value**, enter: `{"demo": {"current_song": {}}}`
5. Click **Add**

Now expand the tree and add demo song:

```json
users/
  demo/
    current_song/
      name: "告白气球"
      artist: "周杰伦"
      cover: "https://imge.kugou.com/stdmusic/240/20170418/20170418173403349763.jpg"
      updated_at: 1731575100
```

**Or import this complete JSON:**

Click the **⋮** menu → **Import JSON** → Paste:

```json
{
  "users": {
    "demo": {
      "current_song": {
        "name": "告白气球",
        "artist": "周杰伦",
        "cover": "https://imge.kugou.com/stdmusic/240/20170418/20170418173403349763.jpg",
        "updated_at": 1731575100
      }
    }
  }
}
```

#### 6. Test Again

```bash
./diagnose_widget.sh
```

Should now show: ✅ No issues found!

---

## 🔧 Issue 2: SVG Generation Error

### Symptoms
- Firebase is connected
- But widget still returns error or blank

### Fix: Verify SVG Generator

Check if `api/svg_generator.py` exists and has no syntax errors:

```bash
cd /workspaces/kugou-widget
python3 -m py_compile api/svg_generator.py

# If no error, file is valid
```

If there's an error, the SVG generator has issues. Let me know the error and I'll fix it.

---

## 🌐 Issue 3: CORS Headers

### Symptoms
- Widget works when you visit URL directly
- But doesn't load on GitHub

### Fix: Ensure CORS Headers Are Set

The `api/index.py` file should already have CORS headers. Verify:

```bash
grep -A 2 "Access-Control-Allow-Origin" api/index.py
```

Should show:
```python
'Access-Control-Allow-Origin': '*'
```

If missing, I'll add them.

---

## 🎯 Issue 4: GitHub Image Caching

### Symptoms
- Widget works when you visit URL directly
- All diagnostic tests pass
- But GitHub still shows old/broken image

### Fix: Clear GitHub's Cache

**Method 1: Add Cache Busting Parameter**

Change your README from:
```markdown
![Kugou Music](https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark)
```

To:
```markdown
![Kugou Music](https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark&v=2)
```

Change `v=2` to `v=3`, `v=4`, etc. each time you need to force refresh.

**Method 2: Wait for Cache Expiration**

GitHub caches images for ~5 minutes. Just wait and hard refresh your profile.

**Method 3: Hard Refresh**

- **Windows/Linux:** Ctrl + F5
- **Mac:** Cmd + Shift + R

---

## ✅ Complete Fix Checklist

Run through this checklist:

- [ ] **Firebase credentials added to Vercel**
  ```bash
  vercel env ls
  # Should show FIREBASE_CREDENTIALS and FIREBASE_DATABASE_URL
  ```

- [ ] **Firebase database created and demo data added**
  ```bash
  # Visit Firebase Console and verify database exists
  ```

- [ ] **Redeployed after adding environment variables**
  ```bash
  vercel --prod
  ```

- [ ] **Health check passes**
  ```bash
  curl https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app/health | grep "firebase.*connected"
  ```

- [ ] **Widget returns SVG**
  ```bash
  curl https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo | grep "<svg"
  ```

- [ ] **Diagnostic script shows no issues**
  ```bash
  ./diagnose_widget.sh
  ```

- [ ] **GitHub README updated with cache-busting parameter**
  ```markdown
  ?user_id=demo&theme=dark&v=2
  ```

---

## 🚑 Quick Emergency Fix (No Firebase)

If you just want to test the widget working WITHOUT Firebase:

### Update `api/index.py` to work without Firebase:

The code already has demo mode that works without Firebase! Just make sure you're using `user_id=demo`:

```markdown
![Kugou Music](https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark)
```

The demo mode doesn't require Firebase and shows cycling demo songs.

---

## 📞 Still Not Working?

### Collect Debug Information

Run this and share the output:

```bash
./diagnose_widget.sh

# Also check Vercel logs:
vercel logs https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app
```

### Check Vercel Function Logs

1. Go to https://vercel.com/dashboard
2. Click your project
3. Click **Functions** tab
4. Look for errors in the logs

### Test Locally

```bash
cd /workspaces/kugou-widget

# Set environment variables
export FIREBASE_CREDENTIALS='{"type":"service_account",...}'
export FIREBASE_DATABASE_URL='https://your-project.firebaseio.com'

# Run locally
python api/index.py

# Visit: http://localhost:5000?user_id=demo
```

If it works locally but not on Vercel → environment variable issue.

---

## 🎉 Success Criteria

Your widget is working when:

✅ Health endpoint returns: `{"status": "healthy", "firebase": "connected"}`  
✅ Widget URL returns SVG code (not error)  
✅ Diagnostic script shows: "No issues found"  
✅ GitHub README shows the widget image  

---

## Common Error Messages & Fixes

### "Application Error"
- **Cause:** Server crash, missing dependencies
- **Fix:** Check Vercel function logs for Python errors

### "500 Internal Server Error"
- **Cause:** Code exception in `api/index.py`
- **Fix:** Check logs with `vercel logs`

### "Missing user_id parameter"
- **Cause:** URL doesn't have `?user_id=demo`
- **Fix:** Add `?user_id=demo` to your URL

### "Firebase not initialized"
- **Cause:** Missing FIREBASE_CREDENTIALS env var
- **Fix:** Follow Issue #1 fix above

---

**Need more help?** Open an issue with the output of `./diagnose_widget.sh`
