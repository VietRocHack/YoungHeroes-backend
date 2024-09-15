import os
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask import request, send_file, jsonify
from services.OpenAI import OpenAIService
import whisper

from dotenv import load_dotenv 

import json

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv('OPENAI_API_KEY')

HTTP_OK = 200
HTTP_BAD_REQUEST = 400

VOICE = os.getenv('TTS_VOICE')
MODEL = os.getenv('TTS_MODEL')
ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_DISPATCHER_ID')

openai = OpenAIService(os.getenv('OPENAI_API_KEY'))
whisper_model = whisper.load_model("tiny.en")

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api')
def api():
    return 'Welcome to the API!'

# Return the ID of a new chat thread
@app.route('/api/new_call', methods=['GET'])
def new_chat():
    id = openai.new_chat()
    return id, HTTP_OK

# Return the audio file of the response from the dispatcher
@app.route('/api/tts/', methods=['GET'])
def tts():
    text = request.args.get('text')
    id = request.args.get('callId')
    if text and id:
        id, text_message = openai.generate_dispatcher_response(text, assistant_id=ASSISTANT_ID, thread_id=id)
        text_tts_path = openai.generate_speech(json.loads(text_message)["message"], VOICE, MODEL)
        print(text_tts_path)
        return send_file(Path(str(text_tts_path).replace("..\\\\", "", 1))), HTTP_OK
    elif not text:
        return 'text parameter is missing.', HTTP_BAD_REQUEST
    else:
        return 'id parameter is missing.', HTTP_BAD_REQUEST
    
# Return the state of the call from the dispatcher
@app.route('/api/get_call_states', methods=['GET'])
def call_states():
    id = request.args.get('callId')
    if id:
        messages = openai.get_call_states(id)
        return jsonify(messages), HTTP_OK
    else:
        return 'id parameter is missing.', HTTP_BAD_REQUEST

# Return the call logs from the dispatcher
@app.route('/api/get_call_log', methods=['GET'])
def call_logs():
    id = request.args.get('callId')
    if id:
        messages = openai.generate_call_logs(id)
        return jsonify(messages), HTTP_OK
    else:
        return 'id parameter is missing.', HTTP_BAD_REQUEST
    
# Return the Speech-to-text
@app.route('/api/stt', methods=['POST'])
def speech_to_text():
    # Check if an audio file is provided in the request
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    print(audio_file)
    try:
        audio_file.save("./audio_new.m4a")
        # Use Whisper to transcribe the audio
        print(audio_file)
        return openai.speech_to_text("./audio_new.m4a"), HTTP_OK
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Remove the temporary file
        if os.path.exists("./audio_new.m4a"):
            os.remove("./audio_new.m4a")

if __name__ == '__main__':
    app.run()