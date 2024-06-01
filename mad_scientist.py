from fastapi import HTTPException, Request, Query
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import base64
from settings import ACCOUNT_ID, AUTH_TOKEN, API_BASE_URL
from typing import Any, Dict
# from mad_sci_mistral_instruct import tokenizer
import requests
ACCOUNT_ID = ACCOUNT_ID
AUTH_TOKEN = AUTH_TOKEN
API_BASE_URL = API_BASE_URL
headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}

# Data for AI models
models = [
     {
        "model": "Mad Sci Mistral-7B Instruct",
        "description": "Mad Sci is a fine-tuned version of the Mistral-7b Instruct generative text model with 7 billion parameters",
        "mid": "SavantofIllusions/mad_sci_mistral_instruct",
        "name": "mad_sci_mistral_instruct",
        "usage": "text"
    },
    {
        "model": "Mistral-7b Instruct",
        "description": "Instruct fine-tuned version of the Mistral-7b generative text model with 7 billion parameters",
        "mid": "@cf/mistral/mistral-7b-instruct-v0.1",
        "name": "mistral_7b_instruct",
        "usage": "mad-sci-text"
    },
    {
        "model": "Hermes 2 Pro on Mistral 7B",
        "description": "Hermes 2 Pro on Mistral 7B is the new flagship 7B Hermes! Hermes 2 Pro is an upgraded, retrained version of Nous Hermes 2, consisting of an updated and cleaned version of the OpenHermes 2.5 Dataset, as well as a newly introduced Function Calling and JSON Mode dataset developed in-house",
        "mid": "@hf/nousresearch/hermes-2-pro-mistral-7b",
        "name": "hermes_2_pro_on_mistral_7b",
        "usage": "text"
    },
    {
        "model": "Dreamshaper-8 LCM",
        "description": "Stable Diffusion model that has been fine-tuned to be better at photorealism without sacrificing range",
        "mid": "@cf/lykon/dreamshaper-8-lcm",
        "name": "dreamshaper_8_lcm",
        "usage": "art"
    }
]



brain_options = ""
art_options = ""
for model in models:
    option = f"<option value='{model['model']}'>{model['model']}</option>"
    if model['usage'] == 'mad-sci-text':
        brain_options += option
    elif model['usage'] == 'art':
        art_options += option

inputs = [
    { "role": "system", "content": """You are a scientist who is very meticulous about word and phrase ambiguation.
      You will attempt to recognize common mistakes in the usage of terms that are present in scientific theories.
      You will not present information as if it is understood to not be definitive. You will not attempt to confuse people.
      If you are given a statement you will rephrase it as a question and then proceed to answer the question as
      if you have been asked that question in the original input.
      You will offer examples that counter false assumptions made in the input.""" },
    { "role": "user", "content": """You are the Mad Scientist AI, my new assistant. Introduce us as such."""}
]

class AI(BaseModel):
    model: str
    description: str
    mid: str
    name: str
    usage: str

class Token(BaseModel):
    access_token: str
    token_type: str

async def get_avatar_data_url(request: Request, img_model: str, prompt_text: str):
    mad_sci = MadScientist(request)
    model_name_response = await mad_sci.get_model_name_by_model(request, model=img_model)
    model_name = model_name_response.strip()  # Remove leading/trailing whitespace
    mid_response = await mad_sci.get_mid_by_model_name(request, model=model_name)
    mid = mid_response.strip()  # Remove leading/trailing whitespace
    
    # Prepare the JSON payload according to the input schema
    json_payload = {
        "prompt": prompt_text,
            # Add other fields if necessary
            # "num_steps": 20,
            # "strength": 1,
            # "guidance": 7.5,
    }
    
    # Make the API call
    response = requests.post(
        f"{API_BASE_URL}{mid}",
        headers=headers,
        json=json_payload
    )
    
    if response.status_code == 200:
        # Assuming the response.content is the binary image data
        image_data = response.content
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        data_url = f"data:image/png;base64,{image_base64}"
        return data_url
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to generate image")

class MadScientist:
    def __init__(self, request: Request):
        self.request = request
        self.image_generated = False
        self.auth = False

    async def set_session(self, request: Request, variable: str, data: Any):
        if self.request.session is not None:
            self.request.session[variable] = data
        else:
            raise HTTPException(status_code=500, detail="Session not initialized")

    async def get_session(self, request: Request, variable: str) -> Any:
        if self.request.session is not None and variable in self.request.session:
            return self.request.session[variable]
        return None

    async def clear_session(self, request: Request):
        request.session.clear()  # Clear the session
        return {"message": "Session cleared"}

    async def get_models(self, request: Request):
        return [AI(**mod) for mod in models]

    async def get_model_by_name(self, request: Request, model: str):
        for mod in models:
            if mod["name"] == model:
                return AI(**mod)
        return {"model": model, "description": "Model Not Found", "_id": "model_not_found", "name": model} 

    async def get_mid_by_model_name(self, request: Request, model: str):
        for mod in models:
            if mod["name"] == model:
                return mod["mid"]

    async def get_model_name_by_model(self, request: Request, model: str):
        for mod in models:
            if mod["model"] == model:
                return mod["name"]
            

    async def chat(self, request: Request, mod_id: str, user_message: str) -> dict:
        # Update the user's message within the inputs structure
        if type(user_message) is list:
            updated_inputs = user_message
        else:
            updated_inputs = [{"role": "user", "content": user_message}]
        payload = {
        "messages": updated_inputs}  # Use the updated inputs with the user's message
        # Send the request to the AI model
        response = requests.post(
        f"{API_BASE_URL}{mod_id}",
        headers=headers,
        json=payload)
        result = response.json()
        # Check for a successful response and extract the reply
        if response.status_code == 200:
            if 'result' in result and 'response' in result['result']:
                data = {"message": result['result']['response'], "model": mod_id, "prompt": user_message}
                    
                ai_response = result['result']['response']
                # Append the user message and AI response to the session messages
                messages = await self.get_session(request, "messages") or []
                messages.append({
                    "user": user_message,
                    "ai": ai_response
                })
                await self.set_session(request=request, variable="messages", data=messages)
                return ai_response
        else:
            # Handle any errors from the API call
            raise HTTPException(status_code=response.status_code, detail="Failed to call AI model")


    async def finetuned_chat(self, request: Request, mod_id: str, user_message: str) -> dict:
        # Update the user's message within the inputs structure
        if isinstance(user_message, list):
            updated_inputs = user_message
        else:
            updated_inputs = [{"role": "user", "content": user_message}]
        # Prepare the input for the model
        inputs = tokenizer(user_message, return_tensors="pt")
        # Generate a response using the model
        with torch.no_grad():
            outputs = model.generate(**inputs)
        # Decode the generated response
        ai_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Prepare the response data
        data = {"message": ai_response, "model": mod_id, "prompt": user_message}        
        return ai_response

        
    async def chat_message(self, request: Request, brain_model: str, message: str) -> str:
        try:
            # Call the /models/{model} route to get the model name
            model_name_response = await self.get_model_name_by_model(request, brain_model)
            model_name = model_name_response.strip()  # Remove leading/trailing whitespace
        except HTTPException as e:
            logger.error(f"Failed to get model name for {brain_model}: {e}")
            return HTMLResponse(content=f"Model not found: {brain_model}", status_code=404)
        try:
            mid_response = await self.get_mid_by_model_name(request, model_name)
            mid = mid_response.strip()  # Remove leading/trailing whitespace
            chat = await self.get_session(request=request, variable="chat")
            if chat is False:
                reply = await self.chat(request, mid, inputs)
                await self.set_session(request=request, variable="chat", data=True)
            else:
                reply = await self.chat(request, mid, message)
        except HTTPException as e:
            logger.error(f"Failed to get model id name for {model_name}: {e}")
            return HTMLResponse(content=f"Model not found: {brain_model}", status_code=404)
        
        await self.set_session(request=request, variable='chat', data=True)
        return reply
    
