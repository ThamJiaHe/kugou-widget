#!/bin/bash
#
# Kugou Widget Diagnostic Script
# Helps identify why the widget isn't loading
#

set -e

URL="https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "=========================================="
echo "  🔍 Kugou Widget Diagnostics"
echo "=========================================="
echo ""
echo "Widget URL: $URL"
echo ""

# Test 1: Health Check
echo -e "${BLUE}Test 1: Health Check${NC}"
echo "Endpoint: /health"
echo ""
HEALTH=$(curl -s "$URL/health" 2>&1)
echo "Response:"
echo "$HEALTH" | jq '.' 2>/dev/null || echo "$HEALTH"
echo ""

if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✓ API is responding${NC}"
else
    echo -e "${RED}✗ API health check failed${NC}"
fi

if echo "$HEALTH" | grep -q "firebase.*connected"; then
    echo -e "${GREEN}✓ Firebase is connected${NC}"
    FIREBASE_OK=true
elif echo "$HEALTH" | grep -q "firebase.*error\|firebase.*false"; then
    echo -e "${RED}✗ Firebase is NOT connected${NC}"
    echo -e "${YELLOW}⚠️  This is likely your issue!${NC}"
    FIREBASE_OK=false
else
    echo -e "${YELLOW}⚠️  Firebase status unclear${NC}"
    FIREBASE_OK=false
fi
echo ""

# Test 2: Widget Endpoint (Demo)
echo -e "${BLUE}Test 2: Widget Endpoint (Demo Mode)${NC}"
echo "Endpoint: /?user_id=demo&theme=dark"
echo ""
WIDGET=$(curl -s "$URL?user_id=demo&theme=dark" 2>&1)
WIDGET_FIRST_100="${WIDGET:0:100}"
echo "First 100 characters:"
echo "$WIDGET_FIRST_100"
echo ""

if echo "$WIDGET" | grep -q "<svg"; then
    echo -e "${GREEN}✓ Widget returns SVG!${NC}"
    SVG_OK=true
elif echo "$WIDGET" | grep -q -i "error\|exception\|traceback"; then
    echo -e "${RED}✗ Widget returns error${NC}"
    echo ""
    echo "Full error response:"
    echo "$WIDGET"
    SVG_OK=false
elif echo "$WIDGET" | grep -q "<html"; then
    echo -e "${RED}✗ Widget returns HTML error page${NC}"
    echo ""
    echo "Full response:"
    echo "$WIDGET"
    SVG_OK=false
else
    echo -e "${RED}✗ Widget returns unexpected content${NC}"
    echo ""
    echo "Full response (first 500 chars):"
    echo "${WIDGET:0:500}"
    SVG_OK=false
fi
echo ""

# Test 3: Test Endpoint
echo -e "${BLUE}Test 3: Test Endpoint${NC}"
echo "Endpoint: /test"
echo ""
TEST=$(curl -s "$URL/test" 2>&1)
TEST_FIRST_100="${TEST:0:100}"
echo "First 100 characters:"
echo "$TEST_FIRST_100"
echo ""

if echo "$TEST" | grep -q "<svg"; then
    echo -e "${GREEN}✓ Test endpoint works${NC}"
else
    echo -e "${RED}✗ Test endpoint failed${NC}"
fi
echo ""

# Test 4: Check if it's an SVG rendering issue
echo -e "${BLUE}Test 4: SVG Structure Check${NC}"
if [ "$SVG_OK" = true ]; then
    echo "Checking SVG structure..."
    
    if echo "$WIDGET" | grep -q "xmlns"; then
        echo -e "${GREEN}✓ SVG has proper namespace${NC}"
    else
        echo -e "${YELLOW}⚠️  SVG missing namespace${NC}"
    fi
    
    if echo "$WIDGET" | grep -q "width="; then
        echo -e "${GREEN}✓ SVG has width attribute${NC}"
    else
        echo -e "${YELLOW}⚠️  SVG missing width${NC}"
    fi
    
    if echo "$WIDGET" | grep -q "height="; then
        echo -e "${GREEN}✓ SVG has height attribute${NC}"
    else
        echo -e "${YELLOW}⚠️  SVG missing height${NC}"
    fi
else
    echo -e "${YELLOW}Skipped (widget doesn't return SVG)${NC}"
fi
echo ""

# Test 5: CORS Headers
echo -e "${BLUE}Test 5: CORS Headers${NC}"
HEADERS=$(curl -sI "$URL?user_id=demo&theme=dark" 2>&1)
echo "Response headers:"
echo "$HEADERS" | grep -i "access-control\|content-type\|cache-control"
echo ""

if echo "$HEADERS" | grep -qi "access-control-allow-origin"; then
    echo -e "${GREEN}✓ CORS headers present${NC}"
else
    echo -e "${YELLOW}⚠️  CORS headers may be missing${NC}"
fi

if echo "$HEADERS" | grep -qi "content-type.*svg"; then
    echo -e "${GREEN}✓ Content-Type is image/svg+xml${NC}"
else
    echo -e "${RED}✗ Content-Type is not SVG${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo "  📊 Diagnostic Summary"
echo "=========================================="
echo ""

ISSUES_FOUND=0

if [ "$FIREBASE_OK" = false ]; then
    echo -e "${RED}❌ Issue Found: Firebase Not Connected${NC}"
    echo "   Solution: Add Firebase credentials to Vercel environment variables"
    echo "   See: Fix #1 in the instructions"
    echo ""
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ "$SVG_OK" = false ]; then
    echo -e "${RED}❌ Issue Found: Widget Not Returning SVG${NC}"
    echo "   This could be due to:"
    echo "   - Missing Firebase connection (check above)"
    echo "   - Error in SVG generation code"
    echo "   - Missing dependencies"
    echo ""
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}✅ No issues found!${NC}"
    echo ""
    echo "Your widget appears to be working correctly."
    echo "If it's not showing on GitHub:"
    echo "  1. GitHub may be caching the old image (wait 5 minutes)"
    echo "  2. Try hard refresh (Ctrl+F5 or Cmd+Shift+R)"
    echo "  3. Add cache busting parameter: ?user_id=demo&v=2"
else
    echo "Found $ISSUES_FOUND issue(s)"
    echo ""
    echo "🔧 Next Steps:"
    echo ""
    
    if [ "$FIREBASE_OK" = false ]; then
        echo "1️⃣ Set up Firebase (MOST IMPORTANT):"
        echo "   vercel env add FIREBASE_CREDENTIALS"
        echo "   vercel env add FIREBASE_DATABASE_URL"
        echo "   vercel --prod  # Redeploy"
        echo ""
    fi
    
    echo "📚 For detailed instructions, see:"
    echo "   - FIX_WIDGET_LOADING.md (comprehensive guide)"
    echo "   - DEPLOYMENT_COMPLETE.md (setup instructions)"
fi

echo ""
echo "=========================================="
echo ""

# Save output to file
LOG_FILE="/tmp/kugou-widget-diagnostic-$(date +%Y%m%d-%H%M%S).log"
{
    echo "Kugou Widget Diagnostic Report"
    echo "Generated: $(date)"
    echo "URL: $URL"
    echo ""
    echo "=== Health Check ==="
    echo "$HEALTH"
    echo ""
    echo "=== Widget Response (first 500 chars) ==="
    echo "${WIDGET:0:500}"
    echo ""
    echo "=== Headers ==="
    echo "$HEADERS"
} > "$LOG_FILE"

echo "Full diagnostic log saved to: $LOG_FILE"
echo ""
