#!/usr/bin/env python3
"""
Local development server for Mad Scientist AI Chat
This runs FastAPI directly without Cloudflare Workers for local testing
"""

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import json
import os

app = FastAPI(title="Mad Scientist AI Chat (Local Dev)", description="Local development version")

class ChatMessage(BaseModel):
    message: str
    model: str = "mock-model"

class ChatResponse(BaseModel):
    response: str
    model_used: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mad Scientist AI Chat (Local Dev)</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #0f0f23; color: #cccccc; }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { color: #00ff41; text-align: center; font-family: 'Courier New', monospace; }
            .dev-notice { background: #ff6b35; color: white; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
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
            <div class="dev-notice">
                <strong>🚧 LOCAL DEVELOPMENT MODE</strong><br>
                This is running FastAPI directly with mock AI responses. Deploy to Cloudflare for real AI.
            </div>
            
            <h1>🧪 Mad Scientist AI Chat 🧪</h1>
            <p style="text-align: center; font-style: italic;">What perplexes you? (Mock AI responses for local testing)</p>
            
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
async def chat_endpoint(chat_message: ChatMessage):
    """Mock chat endpoint for local development"""
    
    # Mock AI responses for common questions
    mock_responses = {
        "hello": "Greetings, fellow scientist! Welcome to my laboratory of digital wonders! 🧪⚗️",
        "quantum": "Ah, quantum mechanics! The realm where particles dance in superposition and reality becomes beautifully uncertain! In quantum computing, we harness these quantum states - qubits that can be both 0 and 1 simultaneously - to perform calculations that would make classical computers weep with envy! 🌌",
        "ai": "Artificial Intelligence! My favorite creation! It's like teaching sand to think - we arrange silicon in clever patterns and suddenly it can recognize faces, write poetry, and engage in delightfully mad conversations like this one! 🤖✨",
        "science": "Science is the art of organized curiosity! We observe, hypothesize, experiment, and occasionally blow things up in the name of knowledge! The universe is our laboratory, and every question leads to ten more delicious mysteries! 🔬🌟",
        "python": "Ah, Python! Not the snake, but the programming language that's as elegant as a serpent's movement! Named after Monty Python, it proves that coding can have a sense of humor. Clean syntax, powerful libraries, and perfect for mad science experiments! 🐍💻"
    }
    
    # Generate response based on keywords in the message
    message_lower = chat_message.message.lower()
    response = "Most fascinating question! As a mad scientist, I believe the universe is full of delightful mysteries waiting to be unraveled! While I'm currently running in development mode with mock responses, imagine the real AI would provide deep insights about your query! 🧪⚡"
    
    for keyword, mock_response in mock_responses.items():
        if keyword in message_lower:
            response = mock_response
            break
    
    return ChatResponse(
        response=response,
        model_used="mock-mad-scientist-v1.0"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "mad-scientist-ai-chat-local",
        "mode": "development",
        "ai_status": "mock_responses"
    }

if __name__ == "__main__":
    print("🧪 Starting Mad Scientist AI Chat (Local Development)")
    print("📍 Open http://localhost:8000 in your browser")
    print("📚 API docs available at http://localhost:8000/docs")
    print("🔬 Running with mock AI responses for local testing")
    
    uvicorn.run(
        "local_dev:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
