# 🚀 Deployment Guide

## Deploy Mad Scientist AI Chat to Your Cloudflare Domain

### Prerequisites
- Docker installed and running
- Cloudflare account with your domain added
- Cloudflare API Token (see instructions below)

## Quick Deploy with Docker

### Step 1: Get Cloudflare API Token
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use "Custom token" with these permissions:
   - **Account**: `Cloudflare Workers:Edit`
   - **Zone**: `Zone:Read`
   - **Account**: `Account:Read`
4. Copy the generated token

### Step 2: Deploy
```bash
# Set your API token
export CLOUDFLARE_API_TOKEN=your_token_here

# Deploy using Docker
docker-compose -f docker-compose.deploy.yml up --build

# Or deploy manually
docker build -f Dockerfile.deploy -t mad-scientist-deploy .
docker run -e CLOUDFLARE_API_TOKEN=$CLOUDFLARE_API_TOKEN mad-scientist-deploy
```

### Step 3: Add Custom Domain (mad-scientist.chat)

**Option A: Automatic (via wrangler.toml)**
The route is already configured in `wrangler.toml`, so deployment should automatically set up `mad-scientist.chat/*`

**Option B: Manual Setup**
1. Go to https://dash.cloudflare.com
2. Navigate to **Workers & Pages** > **mad-scientist**
3. Go to **Settings** > **Triggers**
4. In the **Routes** section, click **Add route**
5. Enter: `mad-scientist.chat/*`
6. Select your `mad-scientist.chat` zone from dropdown
7. Click **Add route**

**Option C: Custom Domains (if available)**
If you see a "Custom Domains" section:
1. Click **Add Custom Domain**
2. Enter: `mad-scientist.chat`
3. Click **Add Custom Domain**

## Alternative: Direct Deployment (Linux/Ubuntu)

If you have Ubuntu/Linux or want to use GitHub Actions:

```bash
# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Wrangler
npm install -g wrangler

# Authenticate (interactive)
wrangler login

# Deploy
wrangler deploy
```

## Understanding Cloudflare Workers Triggers

### Trigger Types:
1. **Routes/Custom Domains** - HTTP requests (what we need)
2. **Cron Triggers** - Scheduled tasks (e.g., daily cleanup)
3. **Queue Consumers** - Process messages from queues

### For Web Applications (like our AI Chat):
Use **Routes** or **Custom Domains** to handle HTTP requests.

## Custom Domain Setup

### Option 1: Subdomain (Recommended)
- Add route: `chat.yourdomain.com/*`
- Creates automatic DNS record
- SSL certificate auto-generated
- Example: `https://chat.yourdomain.com`

### Option 2: Root Domain
- Add route: `yourdomain.com/*`
- May require additional DNS configuration
- Example: `https://yourdomain.com`

### Option 3: Specific Path
- Add route: `yourdomain.com/chat/*`
- AI chat available at: `https://yourdomain.com/chat`

## Environment Variables

Add these to your Cloudflare Worker environment:
- `APP_NAME`: Your custom app name
- `DEFAULT_MESSAGE`: Custom greeting message

## Troubleshooting

**Deployment fails:**
```bash
# Check API token permissions
wrangler whoami

# Verify token has Workers:Edit permissions
```

**Domain not working:**
- Check DNS propagation (can take up to 24 hours)
- Verify domain is in your Cloudflare account
- Check SSL certificate status

**AI not working:**
- Ensure Cloudflare Workers AI is enabled in your dashboard
- Check account has AI credits/plan

## After Deployment

Your Mad Scientist AI Chat will be available at:
- **Workers URL**: `https://mad-scientist.savant-savantlab-org.workers.dev`  
- **Custom Domain**: `https://mad-scientist.chat` 🎯

Visit https://mad-scientist.chat to test your AI chat interface! 🧪⚡
