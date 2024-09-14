# YoungHeroes-backend
To run the API server:

## Setup the Python Server:

`python -m venv env` (create a virtual environment)

`env/Scripts/activate` (or a similar command to start a Python virtual env on a different OS)

`pip install -r requirements.txt` (install requirements. this should take quite long, don't worry)

## Setup .env files (and OpenAI):

You need to create an '.env' file in the 'src' folder. The file should have these variables:

`OPENAI_API_KEY=(your OpenAI API Key)`

`OPENAI_ASSISTANT_DISPATCHER_ID=(your OpenAI Assistant ID)`

`TTS_MODEL=(The OpenAI Dispatch Model, we used tts-1)`

`TTS_VOICE=(The OpenAI Voice used, we used onyx)`

## Run the Python Server

`python src/server.py` (or a similar command to run a Python script on a different OS)

