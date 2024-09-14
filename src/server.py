import os

from flask import Flask
from flask_cors import CORS
from flask import request, send_file
from services.OpenAI import OpenAIService

from dotenv import load_dotenv 

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv('OPENAI_API_KEY')

HTTP_OK = 200
HTTP_BAD_REQUEST = 400

VOICE = os.getenv('VOICE')
MODEL = os.getenv('MODEL')
ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_DISPATCHER_ID')

openai = OpenAIService(os.getenv('OPENAI_API_KEY'))

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api')
def api():
    return 'Welcome to the API!'

@app.route('/api/tts/', methods=['GET'])
def tts():
    text = request.args.get('text')
    if text:
        text_message = openai.generate_dispatcher_response(text, assistant_id=ASSISTANT_ID)
        return text_message, HTTP_OK
        # speech_file = openai.generate_speech(text, voice=VOICE, model=MODEL)
        
        # return "good", HTTP_OK
    else:
        return 'Text parameter is missing.', HTTP_BAD_REQUEST

if __name__ == '__main__':
    app.run()