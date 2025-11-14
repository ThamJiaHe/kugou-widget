#!/bin/bash
# Test your newly deployed widget

URL="https://kugou-widget-8cmxi0zsz-cv4tkg1uav-gmailcoms-projects.vercel.app"

echo "Testing your Kugou Widget..."
echo ""

# Test 1: Health check
echo "1. Health Check:"
curl -s "$URL/health"
echo ""
echo ""

# Test 2: Widget SVG
echo "2. Widget Output (first 200 chars):"
curl -s "$URL?user_id=demo&theme=dark" | head -c 200
echo ""
echo "..."
echo ""

# Test 3: Does it return SVG?
echo "3. Validation:"
RESPONSE=$(curl -s "$URL?user_id=demo&theme=dark")
if echo "$RESPONSE" | grep -q "^<svg"; then
    echo "✅ SUCCESS! Widget returns SVG"
    echo ""
    echo "🎉 Your widget is working!"
    echo ""
    echo "Add this to your GitHub README:"
    echo ""
    echo "![Kugou Music]($URL?user_id=demo&theme=dark)"
    echo ""
else
    echo "❌ Widget not returning SVG"
    echo "Full response:"
    echo "$RESPONSE"
fi
