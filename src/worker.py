from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Mad Scientist AI Chat", description="An AI-powered chat interface using Cloudflare Workers AI")

class ChatMessage(BaseModel):
    message: str
    model: str = "@cf/meta/llama-3-8b-instruct"

class ChatResponse(BaseModel):
    response: str
    model_used: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mad Scientist AI Chat</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #0f0f23; color: #cccccc; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #00ff41; text-align: center; font-family: 'Courier New', monospace; }
            .chat-container { border: 2px solid #00ff41; border-radius: 10px; padding: 20px; margin: 20px 0; }
            .input-group { display: flex; gap: 10px; margin-top: 20px; }
            input[type="text"] { flex: 1; padding: 10px; background: #1a1a2e; border: 1px solid #00ff41; color: #cccccc; border-radius: 5px; }
            button { padding: 10px 20px; background: #00ff41; color: #0f0f23; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
            button:hover { background: #00cc33; }
            .response { margin-top: 20px; padding: 15px; background: #1a1a2e; border-left: 4px solid #00ff41; border-radius: 5px; }
            .loading { color: #00ff41; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 Mad Scientist AI Chat 🧪</h1>
            <p style="text-align: center; font-style: italic;">What perplexes you? Ask the AI anything!</p>
            
            <div class="chat-container">
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Enter your question..." onkeypress="if(event.key==='Enter') sendMessage()">
                    <button onclick="sendMessage()">Send</button>
                </div>
                <div id="response" class="response" style="display: none;"></div>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p><strong>Available Endpoints:</strong></p>
                <p>• <a href="/docs" style="color: #00ff41;">API Documentation</a></p>
                <p>• <a href="/chat" style="color: #00ff41;">Direct Chat API</a></p>
                <p>• <a href="/health" style="color: #00ff41;">Health Check</a></p>
            </div>
        </div>
        
        <script>
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const responseDiv = document.getElementById('response');
                const message = input.value.trim();
                
                if (!message) return;
                
                responseDiv.style.display = 'block';
                responseDiv.innerHTML = '<div class="loading">🧪 The mad scientist is thinking...</div>';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    
                    if (!response.ok) throw new Error('Network response was not ok');
                    
                    const data = await response.json();
                    responseDiv.innerHTML = `<strong>Question:</strong> ${message}<br><br><strong>Answer:</strong> ${data.response}`;
                    input.value = '';
                } catch (error) {
                    responseDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage, request: Request):
    """Main chat endpoint that processes user messages through Cloudflare Workers AI"""
    try:
        # Get the AI binding from the request environment
        env = request.scope.get('env', {})
        ai_binding = env.get('AI')
        
        if not ai_binding:
            raise HTTPException(status_code=500, detail="AI binding not available")
        
        # Prepare the prompt for the AI model
        messages = [
            {"role": "system", "content": "You are a helpful mad scientist assistant. Be creative, enthusiastic, and slightly eccentric in your responses while remaining helpful and accurate."},
            {"role": "user", "content": chat_message.message}
        ]
        
        # Call Cloudflare Workers AI
        response = await ai_binding.run(
            chat_message.model,
            {
                "messages": messages,
                "max_tokens": 1024,
                "temperature": 0.7
            }
        )
        
        # Extract the response text
        ai_response = response.get('response', 'No response generated')
        
        return ChatResponse(
            response=ai_response,
            model_used=chat_message.model
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mad-scientist-ai-chat"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat (future enhancement)"""
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Echo back for now (can be enhanced with AI integration)
            response = {
                "type": "response",
                "message": f"Echo: {message_data.get('message', '')}",
                "timestamp": "now"
            }
            
            await websocket.send_text(json.dumps(response))
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

