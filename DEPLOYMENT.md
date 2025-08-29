# 🚀 Deployment Guide

This guide covers various deployment options for Mad Scientist AI, from simple single-click deployments to advanced container orchestration.

## 🐳 Coolify (Recommended for Self-Hosting)

[Coolify](https://coolify.io/) is a self-hosted alternative to Heroku/Netlify/Vercel. It's perfect for deploying Mad Scientist AI on your own infrastructure.

### Prerequisites
- A server running Coolify (VPS, dedicated server, or local machine)
- GitHub repository access
- Cloudflare AI API credentials

### Deployment Steps

1. **Add Repository**
   - In Coolify dashboard, go to "Projects"
   - Click "Add New Project" or use an existing one
   - Select "Public Repository" and enter: `https://github.com/stepheweffie/mad-scientist.git`

2. **Configure Build Settings**
   - Coolify will automatically detect the Dockerfile
   - Set the build context to root directory
   - No additional build settings needed

3. **Environment Variables**
   Set these required environment variables in Coolify:
   ```bash
   API_BASE_URL=https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/run/
   ACCOUNT_ID=your_cloudflare_account_id
   AUTH_TOKEN=your_cloudflare_api_token
   SECRET_KEY=your_secure_random_secret_key_here
   LOG_LEVEL=INFO
   ```

4. **Domain Configuration**
   - Set your custom domain or use the Coolify-provided subdomain
   - SSL certificates are automatically generated

5. **Deploy**
   - Click "Deploy" and Coolify will build and start your application
   - Monitor the build logs in real-time

6. **Health Check**
   - Once deployed, visit `https://your-domain.com/health` to verify
   - You should see: `{"status":"healthy","service":"Mad Scientist AI","version":"1.0.0"}`

### Coolify Features Used
- ✅ Automatic Docker builds
- ✅ SSL certificate management
- ✅ Environment variable management
- ✅ Build logs and monitoring
- ✅ Git integration with auto-deploy
- ✅ Health checks and restart policies

---

## 🚄 Railway

Railway provides zero-configuration deployments with automatic scaling.

### Quick Deploy
1. Visit [Railway](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select the Mad Scientist repository
4. Add environment variables in the Railway dashboard
5. Railway automatically detects and builds the Dockerfile

### Configuration
```bash
# Railway Environment Variables
API_BASE_URL=https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/run/
ACCOUNT_ID=your_cloudflare_account_id
AUTH_TOKEN=your_cloudflare_api_token
SECRET_KEY=your_secure_random_secret_key
PORT=8000
```

---

## 🎨 Render

Render provides a simple platform for deploying applications with automatic SSL.

### Deployment Steps
1. Go to [Render](https://render.com) dashboard
2. Click "New" → "Web Service"
3. Connect your GitHub account and select the Mad Scientist repository
4. Configure:
   - **Build Command**: Not needed (Docker)
   - **Start Command**: Not needed (Docker)
   - **Environment**: Docker
5. Add environment variables
6. Deploy

---

## ✈️ Fly.io

Fast global deployment with edge computing capabilities.

### Setup
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Navigate to project directory
cd mad-scientist

# Initialize Fly app
fly launch --no-deploy

# Set secrets (environment variables)
fly secrets set \
  API_BASE_URL="https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/run/" \
  ACCOUNT_ID="your_cloudflare_account_id" \
  AUTH_TOKEN="your_cloudflare_api_token" \
  SECRET_KEY="your_secure_random_secret_key"

# Deploy
fly deploy
```

---

## ☁️ Cloud Platforms

### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/mad-scientist
gcloud run deploy mad-scientist \
  --image gcr.io/PROJECT_ID/mad-scientist \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="API_BASE_URL=your_api_url,ACCOUNT_ID=your_account,SECRET_KEY=your_secret"
```

### AWS App Runner
1. Push to Amazon ECR
2. Create App Runner service from ECR image
3. Configure environment variables
4. Deploy with auto-scaling

---

## 🐳 Docker Self-Hosted

### Using Docker Compose (Production)
```bash
# Clone repository
git clone https://github.com/stepheweffie/mad-scientist.git
cd mad-scientist

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Deploy using our scripts
./docker-scripts.sh prod
```

### Manual Docker Deployment
```bash
# Build image
docker build -t mad-scientist .

# Run container
docker run -d \
  --name mad-scientist \
  -p 80:8000 \
  --env-file .env \
  --restart unless-stopped \
  mad-scientist

# Check health
curl http://localhost/health
```

---

## 🔧 VPS Manual Installation

### Ubuntu/Debian Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install requirements
sudo apt install -y python3 python3-pip python3-venv nginx git

# Clone repository
git clone https://github.com/stepheweffie/mad-scientist.git
cd mad-scientist

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Create systemd service
sudo tee /etc/systemd/system/mad-scientist.service > /dev/null <<EOF
[Unit]
Description=Mad Scientist AI
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/mad-scientist
Environment=PATH=/home/ubuntu/mad-scientist/venv/bin
ExecStart=/home/ubuntu/mad-scientist/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable mad-scientist
sudo systemctl start mad-scientist

# Configure Nginx (optional)
sudo tee /etc/nginx/sites-available/mad-scientist > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/mad-scientist /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 🔍 Environment Variables Reference

### Required
```bash
API_BASE_URL=https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/
ACCOUNT_ID=your_cloudflare_account_id
AUTH_TOKEN=your_cloudflare_api_token
SECRET_KEY=your_secure_random_secret_key
```

### Optional
```bash
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
GTAG=your_google_analytics_tag    # Google Analytics tracking
PORT=8000                         # Application port (default: 8000)
```

---

## 🏥 Health Monitoring

All deployments include a health check endpoint:

```bash
curl https://your-domain.com/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Mad Scientist AI",
  "version": "1.0.0",
  "timestamp": "2025-08-29T01:17:00Z"
}
```

---

## 📊 Monitoring and Logging

### Application Logs
- **Container deployments**: Use `docker logs` or platform-specific log viewers
- **Manual deployments**: Logs are written to `logs/` directory
- **Systemd services**: Use `journalctl -u mad-scientist -f`

### Log Levels
Configure logging verbosity with the `LOG_LEVEL` environment variable:
- `DEBUG`: Detailed debug information
- `INFO`: General application information (default)
- `WARNING`: Warning messages only
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

---

## 🚨 Troubleshooting

### Common Issues

#### Application Won't Start
1. Check environment variables are set correctly
2. Verify Cloudflare API credentials
3. Check application logs for detailed error messages

#### Health Check Fails
1. Ensure application is running on correct port
2. Check firewall settings
3. Verify `/health` endpoint is accessible

#### Container Issues
1. Check Docker logs: `docker logs mad-scientist`
2. Verify environment file exists and is properly formatted
3. Ensure container has proper permissions

### Getting Help
- **GitHub Issues**: [Report bugs](https://github.com/stepheweffie/mad-scientist/issues)
- **Discussions**: [Community support](https://github.com/stepheweffie/mad-scientist/discussions)
- **Documentation**: [README.md](README.md) and [Docker Guide](DOCKER.md)

---

**Need help with deployment? Create an issue on GitHub!**
