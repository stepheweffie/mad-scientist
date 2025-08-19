# API Documentation

## Overview

The Mad Scientist AI Chat provides a RESTful API for interacting with Cloudflare Workers AI models. All endpoints return JSON responses unless otherwise specified.

## Base URL

```
https://your-worker.your-subdomain.workers.dev
```

## Authentication

No authentication is required for public endpoints. Rate limiting is handled by Cloudflare Workers.

## Endpoints

### GET /

Returns the main web interface for the chat application.

**Response**: HTML page with embedded chat interface

### POST /chat

Send a message to the AI and receive a response.

**Request Body**:
```json
{
  "message": "Your question here",
  "model": "@cf/meta/llama-3-8b-instruct"
}
```

**Parameters**:
- `message` (string, required): The user's message/question
- `model` (string, optional): AI model to use. Defaults to `@cf/meta/llama-3-8b-instruct`

**Response**:
```json
{
  "response": "AI generated response",
  "model_used": "@cf/meta/llama-3-8b-instruct"
}
```

**Status Codes**:
- 200: Success
- 422: Invalid request body
- 500: AI binding error or processing error

### GET /health

Health check endpoint for monitoring.

**Response**:
```json
{
  "status": "healthy",
  "service": "mad-scientist-ai-chat"
}
```

### GET /docs

Auto-generated OpenAPI documentation (Swagger UI).

**Response**: Interactive API documentation

### WebSocket /ws

Real-time chat connection (basic echo implementation).

**Connection**: `ws://your-worker.workers.dev/ws`

**Send**:
```json
{
  "message": "Hello",
  "type": "chat"
}
```

**Receive**:
```json
{
  "type": "response",
  "message": "Echo: Hello",
  "timestamp": "now"
}
```

## Available AI Models

Current supported models:
- `@cf/meta/llama-3-8b-instruct` (default)
- `@cf/mistral/mistral-7b-instruct-v0.1`
- `@cf/meta/llama-3-70b-instruct`
- `@cf/google/gemma-7b-it`

## Error Handling

All endpoints return structured error responses:

```json
{
  "detail": "Error message description"
}
```

Common error scenarios:
- Invalid JSON in request body
- Missing required fields
- AI binding not available
- Model not found
- Rate limiting exceeded

## Rate Limits

Rate limiting is handled by Cloudflare Workers:
- 100,000 requests per day (free tier)
- 1,000 requests per minute per IP

## Examples

### cURL Examples

**Basic chat**:
```bash
curl -X POST "https://your-worker.workers.dev/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is machine learning?"}'
```

**With specific model**:
```bash
curl -X POST "https://your-worker.workers.dev/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum physics",
    "model": "@cf/meta/llama-3-70b-instruct"
  }'
```

**Health check**:
```bash
curl "https://your-worker.workers.dev/health"
```

### JavaScript Examples

**Using fetch**:
```javascript
const response = await fetch('/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Hello, AI!',
    model: '@cf/meta/llama-3-8b-instruct'
  })
});

const data = await response.json();
console.log(data.response);
```

**WebSocket connection**:
```javascript
const ws = new WebSocket('wss://your-worker.workers.dev/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    message: 'Hello via WebSocket',
    type: 'chat'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data.message);
};
```

### Python Examples

**Using requests**:
```python
import requests

response = requests.post(
    'https://your-worker.workers.dev/chat',
    json={
        'message': 'What is the meaning of life?',
        'model': '@cf/meta/llama-3-8b-instruct'
    }
)

data = response.json()
print(data['response'])
```

**Using websockets**:
```python
import asyncio
import websockets
import json

async def chat():
    uri = "wss://your-worker.workers.dev/ws"
    async with websockets.connect(uri) as websocket:
        message = {
            'message': 'Hello from Python',
            'type': 'chat'
        }
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        data = json.loads(response)
        print(data['message'])

asyncio.run(chat())
```

## Response Format

All API responses follow consistent formatting:

### Successful Response
```json
{
  "response": "Generated AI response text",
  "model_used": "@cf/meta/llama-3-8b-instruct"
}
```

### Error Response
```json
{
  "detail": "Descriptive error message"
}
```

## Performance Considerations

- **Response Time**: Typically 1-5 seconds depending on model and message length
- **Token Limits**: Maximum 1024 tokens per response (configurable)
- **Concurrent Requests**: Handled automatically by Cloudflare Workers
- **Geographic Performance**: Responses are served from Cloudflare's global edge network

## Model Comparison

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `@cf/meta/llama-3-8b-instruct` | Fast | Good | General chat |
| `@cf/mistral/mistral-7b-instruct-v0.1` | Fast | Good | Code/Technical |
| `@cf/meta/llama-3-70b-instruct` | Slow | Excellent | Complex reasoning |
| `@cf/google/gemma-7b-it` | Medium | Good | Balanced |
