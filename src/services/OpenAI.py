from pathlib import Path
from openai import OpenAI
import uuid

# Create a UUID for the speech file
speech_file_path = Path(f"../../audio_output/openai/{uuid.uuid4()}.wav")

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
    

    def generate_conversation_from_array(self, conversation):
        return conversation

    # Generate dispatcher response from conversation using Assistant model
    def generate_dispatcher_response(self, message, assistant_id, thread_id = ""):
        # Generate a Thread if there is no thread:
        if thread_id == "":
            thread_id = self.client.assistant.create_thread().id

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id= thread_id,
            assistant_id= assistant_id,
            instructions="Please address the user as Jane Doe. The user has a premium account."
        )

        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(
                thread_id=thread_id,
            )
            print(messages)
            return messages
        else:
            print(run.status)
            return run.status

    
    def generate_review_response(self, conversation, model, prompt):
        return conversation
    
    