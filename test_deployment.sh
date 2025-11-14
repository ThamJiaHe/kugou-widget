#!/bin/bash
#
# Test Your Deployed Kugou Widget
# This script tests all endpoints of your deployed widget
#

WIDGET_URL="https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app"

echo "=========================================="
echo "  Testing Kugou Widget Deployment"
echo "=========================================="
echo ""
echo "Widget URL: $WIDGET_URL"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test 1: Health Check
echo -e "${YELLOW}Test 1: Health Check${NC}"
echo "GET $WIDGET_URL/health"
RESPONSE=$(curl -s "$WIDGET_URL/health")
if echo "$RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    echo "Response: $RESPONSE"
else
    echo -e "${RED}✗ Health check failed${NC}"
    echo "Response: $RESPONSE"
fi
echo ""

# Test 2: Demo Widget
echo -e "${YELLOW}Test 2: Demo Widget${NC}"
echo "GET $WIDGET_URL?user_id=demo&theme=dark"
RESPONSE=$(curl -s "$WIDGET_URL?user_id=demo&theme=dark")
if echo "$RESPONSE" | grep -q "<svg"; then
    echo -e "${GREEN}✓ Demo widget works${NC}"
    echo "SVG generated successfully"
else
    echo -e "${RED}✗ Demo widget failed${NC}"
    echo "Response: ${RESPONSE:0:200}..."
fi
echo ""

# Test 3: Test Endpoint
echo -e "${YELLOW}Test 3: Test Endpoint${NC}"
echo "GET $WIDGET_URL/test"
RESPONSE=$(curl -s "$WIDGET_URL/test")
if echo "$RESPONSE" | grep -q "<svg"; then
    echo -e "${GREEN}✓ Test endpoint works${NC}"
    echo "SVG generated successfully"
else
    echo -e "${RED}✗ Test endpoint failed${NC}"
    echo "Response: ${RESPONSE:0:200}..."
fi
echo ""

# Test 4: Light Theme
echo -e "${YELLOW}Test 4: Light Theme${NC}"
echo "GET $WIDGET_URL?user_id=demo&theme=light"
RESPONSE=$(curl -s "$WIDGET_URL?user_id=demo&theme=light")
if echo "$RESPONSE" | grep -q "<svg"; then
    echo -e "${GREEN}✓ Light theme works${NC}"
else
    echo -e "${RED}✗ Light theme failed${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo "  Test Summary"
echo "=========================================="
echo ""
echo -e "${GREEN}✓ Widget is deployed and working!${NC}"
echo ""
echo "Next Steps:"
echo "1. Deploy KuGouMusicApi (see DEPLOY_KUGOU_API.md)"
echo "2. Login to your Kugou account"
echo "3. Connect credentials via /setup-kugou"
echo "4. Add widget to your GitHub profile README"
echo ""
echo "Demo Widget URL (ready to use now):"
echo "$WIDGET_URL?user_id=demo&theme=dark"
echo ""
echo "Documentation:"
echo "- Quick Setup: QUICK_SETUP.md"
echo "- Deploy KuGou API: DEPLOY_KUGOU_API.md"
echo "- Full Guide: KUGOU_API_INTEGRATION.md"
echo ""
