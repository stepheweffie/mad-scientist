# 🧪 Mad Scientist AI Chat

An AI-powered chat interface built with FastAPI and deployed on Cloudflare Workers, using Cloudflare Workers AI for intelligent conversations.

![Mad Scientist Demo](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-FastAPI-blue) ![AI](https://img.shields.io/badge/AI-Cloudflare_Workers-orange)

## 🚀 Quick Start

### Option 1: Docker (Recommended for Local Development)

```bash
# Clone the repository
git clone https://github.com/stepheweffie/mad-scientist.git
cd mad-scientist
git checkout minimal

# Run with Docker Compose (easiest)
docker-compose up --build

# Or build and run manually
docker build -t mad-scientist .
docker run -p 8787:8787 mad-scientist

# Visit http://localhost:8787
```

### Option 2: Local Python Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run local development server with mock AI
python local_dev.py

# Visit http://localhost:8000
```

### Option 3: Cloudflare Workers Deployment

```bash
# Install Wrangler CLI
npm install -g wrangler

# Install dependencies
npm install

# Login to Cloudflare
wrangler login

# Deploy
wrangler deploy
```

## ✨ Features

- **AI Chat**: Powered by Cloudflare Workers AI (Llama-3-8B-Instruct)
- **Modern UI**: Dark theme with "mad scientist" aesthetics
- **FastAPI Backend**: Fast, type-safe Python API
- **Real-time Ready**: WebSocket support for future enhancements
- **Global Edge**: Deployed on Cloudflare's global network
- **Auto Docs**: Built-in OpenAPI documentation at `/docs`

## 🏗️ Project Structure

```
mad-scientist/
├── src/
│   └── worker.py          # Main FastAPI application with AI integration
├── wrangler.toml          # Cloudflare Workers configuration
├── package.json           # Node.js dependencies (Wrangler CLI)
├── requirements.txt       # Python dependencies (FastAPI, etc.)
├── local_dev.py           # Local development server with mock AI
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose orchestration
├── README.md              # Main documentation (this file)
├── API.md                 # Detailed API documentation
└── .gitignore             # Git exclusion rules
```

## 🔧 Configuration

### Current AI Models

The app uses `@cf/meta/llama-3-8b-instruct` by default. Other available models:
- `@cf/mistral/mistral-7b-instruct-v0.1`
- `@cf/meta/llama-3-70b-instruct` (slower but more capable)
- `@cf/google/gemma-7b-it`

Change the model in `src/worker.py`:

```python
class ChatMessage(BaseModel):
    message: str
    model: str = "@cf/meta/llama-3-8b-instruct"  # Change this
```

### Environment Variables

Edit `wrangler.toml`:

```toml
[vars]
APP_NAME = "Your Custom App Name"
DEFAULT_MESSAGE = "Your custom greeting"
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|--------------|
| `/` | GET | Web interface |
| `/chat` | POST | Chat API |
| `/docs` | GET | API documentation |
| `/health` | GET | Health check |
| `/ws` | WebSocket | Real-time chat |

### Chat API Example

```bash
curl -X POST "https://your-worker.workers.dev/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum computing",
    "model": "@cf/meta/llama-3-8b-instruct"
  }'
```

## 🐳 Docker Deployment

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### Quick Docker Setup

#### Method 1: Docker Compose (Recommended)

```bash
# Clone and navigate to project
git clone https://github.com/stepheweffie/mad-scientist.git
cd mad-scientist
git checkout minimal

# Start the application
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

#### Method 2: Manual Docker Build

```bash
# Build the Docker image
docker build -t mad-scientist-chat .

# Run the container
docker run -p 8787:8787 mad-scientist-chat

# Run in background with custom name
docker run -d --name mad-scientist -p 8787:8787 mad-scientist-chat

# View logs
docker logs -f mad-scientist

# Stop and remove
docker stop mad-scientist
docker rm mad-scientist
```

### Development with Docker

```bash
# Run with volume mounting for live code changes
docker run -p 8787:8787 -v $(pwd)/src:/app/src mad-scientist-chat

# Or use docker-compose with volumes (already configured)
docker-compose up
```

### Docker Environment Variables

Customize the application by setting environment variables:

```bash
# Using Docker run
docker run -p 8787:8787 \
  -e APP_NAME="My Custom Chat" \
  -e DEFAULT_MESSAGE="Hello there!" \
  mad-scientist-chat
```

Or add them to `docker-compose.yml`:

```yaml
services:
  mad-scientist:
    build: .
    environment:
      - APP_NAME=My Custom Chat
      - DEFAULT_MESSAGE=Hello there!
    ports:
      - "8787:8787"
```

### Docker Troubleshooting

**Port already in use:**
```bash
# Use a different port
docker run -p 8080:8787 mad-scientist-chat
# Then visit http://localhost:8080
```

**Build fails:**
```bash
# Clean build without cache
docker build --no-cache -t mad-scientist-chat .

# Check Docker version compatibility
docker --version
```

**Container won't start:**
```bash
# Check container logs
docker logs container-name

# Run interactively for debugging
docker run -it mad-scientist-chat /bin/bash
```

**macOS compatibility issues:**
```bash
# For older macOS versions, use local Python instead
python local_dev.py
```

## 🐛 General Debugging

### Common Issues

**"AI binding not available"**
- This only affects Cloudflare Workers deployment
- For local development, use `python local_dev.py` (mock responses)
- Ensure Cloudflare Workers AI is enabled in your dashboard
- Check the `[ai]` binding in `wrangler.toml`

**Deployment fails**
```bash
wrangler whoami  # Check auth
wrangler login   # Re-authenticate
```

**Local development (Wrangler)**
```bash
# Start local dev server (requires macOS 13.5+)
wrangler dev

# With debug logs
wrangler dev --log-level debug

# Check live logs
wrangler tail

# For older macOS, use Docker or Python directly
docker-compose up  # or
python local_dev.py
```

## 🚀 Development

### Local Testing

```bash
# Start development server
wrangler dev

# Visit http://localhost:8787
```

### Code Structure

- `src/worker.py`: Main FastAPI app with embedded HTML
- AI integration via Cloudflare Workers AI binding
- Type-safe with Pydantic models
- Error handling and health checks

## 📚 Resources

- [Cloudflare Workers AI Models](https://developers.cloudflare.com/workers-ai/models/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

**Happy experimenting! 🧪⚡**
