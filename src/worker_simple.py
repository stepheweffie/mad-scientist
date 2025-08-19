async def on_fetch(request, env, ctx):
    """Handle incoming requests"""
    
    url = str(request.url)
    method = request.method
    
    # Health check
    if url.endswith("/health"):
        return Response.json({
            "status": "healthy",
            "service": "mad-scientist-ai-chat"
        })
    
    # Chat endpoint
    if method == "POST" and "/chat" in url:
        return await handle_chat(request, env)
    
    # Default - serve HTML interface
    return serve_html()


async def handle_chat(request, env):
    """Handle AI chat requests"""
    try:
        # Parse request body
        body = await request.json()
        message = body.get("message", "")
        
        if not message:
            return Response.json({"error": "Message required"}, status=400)
        
        # Get AI binding
        ai = env.AI
        
        if not ai:
            return Response.json({"error": "AI binding not available"}, status=500)
        
        # Call Cloudflare Workers AI
        messages = [
            {"role": "system", "content": "You are a helpful mad scientist assistant. Be creative, enthusiastic, and slightly eccentric in your responses while remaining helpful and accurate."},
            {"role": "user", "content": message}
        ]
        
        ai_response = await ai.run("@cf/meta/llama-3-8b-instruct", {
            "messages": messages,
            "max_tokens": 1024,
            "temperature": 0.7
        })
        
        return Response.json({
            "response": ai_response["response"],
            "model_used": "@cf/meta/llama-3-8b-instruct"
        })
        
    except Exception as e:
        return Response.json({"error": f"Chat error: {str(e)}"}, status=500)


def serve_html():
    """Serve the main HTML interface"""
    html = """
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
        .live-badge { position: fixed; top: 10px; right: 10px; background: #00ff41; color: #0f0f23; padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="live-badge">🚀 LIVE on mad-scientist.chat</div>
    <div class="container">
        <h1>🧪 Mad Scientist AI Chat 🧪</h1>
        <p style="text-align: center; font-style: italic;">What perplexes you today? Ask the AI anything!</p>
        
        <div class="chat-container">
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="Enter your question..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">Send</button>
            </div>
            <div id="response" class="response" style="display: none;"></div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <p><strong>🧪 Powered by Cloudflare Workers AI</strong></p>
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
        
        // Auto-focus input on page load
        window.onload = () => document.getElementById('messageInput').focus();
    </script>
</body>
</html>
    """
    
    return Response(html, headers={"Content-Type": "text/html"})
