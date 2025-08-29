# 🐳 Docker Guide for Mad Scientist AI

This guide covers everything you need to know about running Mad Scientist AI with Docker, from development to production deployment.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Development](#development)
- [Production](#production)
- [Docker Compose Files](#docker-compose-files)
- [Management Scripts](#management-scripts)
- [Health Monitoring](#health-monitoring)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

## 🚀 Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 1.29 or higher
- **System Requirements**: 
  - 2GB RAM minimum (4GB recommended)
  - 1GB disk space for images
  - Linux, macOS, or Windows with WSL2

### Installation Check

```bash
# Verify Docker installation
docker --version
docker-compose --version

# Test Docker is running
docker run hello-world
```

## ⚡ Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/stepheweffie/mad-scientist.git
cd mad-scientist
git checkout docker  # Switch to Docker branch
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your Cloudflare credentials
nano .env  # or use your preferred editor
```

### 3. Start the Application

```bash
# Development mode
./docker-scripts.sh dev

# Or production mode
./docker-scripts.sh prod
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required - Cloudflare API Configuration
API_BASE_URL=https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/run/
ACCOUNT_ID=your_cloudflare_account_id
AUTH_TOKEN=your_cloudflare_api_token

# Required - Application Security
SECRET_KEY=your-secure-secret-key-here

# Optional - Application Settings
LOG_LEVEL=INFO
GTAG=your_google_analytics_tag
PORT=8000
DOMAIN=localhost
```

### Cloudflare Setup

1. **Create Cloudflare Account**: Sign up at [cloudflare.com](https://cloudflare.com)
2. **Get Account ID**: Found in the right sidebar of your Cloudflare dashboard
3. **Generate API Token**:
   - Go to "My Profile" → "API Tokens"
   - Click "Create Token"
   - Use "Custom token" with these permissions:
     - `Account:Cloudflare Workers:Edit`
     - `Zone:Zone:Read`

## 🔧 Development

### Development Environment

The development setup includes:
- Hot reload enabled
- Debug logging
- Source code mounting (optional)
- Development-friendly restart policies

```bash
# Start development environment (foreground)
./docker-scripts.sh dev

# Start development environment (background)
./docker-scripts.sh dev-bg

# View development logs
./docker-scripts.sh logs dev

# Stop development environment
docker-compose -f docker-compose.dev.yml down
```

### Development Features

- **Live Reload**: Changes to code trigger automatic restarts
- **Debug Logging**: Detailed logs for troubleshooting
- **Volume Mounting**: Host logs directory mounted for easy access
- **No Auto-Restart**: Containers stop when they crash (for debugging)

## 🏭 Production

### Production Environment

The production setup includes:
- Optimized multi-stage build
- Non-root user for security
- Health checks and monitoring
- Resource limits
- Automatic restarts
- SSL/TLS support with Traefik

```bash
# Start production environment
./docker-scripts.sh prod

# View production logs
./docker-scripts.sh logs prod

# Check application health
./docker-scripts.sh health
```

### Production Features

- **Multi-Stage Build**: Smaller, more secure images
- **Non-Root User**: Runs as `appuser` (UID 1000)
- **Resource Limits**: CPU and memory constraints
- **Health Checks**: Automatic container health monitoring
- **Persistent Logs**: Logs stored in Docker volumes
- **Auto-Restart**: Automatic recovery from failures

## 📁 Docker Compose Files

### docker-compose.yml (Default)
- **Purpose**: Basic setup with environment variable support
- **Use Case**: Standard deployment
- **Features**: Persistent logs, health checks, Traefik integration

### docker-compose.dev.yml (Development)
- **Purpose**: Development-optimized configuration
- **Use Case**: Local development and debugging
- **Features**: Live reload, debug logging, no auto-restart

### docker-compose.prod.yml (Production)
- **Purpose**: Production-ready configuration
- **Use Case**: Production deployments
- **Features**: Resource limits, SSL support, monitoring

## 🛠️ Management Scripts

The `docker-scripts.sh` provides convenient management commands:

### Build Commands
```bash
./docker-scripts.sh build       # Build Docker image
```

### Environment Commands
```bash
./docker-scripts.sh dev         # Start development (foreground)
./docker-scripts.sh dev-bg      # Start development (background)
./docker-scripts.sh prod        # Start production
```

### Management Commands
```bash
./docker-scripts.sh stop        # Stop all containers
./docker-scripts.sh clean       # Full cleanup
./docker-scripts.sh logs [env]  # View logs
./docker-scripts.sh health      # Health check
./docker-scripts.sh shell [env] # Container shell
```

### Examples
```bash
# Full development workflow
./docker-scripts.sh dev-bg      # Start in background
./docker-scripts.sh logs dev    # Watch logs
./docker-scripts.sh health      # Check health
./docker-scripts.sh shell dev   # Debug in container
./docker-scripts.sh stop        # Clean shutdown

# Production deployment
./docker-scripts.sh prod        # Deploy production
./docker-scripts.sh health      # Verify deployment
```

## 🏥 Health Monitoring

### Health Check Endpoint

The application includes a health check endpoint at `/health`:

```json
{
  "status": "healthy",
  "service": "Mad Scientist AI",
  "version": "1.0.0",
  "timestamp": "2025-08-29T01:03:00Z"
}
```

### Docker Health Checks

Health checks are configured in all compose files:
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3-5 attempts
- **Start Period**: 40-60 seconds

### Monitoring Commands

```bash
# Check application health
curl http://localhost:8000/health

# Docker container health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# View health check logs
docker logs mad-scientist-app | grep health
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Container Won't Start
```bash
# Check logs
./docker-scripts.sh logs

# Common causes:
# - Missing .env file
# - Invalid API credentials
# - Port conflicts
```

#### 2. Health Check Failures
```bash
# Test health endpoint manually
curl -f http://localhost:8000/health

# Check if application is running
docker exec mad-scientist-app ps aux
```

#### 3. Permission Issues
```bash
# Check container user
docker exec mad-scientist-app id

# Fix log directory permissions
sudo chown -R 1000:1000 ./logs
```

#### 4. Network Issues
```bash
# Check network connectivity
docker network ls
docker network inspect mad-scientist-network

# Test DNS resolution
docker exec mad-scientist-app nslookup google.com
```

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
# Set debug environment
export LOG_LEVEL=DEBUG

# Start with debug logging
./docker-scripts.sh dev
```

### Container Inspection

```bash
# Inspect running container
docker inspect mad-scientist-app

# View resource usage
docker stats mad-scientist-app

# Access container shell
./docker-scripts.sh shell
```

## 🔐 Security Considerations

### Container Security

1. **Non-Root User**: Application runs as `appuser` (UID 1000)
2. **Read-Only Filesystem**: Where possible, use read-only mounts
3. **Resource Limits**: CPU and memory constraints in production
4. **Health Checks**: Automatic detection of compromised containers

### Network Security

1. **Custom Networks**: Isolated Docker networks
2. **Port Mapping**: Only expose necessary ports
3. **Traefik Integration**: SSL termination and security headers
4. **Firewall**: Consider host-level firewall rules

### Data Security

1. **Environment Variables**: Never commit secrets to Git
2. **Volume Permissions**: Proper file permissions on mounted volumes
3. **Log Security**: Ensure logs don't contain sensitive information
4. **API Keys**: Secure Cloudflare API token storage

### Production Security Checklist

- [ ] Use strong `SECRET_KEY` (32+ characters)
- [ ] Enable SSL/TLS certificates
- [ ] Set up proper firewall rules
- [ ] Configure log rotation
- [ ] Monitor container health
- [ ] Regular security updates
- [ ] Backup configuration files

## 🚀 Deployment Examples

### Basic Development
```bash
git clone https://github.com/stepheweffie/mad-scientist.git
cd mad-scientist
git checkout docker
cp .env.example .env
# Edit .env with your credentials
./docker-scripts.sh dev
```

### Production with Traefik
```bash
# With Traefik proxy
export DOMAIN=yourdomain.com
./docker-scripts.sh prod
```

### Docker Swarm Deployment
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml mad-scientist
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Cloudflare Workers AI API](https://developers.cloudflare.com/workers-ai/)
- [FastAPI Docker Documentation](https://fastapi.tiangolo.com/deployment/docker/)

## 🆘 Support

If you encounter issues:

1. **Check Logs**: Always start with `./docker-scripts.sh logs`
2. **Health Check**: Run `./docker-scripts.sh health`
3. **GitHub Issues**: [Report bugs](https://github.com/stepheweffie/mad-scientist/issues)
4. **Discussions**: [Community support](https://github.com/stepheweffie/mad-scientist/discussions)

---

**Happy Containerizing! 🧪🐳**
