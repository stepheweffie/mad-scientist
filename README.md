# 🧪 Mad Scientist AI Chat

An AI-powered chat interface built with FastAPI and deployed on Cloudflare Workers, using Cloudflare Workers AI for intelligent conversations.

![Mad Scientist Demo](https://img.shields.io/badge/Status-Active-green) ![Python](https://img.shields.io/badge/Python-FastAPI-blue) ![AI](https://img.shields.io/badge/AI-Cloudflare_Workers-orange)

## 🚀 Quick Start

```bash
# Install Wrangler CLI
npm install -g wrangler

# Clone and setup
cd mad-scientist
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
│   └── worker.py          # Main FastAPI application
├── wrangler.toml          # Cloudflare Workers config
├── package.json           # Node.js dependencies (Wrangler)
├── requirements.txt       # Python dependencies
└── README.md             # This file
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

## 🐛 Debugging

### Common Issues

**"AI binding not available"**
- Ensure Cloudflare Workers AI is enabled in your dashboard
- Check the `[ai]` binding in `wrangler.toml`

**Deployment fails**
```bash
wrangler whoami  # Check auth
wrangler login   # Re-authenticate
```

**Local development**
```bash
# Start local dev server
wrangler dev

# With debug logs
wrangler dev --log-level debug

# Check live logs
wrangler tail
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
