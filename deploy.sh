#!/bin/bash

echo "🧪 Mad Scientist AI Chat - Cloudflare Workers Deployment"
echo "======================================================="

# Check if CLOUDFLARE_API_TOKEN is set
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "❌ Error: CLOUDFLARE_API_TOKEN environment variable not found"
    echo ""
    echo "🔧 To set up your API token, run: ./setup_api.sh"
    echo "Or manually set it with:"
    echo "export CLOUDFLARE_API_TOKEN=your_token_here"
    echo ""
    exit 1
fi

echo "✅ Using global Cloudflare API Token"
echo "📋 Project: mad-scientist"
echo "🌐 Domain: mad-scientist.chat"
echo ""
echo "🚀 Deploying to Cloudflare Workers..."

# Load NVM and use Node 20
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Deploy to Cloudflare Workers
wrangler deploy --yes

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment successful!"
    echo "🌐 Mad Scientist AI Chat is live at:"
    echo "   👉 https://mad-scientist.chat"
    echo ""
    echo "🔗 Also available at .workers.dev subdomain"
    echo "📊 Check status: https://mad-scientist.chat/health"
    echo ""
else
    echo "❌ Deployment failed"
    echo "💡 Try running: ./setup_api.sh to check your API token"
    exit 1
fi
