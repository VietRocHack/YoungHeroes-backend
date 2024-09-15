from pathlib import Path
from openai import OpenAI
import uuid
import json

# Create a UUID for the speech file. If there is not path, create one
speech_file_path = Path(__file__).parent.parent.parent / f"audio_output\openai\{uuid.uuid4()}.mp3"

class OpenAIService:
    # client: OpenAI client
    # api_key: str

    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key = api_key)

    # Generate speech from text, save to file
    def generate_speech(self, text, voice, model):
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)
        return speech_file_path

    # Generate a new chat thread for OpenAI Assistant
    def new_chat(self):
        thread_id = self.client.beta.threads.create().id
        return thread_id

    # Generate dispatcher response from conversation using Assistant model. Also advances the thread
    def generate_dispatcher_response(self, message, assistant_id, thread_id = ""):
        # Create a message in the thread
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )

        # Create and poll a run for the thread
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Retrieve the thread and messages if the run is completed
        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(
                thread_id=thread_id,    
            )
            newest_message = messages.data[0].content[0].text.value
            print(newest_message)
            return thread_id, newest_message
        else:
            return thread_id, run.status

    def get_call_states(self, id):
        messages = self.client.beta.threads.messages.list(
            thread_id=id,    
        )

        message = json.loads(messages.data[0].content[0].text.value)
        print(message)
        return message['isFinished'], message['isPrankCall']

    # Generate call logs from a thread
    def generate_call_logs(self, id):
        messages = self.client.beta.threads.messages.list(
            thread_id=id,    
        )

        message_list = []

        is_operator_call = len(messages.data) % 2 != 0
        for message in messages.data:
            is_operator_call = not is_operator_call
            if is_operator_call:
                message_list.insert(0, json.loads(message.content[0].text.value)["message"])
            else:
                message_list.insert(0, message.content[0].text.value)
        
        return message_list
        
    def generate_review_response(self, conversation, model, prompt):
        return conversation
    
    def speech_to_text(self, path):
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=open(path, "rb"),
        )
        return response.text
    
    