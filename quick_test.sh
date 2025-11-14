#!/bin/bash
#
# Quick Widget Test
# Fast check if your widget is working
#

URL="https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app"

echo "🔍 Quick Widget Test"
echo ""

# Test 1: Can we reach the API?
echo "1️⃣ Testing connection..."
if curl -s -f "$URL/health" > /dev/null 2>&1; then
    echo "✅ API is reachable"
else
    echo "❌ Cannot reach API"
    exit 1
fi

# Test 2: Is Firebase connected?
echo ""
echo "2️⃣ Checking Firebase..."
HEALTH=$(curl -s "$URL/health")
if echo "$HEALTH" | grep -q "firebase.*true\|firebase.*connected"; then
    echo "✅ Firebase is connected"
elif echo "$HEALTH" | grep -q "firebase.*false\|firebase.*error"; then
    echo "❌ Firebase is NOT connected"
    echo ""
    echo "🔧 Fix this by adding Firebase credentials to Vercel:"
    echo "   1. vercel env add FIREBASE_CREDENTIALS production"
    echo "   2. vercel env add FIREBASE_DATABASE_URL production"
    echo "   3. vercel --prod"
    echo ""
    echo "📖 See: FIX_WIDGET_LOADING.md for detailed instructions"
    exit 1
else
    echo "⚠️  Firebase status unclear"
fi

# Test 3: Does the widget return SVG?
echo ""
echo "3️⃣ Testing widget output..."
WIDGET=$(curl -s "$URL?user_id=demo&theme=dark")
if echo "$WIDGET" | grep -q "^<svg"; then
    echo "✅ Widget returns SVG"
    echo ""
    echo "🎉 Your widget is working!"
    echo ""
    echo "Add this to your GitHub README:"
    echo ""
    echo "![Kugou Music]($URL?user_id=demo&theme=dark)"
    echo ""
else
    echo "❌ Widget does NOT return SVG"
    echo ""
    echo "First 200 characters of response:"
    echo "${WIDGET:0:200}"
    echo ""
    echo "🔧 Run full diagnostics: ./diagnose_widget.sh"
    exit 1
fi

# Test 4: Open in browser
echo "4️⃣ Want to see it in your browser?"
echo ""
echo "Visit this URL:"
echo "$URL?user_id=demo&theme=dark"
echo ""
echo "Or run: xdg-open '$URL?user_id=demo&theme=dark' 2>/dev/null || open '$URL?user_id=demo&theme=dark' 2>/dev/null"
echo ""
