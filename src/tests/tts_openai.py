from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the API key from the .env file
load_dotenv()
client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

# Path to save the speech file
# Put into the audio_output/openai folder
speech_file_path = Path("audio_output/openai/speech.wav")

response = client.audio.speech.create(
  model="tts-1",
  voice="onyx",
  input="Địt mẹ thằng hoàng ngu vl"
)

response.stream_to_file(speech_file_path)

