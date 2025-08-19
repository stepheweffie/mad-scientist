#!/bin/bash

echo "🔑 Setting up Cloudflare API Token for Mad Scientist deployment"
echo "=============================================================="

# Check if API token is already set
if [ -n "$CLOUDFLARE_API_TOKEN" ]; then
    echo "✅ CLOUDFLARE_API_TOKEN is already set"
    echo "Current token: ${CLOUDFLARE_API_TOKEN:0:10}..."
    read -p "Do you want to update it? (y/n): " update_token
    if [ "$update_token" != "y" ]; then
        echo "Keeping existing token."
        exit 0
    fi
fi

echo ""
echo "📋 To get your Cloudflare API Token:"
echo "1. Go to: https://dash.cloudflare.com/profile/api-tokens"
echo "2. Click 'Create Token'"
echo "3. Use 'Custom token' with these permissions:"
echo "   - Account: Cloudflare Workers:Edit"
echo "   - Zone: Zone:Read"
echo "   - Account: Account:Read"
echo "4. Copy the generated token"
echo ""

read -p "🔑 Enter your Cloudflare API Token: " api_token

if [ -z "$api_token" ]; then
    echo "❌ No token provided. Exiting."
    exit 1
fi

# Add to .zshrc if not already there
if ! grep -q "CLOUDFLARE_API_TOKEN" ~/.zshrc; then
    echo "" >> ~/.zshrc
    echo "# Cloudflare API Token for Mad Scientist" >> ~/.zshrc
    echo "export CLOUDFLARE_API_TOKEN=\"$api_token\"" >> ~/.zshrc
else
    # Update existing token
    sed -i '' "s/export CLOUDFLARE_API_TOKEN=.*/export CLOUDFLARE_API_TOKEN=\"$api_token\"/" ~/.zshrc
fi

# Set for current session
export CLOUDFLARE_API_TOKEN="$api_token"

echo "✅ API Token configured successfully!"
echo "🔄 Reload your terminal or run: source ~/.zshrc"
echo ""
echo "🚀 You can now deploy with: ./deploy.sh"
echo "   Or manually with: wrangler deploy"
