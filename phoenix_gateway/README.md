# Phoenix API Gateway

A high-performance API gateway built with Phoenix/Elixir that orchestrates communication between Flask authentication service and FastAPI chat service.

## Architecture

The Phoenix Gateway acts as a single entry point for all API calls, providing:

- **Service Orchestration**: Coordinates calls between Flask (auth) and FastAPI (chat) services
- **JWT Authentication**: Validates tokens and manages user sessions
- **Circuit Breaker Pattern**: Provides resilience against service failures
- **Request/Response Transformation**: Standardizes API responses across services
- **Health Monitoring**: Tracks service availability and performance

## Features

### 🔐 Authentication Management
- User registration and login
- JWT token validation and refresh
- Session management with HTTP cookies
- User profile retrieval

### 💬 Chat Operations
- AI-powered chat message processing
- Chat history retrieval with pagination
- Avatar generation and management
- Real-time communication support

### 🎯 Unified Dashboard
- Combined endpoint for fetching user profile, chat history, and avatar data
- Concurrent API calls for optimal performance
- Graceful degradation when services are unavailable

### 🛡️ Resilience & Monitoring
- Circuit breaker protection for all external service calls
- Health checks for service availability
- Comprehensive logging and error handling
- CORS support for web applications

## API Endpoints

### Authentication
```
POST /api/auth/register      # Register new user
POST /api/auth/login         # User login
POST /api/auth/logout        # User logout
POST /api/auth/refresh       # Refresh JWT token
GET  /api/auth/validate      # Validate current token
GET  /api/auth/profile       # Get user profile
```

### Chat
```
POST /api/chat/message       # Send chat message
GET  /api/chat/history       # Get chat history
GET  /api/chat/avatar        # Get user avatar
POST /api/chat/avatar        # Generate user avatar
```

### Dashboard
```
GET  /api/dashboard          # Combined user dashboard data
```

### System
```
GET  /health                 # Health check endpoint
```

## Environment Variables

```bash
# Service URLs
AUTH_SERVICE_URL=http://auth-service:5000
CHAT_SERVICE_URL=http://chat-service:8000

# Phoenix Configuration
MIX_ENV=prod
SECRET_KEY_BASE=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here

# Database
DATABASE_URL=ecto://postgres:postgres@postgres:5432/phoenix_gateway_prod
```

## Development

### Prerequisites
- Elixir 1.15+
- Phoenix 1.7+
- PostgreSQL (for session storage)

### Setup
```bash
cd phoenix_gateway
mix deps.get
mix ecto.create
mix ecto.migrate
```

### Running
```bash
# Development
mix phx.server

# Production
MIX_ENV=prod mix phx.server
```

### Testing
```bash
mix test
```

## Docker Deployment

The Phoenix Gateway is designed to run as part of a Docker Compose setup. See the main project's `docker-compose.integrated.yml` for full configuration.

## Circuit Breaker Configuration

The gateway uses circuit breakers to protect against service failures:

- **Threshold**: 5 failures in 10 seconds
- **Recovery Time**: 60 seconds
- **Protected Services**: Auth service, Chat service
- **Failure Types**: Connection failures, timeouts, 5xx errors

## Integration with Existing Services

This Phoenix gateway orchestrates calls between:
- **Flask Auth Service** (Port 5000): User authentication and management
- **FastAPI Chat Service** (Port 8000): AI chat and avatar generation

All API calls are routed through Phoenix at `/api/*` endpoints, providing a unified interface while maintaining backward compatibility with existing direct service access.
