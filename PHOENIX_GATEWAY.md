# Phoenix API Gateway Integration

This branch adds a Phoenix/Elixir API Gateway that provides a unified, high-performance interface for the Mad Scientist chat application.

## 🚀 What's New

### Phoenix API Gateway (`phoenix_gateway/`)
A high-performance API orchestration layer built with Phoenix/Elixir that:
- Provides unified API endpoints at `/api/*`
- Orchestrates calls between authentication and chat services
- Implements circuit breaker patterns for fault tolerance
- Offers concurrent request processing for better performance
- Includes comprehensive health monitoring

### Updated Infrastructure
- **Docker Compose**: `docker-compose.phoenix.yml` includes Phoenix service + PostgreSQL
- **Nginx Config**: `nginx.phoenix.conf` routes API calls through Phoenix Gateway
- **Service Integration**: Maintains backward compatibility while adding new API layer

## 📡 API Endpoints

### Authentication
```bash
POST /api/auth/register      # Register new user
POST /api/auth/login         # User login
GET  /api/auth/profile       # Get user profile
POST /api/auth/refresh       # Refresh JWT token
POST /api/auth/logout        # User logout
```

### Chat Operations
```bash
POST /api/chat/message       # Send chat message and get AI response
GET  /api/chat/history       # Get chat history with pagination
GET  /api/chat/avatar        # Get user's avatar
POST /api/chat/avatar        # Generate new avatar
```

### Dashboard
```bash
GET  /api/dashboard          # Combined user data (profile + history + avatar)
```

### System Health
```bash
GET  /health                 # Service health monitoring
```

## 🏗️ Architecture

```
Web Browser
    ↓
Nginx (Port 80)
    ↓
Phoenix Gateway (Port 4000) ← New API Layer
    ↓         ↓
Flask      FastAPI
(Auth)     (Chat)
```

## 🚀 Quick Start

### Development
```bash
# Start Phoenix Gateway
cd phoenix_gateway
mix deps.get
mix ecto.create
mix phx.server

# Phoenix runs on http://localhost:4000
```

### Production (Docker)
```bash
# Build and run all services including Phoenix Gateway
docker-compose -f docker-compose.phoenix.yml up -d

# Services:
# - Phoenix Gateway: http://localhost:4000
# - Nginx (with Phoenix routing): http://localhost:80
# - API endpoints: http://localhost/api/*
# - Health check: http://localhost/health
```

## 🔧 Environment Variables

```bash
# Phoenix Gateway Configuration
AUTH_SERVICE_URL=http://auth-service:5000    # Flask auth service
CHAT_SERVICE_URL=http://chat-service:8000    # FastAPI chat service
SECRET_KEY_BASE=your_secret_key              # Phoenix secret
JWT_SECRET_KEY=your_jwt_secret               # JWT validation key
DATABASE_URL=ecto://postgres:postgres@postgres:5432/phoenix_gateway_prod
```

## 🎯 Key Benefits

### Performance
- **High Concurrency**: Elixir's actor model handles thousands of concurrent requests
- **Concurrent API Calls**: Dashboard endpoint fetches multiple services simultaneously
- **Connection Pooling**: Optimized HTTP client connections

### Reliability
- **Circuit Breaker Pattern**: Automatic failover when services are down
- **Health Monitoring**: Real-time service status tracking
- **Graceful Degradation**: Partial responses when some services unavailable

### Developer Experience
- **Unified API**: Single entry point for all operations
- **Consistent Response Format**: Standardized JSON responses
- **Comprehensive Logging**: Detailed request/response tracking
- **Backward Compatibility**: Existing endpoints still work

## 📊 Example Usage

### Old Way (Multiple API Calls)
```javascript
// Requires 3 separate API calls
const profile = await fetch('/auth/profile');
const history = await fetch('/mad-scientist/history');
const avatar = await fetch('/mad-scientist/avatar');
```

### New Way (Phoenix Gateway)
```javascript
// Single API call that orchestrates everything
const dashboard = await fetch('/api/dashboard');
// Returns { profile, chat_history, avatar, meta } in one response
```

### Chat Message Example
```javascript
const response = await fetch('/api/chat/message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    message: 'Hello, what can you help me with?',
    context: { conversation_id: 'conv-123' }
  })
});
```

## 🛠️ Development Notes

### Project Structure
```
phoenix_gateway/
├── lib/
│   ├── phoenix_gateway/
│   │   └── services/           # Service communication modules
│   │       ├── auth_service.ex    # Flask auth service client
│   │       ├── chat_service.ex    # FastAPI chat service client
│   │       └── circuit_breaker.ex # Fault tolerance
│   └── phoenix_gateway_web/
│       ├── controllers/        # API controllers
│       └── plugs/             # Authentication middleware
├── config/                    # Environment configuration
├── Dockerfile                 # Container build
└── README.md                 # Detailed documentation
```

### Testing
```bash
cd phoenix_gateway
mix test

# Test specific modules
mix test test/phoenix_gateway/services/
mix test test/phoenix_gateway_web/controllers/
```

## 🔄 Migration Path

### Phase 1: Parallel Deployment
- Deploy Phoenix Gateway alongside existing services
- Both old and new APIs work simultaneously
- Test new endpoints while maintaining existing functionality

### Phase 2: Client Migration
- Update frontend applications to use `/api/*` endpoints
- Leverage improved performance and reliability
- Monitor both API versions

### Phase 3: Legacy Deprecation
- Once clients migrated, consider deprecating direct service access
- Maintain Phoenix Gateway as single API entry point

## 📈 Monitoring

### Health Checks
```bash
# Check overall system health
curl http://localhost/health

# Response includes:
# - Service status (auth, chat, phoenix)
# - Response times
# - System information
```

### Circuit Breaker Status
The Phoenix Gateway automatically monitors service health and implements circuit breakers to prevent cascading failures.

## 🤝 Contributing

When working with the Phoenix Gateway:
1. Follow Elixir/Phoenix conventions
2. Add tests for new functionality
3. Update API documentation
4. Ensure Docker builds work correctly

## 🆘 Troubleshooting

### Common Issues
- **Service Connection**: Check `AUTH_SERVICE_URL` and `CHAT_SERVICE_URL` environment variables
- **JWT Validation**: Ensure `JWT_SECRET_KEY` matches across all services
- **Database**: Verify PostgreSQL is running for Phoenix (port 5432)
- **Port Conflicts**: Make sure ports 4000, 5000, 8000, 5432 are available

### Debug Mode
```bash
export LOG_LEVEL=debug
cd phoenix_gateway
mix phx.server
```

---

This Phoenix Gateway provides a production-ready API layer that makes the Mad Scientist application more scalable, reliable, and developer-friendly! 🚀
