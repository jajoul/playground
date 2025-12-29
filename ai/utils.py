
from google import genai
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_ai_response(model='gemini-2.5-flash-tts',bot_name='tuffus',colleague_name='muffin',subject='', history=None):
    system_instruction=[f'your name is {bot_name} and here your colleague is called {colleague_name}.\n talk seriouslly about {subject}']
    
    model_instance = client.models.generate_content(
        model=model,
        config=GenerateContentConfig(system_instruction=system_instruction),
        contents='start the conversation'
    )

    if history is None:
        history = []

    formatted_history = []
    for msg in history:
        if msg['role'] == bot_name:
            api_role = 'model'
        else:
            api_role = 'user'
        formatted_history.append({"role": api_role, "parts": [{"text": msg['content']}]})

    contents = formatted_history
    if not contents:
        contents = [{'role': 'user', 'parts': [{'text': f'Hello {bot_name}, let\'s talk about {subject}.'}]}]

    response = model_instance.text
    
    if response:
        return response
    return ""
