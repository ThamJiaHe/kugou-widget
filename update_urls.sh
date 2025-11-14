#!/bin/bash
#
# Update Widget URL in Documentation
# Updates all occurrences of the old widget URL to the new deployment URL
#

OLD_URL="kugou-widget-n7ck3dfve-cv4tkg1uav-gmailcoms-projects.vercel.app"
NEW_URL="kugou-widget-6yzx2np4o-cv4tkg1uav-gmailcoms-projects.vercel.app"

echo "Updating widget URL in all documentation files..."
echo "Old: $OLD_URL"
echo "New: $NEW_URL"
echo ""

# Update all markdown files
find . -type f -name "*.md" ! -path "./.git/*" -exec sed -i "s|$OLD_URL|$NEW_URL|g" {} \;

echo "✓ Updated all .md files"

# Update Python files if needed
find . -type f -name "*.py" ! -path "./.git/*" -exec sed -i "s|$OLD_URL|$NEW_URL|g" {} \;

echo "✓ Updated all .py files"

# Update shell scripts
find . -type f -name "*.sh" ! -path "./.git/*" -exec sed -i "s|$OLD_URL|$NEW_URL|g" {} \;

echo "✓ Updated all .sh files"

echo ""
echo "URL update complete!"
echo ""
echo "Test your new deployment:"
echo "curl https://$NEW_URL/health"
echo ""
