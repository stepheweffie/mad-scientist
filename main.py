
from fastapi import FastAPI, HTTPException, Query, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from mad_scientist import MadScientist, get_avatar_data_url, AI, brain_options, art_options, inputs
from static import css_styles
import requests
import httpx
import logging
from urllib.parse import quote, urlencode

logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.add_middleware(SessionMiddleware, secret_key="secret")
app_name = "Mad Scientist"
durl = {}

@app.get("/models", response_model=list[AI], response_class=PlainTextResponse)
async def models(request: Request):
    mad_scientist = MadScientist(request)
    models = mad_scientist.get_models()
    return models 

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

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mad Scientist AI</title>
    <style>{css_styles}</style>
</head>
<body>
    <div class="centered form-containter">
    <h1>Mad Scientist AI</h1>
    <form action="/generate-avatar/" method="get">
    <o>Language Model</p>
    <select class="message custom-select input-element" id="modelName" name="brain_model" required>
        {brain_options}
    </select><br><br>
    <o>Image Model</p>
    <select class="message custom-select input-element" id="modelName" name="image_model" required>
        {art_options}
    </select><br>
    <p>Image Prompt Input<p/>
    <textarea class="chat-input" placeholder="A Mad Scientist" name="prompt" rows="4" cols="50"></textarea><br><br> <!-- Added textarea for entering text -->
    <button class="input-element submit" type="submit">Experiment!</button>
    </form>
    </div>
</body>
</html>
"""

@app.get("/")
async def root(request: Request):
    mad_scientist = MadScientist(request)
    messages = await mad_scientist.set_session(request=request, variable="messages", data='')
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/generate-avatar/")
async def generate_avatar(request: Request, brain_model: str = Query(None), image_model: str = Query(None), prompt: str = Query(None)):
    mad_scientist = MadScientist(request)
    data_url = await get_avatar_data_url(request, img_model=image_model, prompt_text=prompt)
    durl['data_url'] = data_url
    avatar_page = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mad Scientist AI</title>
    <style>{css_styles}</style>
    </head>
    <body>
    <div class="centered form-containter">
    <div>
    <img src={data_url}>
    </div>
    <center><h1>Mad Scientist AI</h1>
    <div class="column">
    <form action='/mad-scientist/' method="get">
    <input type="hidden" name="brain_model" value="{brain_model}">
    <input type="hidden" name="image_model" value="{image_model}">
    <input type="hidden" name="prompt" value="{prompt}">
    <button class="input-element avatar-button submit" type="submit">Save & Use</button>
    </form>
    </div>
    <div class="column">
    <form action='/generate-avatar/' method="get">
    <button class="input-element avatar-button submit" type="submit">Regenerate</button>
    </form>
    </div>
    </center>
    </div>
    </div>
    '''
    return HTMLResponse(content=avatar_page, status_code=200)


@app.get("/mad-scientist/")
async def get_chat(request: Request, brain_model: str = Query(None), image_model: str = Query(None), prompt: str = Query(None)):
    mad_scientist = MadScientist(request)
    if 'durl' not in request.session:
        data_url = durl['data_url']
        mad_scientist.set_session(request=request, variable="durl", data=data_url)
    else:
        data_url = mad_scientist.get_session(request, "durl")
        
    ai_intro = await mad_scientist.chat_message(request, brain_model, inputs)
    
    # Retrieve 'messages' from the session
    messages = await mad_scientist.get_session(request=request, variable="messages")

    # Render the chat template with the session data
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "css_styles": css_styles,
        "brain_model": brain_model,
        "app_name": app_name,
        "messages": messages,
        "durl": data_url,
        "intro": ai_intro,
    })


@app.post("/mad-scientist/")
async def post_chat(request: Request, prompt: str = Form(...), brain_model: str = Form(...)):
    mad_scientist = MadScientist(request)
    data = f'{PROMPT_INTRO}'
    # Initialize 'messages' in the session if it doesn't exist
    if 'messages' not in request.session:
        await mad_scientist.set_session(request=request, variable="messages", data=data)
        ai_response = await mad_scientist.chat_message(brain_model, prompt)
    messages = await mad_scientist.get_session(request=request, variable="messages")
    messages.append({"user": prompt, "ai": ai_response})
    
    # Redirect back to the chat page to display the updated chat history
    return templates.TemplateResponse("chat.html", {"request": request, "css_styles": css_styles, "brain_model": brain_model, "app_name": app_name, "messages": messages
                                                    ,"durl": data_url})

'''
@app.get("/mad-scientist/dr-jorpy/", response_class=JSONResponse)
async def dr_jorpy(request: Request, token: Token = Depends()):
    mad_scientist = MadScientist(request)
    # ai_response = mad_scientist.jorpy_reply(token=token)
    # return ai_response
'''
