# Widget Not Loading? Start Here! 🔧

Your widget is deployed at:
**https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app**

If you see "Kugou Music" text instead of the widget image on GitHub, follow these steps.

---

## 🚀 Quick Fix (2 minutes)

### Step 1: Run Quick Test

```bash
chmod +x quick_test.sh
./quick_test.sh
```

This will tell you if Firebase is connected or not.

### Step 2: If Firebase is Missing

**You'll see:** `❌ Firebase is NOT connected`

**Fix it:**

```bash
# Add Firebase credentials to Vercel
vercel env add FIREBASE_CREDENTIALS production
# Paste your Firebase service account JSON when prompted

vercel env add FIREBASE_DATABASE_URL production
# Enter your Firebase database URL when prompted

# Redeploy
vercel --prod
```

**Where to get these?**
1. Go to https://console.firebase.google.com
2. Create a new project (or use existing)
3. Get service account JSON: Settings ⚙️ → Service accounts → Generate new private key
4. Get database URL: Realtime Database section (e.g., `https://your-project.firebaseio.com`)

### Step 3: Test Again

```bash
./quick_test.sh
```

Should now show: `✅ Widget returns SVG`

### Step 4: Update GitHub README

```markdown
![Kugou Music](https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark&v=1)
```

**Note:** Change `v=1` to `v=2` if GitHub still shows old cached image.

---

## 📚 Need More Help?

### Full Diagnostic

```bash
chmod +x diagnose_widget.sh
./diagnose_widget.sh
```

This runs a complete health check and tells you exactly what's wrong.

### Detailed Troubleshooting

See **[FIX_WIDGET_LOADING.md](FIX_WIDGET_LOADING.md)** for:
- Firebase setup step-by-step
- CORS issues
- GitHub caching problems
- Error message explanations

### Test in Browser

Visit directly to see if it works:
```
https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark
```

**Should show:** SVG widget with song info  
**If you see error page:** Firebase not connected (see Step 2 above)

---

## ✅ Checklist

- [ ] Run `./quick_test.sh` → Should pass all tests
- [ ] Firebase credentials added to Vercel
- [ ] Redeployed with `vercel --prod`
- [ ] Widget URL returns SVG (not error)
- [ ] GitHub README has correct URL with cache-busting `?v=1`

---

## 🎯 Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Kugou Music" text only | Firebase not connected | Add Firebase env vars |
| Error page when visiting URL | Missing credentials | `vercel env add FIREBASE_CREDENTIALS` |
| Works in browser, not GitHub | Image caching | Add `?v=2` to URL |
| "Application Error" | Deployment issue | Check `vercel logs` |

---

## 💡 Pro Tip: Test Without Firebase

Want to test immediately without setting up Firebase?

The widget already has built-in demo mode that works without Firebase!

Just make sure your URL has `?user_id=demo`:

```markdown
![Kugou Music](https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app?user_id=demo&theme=dark)
```

This should work immediately even without Firebase setup.

If even this doesn't work, there's a deployment issue. Run `./diagnose_widget.sh` to investigate.

---

**Still stuck?** Run `./diagnose_widget.sh` and open an issue with the output.
