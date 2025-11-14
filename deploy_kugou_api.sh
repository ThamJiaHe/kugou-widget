#!/bin/bash
#
# KuGouMusicApi Deployment Script
# This script helps you deploy the Node.js KuGouMusicApi service to Vercel
#

set -e  # Exit on error

echo "=========================================="
echo "  KuGouMusicApi Deployment Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/MakcRe/KuGouMusicApi.git"
TARGET_DIR="$HOME/KuGouMusicApi"

echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Please install Node.js first: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
fi

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
fi

echo -e "${GREEN}✓ All prerequisites installed${NC}"
echo ""

echo -e "${YELLOW}Step 2: Cloning KuGouMusicApi repository...${NC}"

# Remove existing directory if it exists
if [ -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}Directory $TARGET_DIR already exists. Removing...${NC}"
    rm -rf "$TARGET_DIR"
fi

# Clone the repository
git clone "$REPO_URL" "$TARGET_DIR"
cd "$TARGET_DIR"

echo -e "${GREEN}✓ Repository cloned to $TARGET_DIR${NC}"
echo ""

echo -e "${YELLOW}Step 3: Installing dependencies...${NC}"
npm install

echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

echo -e "${YELLOW}Step 4: Deploying to Vercel...${NC}"
echo ""
echo "You will be prompted to:"
echo "  1. Login to Vercel (if not already logged in)"
echo "  2. Select your scope (personal account)"
echo "  3. Link to existing project or create new one"
echo "  4. Confirm deployment settings"
echo ""
read -p "Press Enter to continue with deployment..."

# Deploy to Vercel
vercel --prod

echo ""
echo -e "${GREEN}=========================================="
echo "  Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo "Your KuGouMusicApi is now deployed to Vercel."
echo ""
echo -e "${YELLOW}IMPORTANT: Save your API URL${NC}"
echo "Example: https://ku-gou-music-api-xxxxx.vercel.app"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Test your API:"
echo "   curl https://YOUR_API_URL/health"
echo ""
echo "2. Login to Kugou (get verification code):"
echo "   curl 'https://YOUR_API_URL/login/code?username=YOUR_PHONE_NUMBER'"
echo ""
echo "3. Verify and get credentials:"
echo "   curl 'https://YOUR_API_URL/login/verify?username=YOUR_PHONE_NUMBER&code=123456'"
echo ""
echo "4. Connect to your widget:"
echo "   curl -X POST https://kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app/setup-kugou \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{"
echo "       \"user_id\": \"YOUR_GITHUB_USERNAME\","
echo "       \"api_url\": \"https://YOUR_API_URL\","
echo "       \"userid\": \"FROM_STEP_3\","
echo "       \"token\": \"FROM_STEP_3\""
echo "     }'"
echo ""
echo "For detailed instructions, see: KUGOU_API_INTEGRATION.md"
echo ""
