
from fastapi import FastAPI, HTTPException, Query, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from mad_scientist import MadScientist, get_avatar_data_url, AI, brain_options, art_options, inputs, SECRET_KEY, GTAG
from static import css_styles
from logging_config import setup_logging, get_logger
import requests
import httpx
import logging
import os
from urllib.parse import quote, urlencode

# Setup logging
log_level = os.getenv("LOG_LEVEL", "INFO")
setup_logging(log_level)
logger = get_logger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app_name = "Mad Scientist"
durl = {}
responses = {}
responses['ai'] = []

@app.get("/models", response_model=list[AI], response_class=PlainTextResponse)
async def models(request: Request):
    logger.info("Fetching available models")
    try:
        mad_scientist = MadScientist(request)
        models = mad_scientist.get_models()
        logger.debug(f"Retrieved {len(models) if models else 0} models")
        return models
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch models")

@app.get("/models/{model}", response_model=list[AI], response_class=PlainTextResponse)
async def model_by_name(request: Request, model: str):
        mad_scientist = MadScientist(request)
        model_info = mad_scientist.get_model_by_name(model=model)
        return model_info
    
@app.get("/models/{model}/mid", response_class=PlainTextResponse)
async def id_by_model_name(model: str):
        mad_scientist = MadScientist(request)
        model_id = mad_scintist.get_mid_by_model_name(model=model)
        return model_id

@app.get("/models/{model}", response_class=PlainTextResponse)
async def model_api_name(model: str):
        mad_scientist = MadScientist(request)
        model_name = mad_scientist.get_model_name_by_model(model=model)
        return model_name

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mad Scientist AI - Model Selection</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>""" + css_styles + """</style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
</head>
<body>
    <div class="centered form-containter animate__animated animate__fadeIn">
        <h1>🧪 <span class="lab-title">Mad Scientist AI</span> 🧪</h1>
        
        <form action="/generate-avatar/" method="get" class="model-form">
            <div class="input-group">
                <label for="brain_model">Language Model</label>
                <select class="custom-select input-element" id="brain_model" name="brain_model" required>
""" + brain_options + """
                </select>
            </div>
            
            <div class="input-group">
                <label for="image_model">Image Model</label>
                <select class="custom-select input-element" id="image_model" name="image_model" required>
""" + art_options + """
                </select>
            </div>
            
            <div class="input-group">
                <label for="prompt">Avatar Prompt</label>
                <textarea 
                    class="input-element" 
                    placeholder="A Mad Scientist" 
                    name="prompt" 
                    id="prompt"
                    rows="4" 
                    required
                ></textarea>
            </div>
            
            <button class="submit" type="submit" onclick="this.innerHTML='🧪 Experimenting...'; this.classList.add('loading');">🧪 Start Experiment!</button>
        </form>
        
        <div class="lab-features">
            <div class="feature-grid">
                <div class="feature-item">
                    <span class="feature-icon">🤖</span>
                    <span>AI Models</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🎨</span>
                    <span>Custom Avatars</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">⚡</span>
                    <span>Instant Results</span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const promptInput = document.getElementById('prompt');
            const submitButton = document.querySelector('.submit');
            
            // Auto-focus on prompt input
            promptInput.focus();
            
            // Form validation
            document.querySelector('.model-form').addEventListener('submit', function(e) {{
                const brainModel = document.getElementById('brain_model').value;
                const imageModel = document.getElementById('image_model').value;
                const prompt = document.getElementById('prompt').value;
                
                if (!brainModel || !imageModel || !prompt.trim()) {{
                    e.preventDefault();
                    alert('Please fill in all fields before experimenting!');
                    submitButton.innerHTML = '🧪 Start Experiment!';
                    submitButton.classList.remove('loading');
                }}
            }});
            
            // Hover effects
            document.querySelector('.form-containter').addEventListener('mouseenter', function() {{
                this.style.transform = 'translate(-50%, -50%) scale(1.02)';
            }});
            
            document.querySelector('.form-containter').addEventListener('mouseleave', function() {{
                this.style.transform = 'translate(-50%, -50%) scale(1)';
            }});
        }});
    </script>
    
    <style>
        .model-form .input-group {
            margin-bottom: 1.5rem;
        }
        
        .model-form .input-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--glow-color);
            font-weight: 500;
        }
        
        .model-form textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        .lab-features {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--primary-color);
        }
        
        .feature-grid {
            display: flex;
            justify-content: space-around;
            gap: 1rem;
        }
        
        .feature-item {
            text-align: center;
            padding: 0.5rem;
            transition: transform 0.3s ease;
        }
        
        .feature-item:hover {
            transform: scale(1.1);
        }
        
        .feature-icon {
            display: block;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }
        
        .form-containter {
            transition: all 0.3s ease;
        }
    </style>
</body>
</html>
"""

initial_html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mad Scientist AI - Laboratory Access</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>{css_styles}</style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
</head>
<body>
    <div class="centered form-containter">
        <h1>🧪 <span class="lab-title">Mad Scientist AI</span> 🧪</h1>
        
        <form action="/verify-email/" method="post" class="access-form">
            <div class="input-group">
                <label for="email">Email</label>
                <input 
                    class="input-element" 
                    type="email" 
                    name="email" 
                    id="email"
                    placeholder="Email address" 
                    required
                    autocomplete="email"
                >
            </div>
            
            <button 
                class="submit" 
                type="submit"
                onclick="this.innerHTML='Loading...'; this.classList.add('loading');"
            >
                Continue
            </button>
        </form>
        
        <div class="lab-features">
            <div class="feature-grid">
                <div class="feature-item">
                    <span class="feature-icon">🔮</span>
                    <span>AI Oracle</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">✨</span>
                    <span>Mystical Avatars</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">💫</span>
                    <span>Arcane Magic</span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const emailInput = document.getElementById('email');
            const submitButton = document.querySelector('.submit');
            
            // Auto-focus on email input
            emailInput.focus();
            
            // Enhanced form validation
            emailInput.addEventListener('input', function() {{
                const email = this.value;
                if (email.includes('@') && email.includes('.')) {{
                    this.style.borderColor = 'var(--glow-color)';
                }} else {{
                    this.style.borderColor = 'var(--primary-color)';
                }}
            }});
            
            // Add subtle scale effect on hover
            document.querySelector('.form-containter').addEventListener('mouseenter', function() {{
                this.style.transform = 'translate(-50%, -50%) scale(1.02)';
            }});
            
            document.querySelector('.form-containter').addEventListener('mouseleave', function() {{
                this.style.transform = 'translate(-50%, -50%) scale(1)';
            }});
        }});
    </script>
    
    <style>
        .lab-intro {{
            margin-bottom: 2rem;
            padding: 1rem;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--primary-color), var(--surface-color));
        }}
        
        .input-group {{
            margin-bottom: 1.5rem;
        }}
        
        .input-group label {{
            display: block;
            margin-bottom: 0.5rem;
            color: var(--glow-color);
            font-weight: 500;
        }}
        
        .lab-features {{
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--primary-color);
        }}
        
        .feature-grid {{
            display: flex;
            justify-content: space-around;
            gap: 1rem;
        }}
        
        .feature-item {{
            text-align: center;
            padding: 0.5rem;
            transition: transform 0.3s ease;
        }}
        
        .feature-item:hover {{
            transform: scale(1.1);
        }}
        
        .feature-icon {{
            display: block;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .form-containter {{
            transition: all 0.3s ease;
        }}
    </style>
</body>
</html>
"""

@app.get("/")
async def root(request: Request):
    logger.info("Root endpoint accessed")
    try:
        mad_scientist = MadScientist(request)
        messages = await mad_scientist.set_session(request=request, variable="messages", data='')
        token = await mad_scientist.set_session(request=request, variable="token", data='')    
        logger.debug("Session initialized for new user")
        return HTMLResponse(content=initial_html_content, status_code=200)
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/generate-avatar/")
async def generate_avatar(request: Request, brain_model: str = Query(None), image_model: str = Query(None), prompt: str = Query(None)):
    logger.info(f"Generating avatar with model: {image_model}, prompt: {prompt}")
    try:
        mad_scientist = MadScientist(request)
        data_url = await get_avatar_data_url(request, img_model=image_model, prompt_text=prompt)
        durl['data_url'] = data_url
        await mad_scientist.set_session(request=request, variable="chat", data=False)
        logger.debug("Avatar generated successfully")
    except Exception as e:
        logger.error(f"Error generating avatar: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate avatar")

    avatar_page = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mad Scientist AI - Avatar Created</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>{css_styles}</style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    </head>
    <body>
        <div class="centered form-containter animate__animated animate__zoomIn">
            <h1 class="animate__animated animate__pulse animate__infinite">🧪 Mad Scientist AI 🧪</h1>
            
            <div class="avatar-showcase animate__animated animate__fadeInDown animate__delay-1s">
                <div class="avatar-frame">
                    <img src="{data_url}" alt="Generated Mad Scientist Avatar" class="generated-avatar animate__animated animate__bounceIn animate__delay-2s">
                </div>
                <p class="avatar-success animate__animated animate__fadeInUp animate__delay-3s">
                    🎉 Your Mad Scientist Avatar is Ready! 🎉<br>
                    <span style="font-size: 0.9rem; color: var(--text-muted);">Prompt: "{prompt}"</span>
                </p>
            </div>
            
            <div class="avatar-actions animate__animated animate__slideInUp animate__delay-4s">
                <div class="action-buttons">
                    <form action='/mad-scientist/' method="get" style="display: inline-block;">
                        <input type="hidden" name="brain_model" value="{brain_model}">
                        <input type="hidden" name="image_model" value="{image_model}">
                        <input type="hidden" name="prompt" value="{prompt}">
                        <button 
                            class="submit avatar-button animate__animated animate__pulse animate__infinite" 
                            type="submit"
                            style="background: linear-gradient(135deg, var(--secondary-color), var(--glow-color)); margin-right: 1rem;"
                            onclick="this.innerHTML='🚀 Launching Chat...'; this.classList.add('loading');"
                        >
                            ✨ Save & Use Avatar ✨
                        </button>
                    </form>
                    
                    <form action='/generate-avatar/' method="get" style="display: inline-block;">
                        <input type="hidden" name="brain_model" value="{brain_model}">
                        <input type="hidden" name="image_model" value="{image_model}">
                        <input type="hidden" name="prompt" value="{prompt}">
                        <button 
                            class="submit avatar-button" 
                            type="submit"
                            style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color))"
                            onclick="this.innerHTML='🎲 Generating...'; this.classList.add('loading');"
                        >
                            🔄 Try Again
                        </button>
                    </form>
                </div>
                
                <div class="model-info animate__animated animate__fadeInUp animate__delay-5s">
                    <div class="info-grid">
                        <div class="info-item">
                            <span class="info-label">🤖 Brain Model:</span>
                            <span class="info-value">{brain_model}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">🎨 Image Model:</span>
                            <span class="info-value">{image_model}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                const avatar = document.querySelector('.generated-avatar');
                
                avatar.addEventListener('mouseenter', function() {{
                    this.style.transform = 'scale(1.1) rotate(5deg)';
                }});
                
                avatar.addEventListener('mouseleave', function() {{
                    this.style.transform = 'scale(1) rotate(0deg)';
                }});
                
                document.querySelectorAll('.avatar-button').forEach(button => {{
                    button.addEventListener('mouseenter', function() {{
                        this.style.animation = 'bounce 0.6s ease';
                    }});
                }});
            }});
        </script>
        
        <style>
            .avatar-showcase {
                text-align: center;
                margin: 2rem 0;
            }
            
            .avatar-frame {
                display: inline-block;
                padding: 10px;
                border: 3px solid var(--glow-color);
                border-radius: 50%;
                background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
                box-shadow: inset 0 0 20px var(--shadow-light);
                margin-bottom: 1rem;
            }
            
            .generated-avatar {
                width: 200px;
                height: 200px;
                border-radius: 50%;
                object-fit: cover;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .avatar-success {
                color: var(--glow-color);
                font-size: 1.2rem;
                font-weight: 600;
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .avatar-actions {
                text-align: center;
            }
            
            .action-buttons {
                margin-bottom: 2rem;
            }
            
            .avatar-button {
                margin: 0.5rem;
                padding: 15px 25px;
                font-size: 1rem;
                min-width: 200px;
                transition: all 0.3s ease;
            }
            
            .model-info {
                background: linear-gradient(135deg, var(--primary-color), var(--surface-color));
                padding: 1rem;
                border-radius: 10px;
                border-top: 1px solid var(--glow-color);
            }
            
            .info-grid {
                display: flex;
                justify-content: space-around;
                gap: 1rem;
            }
            
            .info-item {
                text-align: center;
            }
            
            .info-label {
                display: block;
                color: var(--glow-color);
                font-weight: 500;
                margin-bottom: 0.5rem;
            }
            
            .info-value {
                color: var(--text-color);
                font-size: 0.9rem;
            }
            
            @media (max-width: 768px) {{
                .action-buttons form {{
                    display: block !important;
                    margin: 0.5rem 0;
                }}
                
                .avatar-button {{
                    width: 100%;
                    margin: 0.5rem 0;
                }}
                
                .info-grid {{
                    flex-direction: column;
                    gap: 0.5rem;
                }}
            }}
        </style>
    </body>
    </html>
    '''
    return HTMLResponse(content=avatar_page, status_code=200)


@app.get("/mad-scientist/")
async def get_chat(request: Request, brain_model: str = Query(None), image_model: str = Query(None), prompt: str = Query(None)):
    mad_scientist = MadScientist(request)
    if len(durl) > 0:
        data_url = durl['data_url']
    else:
        data_url = await get_avatar_data_url(request, img_model=image_model, prompt_text='A Mad Scientist')
        durl['data_url'] = data_url
        
    chat = await mad_scientist.get_session(request=request, variable="chat")
    if chat is False:
        ai_intro = await mad_scientist.chat_message(request, brain_model, inputs)
        # Check it for obvious errors
        ai_intro = ai_intro.replace("Dr.", "").strip()
        ai_intro = ai_intro.replace("you are my", "I am your").strip()
        # Dummy message
        message = 'Hello, Mad Scientist AI. Please introduce yourself.'
        responses['intro'] = ai_intro
        return templates.TemplateResponse("chat.html", {
            "request": request,
            "css_styles": css_styles,
            "brain_model": brain_model,
            "app_name": app_name,
            "message": message,
            "durl": data_url,
            "response": responses['intro'],
        })
    
    else:
        return templates.TemplateResponse("chat.html", {
            "request": request,
            "css_styles": css_styles,
            "brain_model": brain_model,
            "app_name": app_name,
            "message": prompt,
            "durl": data_url,
            "response": responses['ai'][-1],
        })
            

@app.post("/mad-scientist/")
async def post_chat(request: Request, prompt: str = Form(...), brain_model: str = Form(...)):
    logger.info(f"Chat message received: {prompt[:100]}{'...' if len(prompt) > 100 else ''} using model: {brain_model}")
    try:
        mad_scientist = MadScientist(request)
        ai_response = await mad_scientist.chat_message(request, brain_model, prompt)
        # Redirect back to the GET chat page to display the updated chat history
        ai = responses['ai']
        ai.append(ai_response)
        logger.debug(f"AI response generated, length: {len(ai_response) if ai_response else 0}")
        response = RedirectResponse(
            url=f"/mad-scientist/?brain_model={brain_model}&app_name={app_name}&prompt={prompt}",
            status_code=303
        )
        response.set_cookie(key="session", value=request.session)  # Ensure the session cookie is updated
        return response
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat message")


@app.post("/verify-email/")
async def post_email(request: Request, email: str = Form(...)):
    response = RedirectResponse(
        url=f"/",
        status_code=303
    )
    return response


@app.get("/demo")
async def demo(request: Request):
    """Demo route that bypasses avatar generation for testing"""
    logger.info("Demo route accessed")
    try:
        mad_scientist = MadScientist(request)
        # Use a placeholder image instead of generating one
        placeholder_avatar = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzQ3MzIzZCIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTZweCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGRvbWluYW50LWJhc2VsaW5lPSJjZW50cmFsIj5NYWQgU2NpZW50aXN0PC90ZXh0Pjwvc3ZnPg=="
        durl['data_url'] = placeholder_avatar
        
        return templates.TemplateResponse("chat.html", {
            "request": request,
            "css_styles": css_styles,
            "brain_model": "Demo Mode",
            "app_name": app_name,
            "message": "Demo chat without API",
            "durl": placeholder_avatar,
            "response": "Welcome to Mad Scientist AI! This is demo mode - the chat AI is not connected but you can see the interface.",
        })
    except Exception as e:
        logger.error(f"Error in demo route: {str(e)}")
        return HTMLResponse(content=f"<h1>Demo Error: {str(e)}</h1>", status_code=500)

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and load balancers."""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "Mad Scientist AI",
        "version": "1.0.0",
        "timestamp": "2025-08-29T01:03:00Z"
    }


# @app.get("/mad-scientist/session/messages", response_model=list[MESSAGE], response_class=PlainTextResponse)
# async def get_messages(request: Request)
#    messages = await self.get_session(request, "messages") or []
#    return messages

