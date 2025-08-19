#!/bin/bash

echo "🧪 Mad Scientist AI Chat - Cloudflare Workers Deployment"
echo "======================================================="

# Check if CLOUDFLARE_API_TOKEN is set
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "❌ Error: CLOUDFLARE_API_TOKEN environment variable is required"
    echo "Please set your Cloudflare API token:"
    echo "export CLOUDFLARE_API_TOKEN=your_token_here"
    exit 1
fi

# Set the API token for Wrangler
export CLOUDFLARE_API_TOKEN=$CLOUDFLARE_API_TOKEN

echo "✅ Cloudflare API Token configured"
echo "📋 Project configuration:"
cat wrangler.toml

echo ""
echo "🚀 Deploying to Cloudflare Workers..."

# Deploy to Cloudflare Workers
wrangler deploy --yes

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment successful!"
    echo "🌐 Your Mad Scientist AI Chat is now live!"
    echo ""
    echo "Next steps to add custom domain:"
    echo "1. Go to https://dash.cloudflare.com"
    echo "2. Navigate to Workers & Pages > mad-scientist"
    echo "3. Go to Settings > Triggers"
    echo "4. Add Custom Domain and enter your domain"
    echo ""
else
    echo "❌ Deployment failed"
    exit 1
fi
