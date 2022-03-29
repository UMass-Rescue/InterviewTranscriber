import json
import os
import requests
from fastapi import Request, FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from transcribe_audio import Transcriber

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def transcribe(audio_filename: str, questions: []):
    model_path = "/opt/vosk-model-en/model"

    transcriber = Transcriber(model_path)
    text = transcriber.transcribe(audio_filename)
    print(text)

    analyze(text, questions)

def analyze(text, questions):

    input = {}
    input['full_text'] = text
    input['questions'] = questions

    nlp_tools_hostname = os.getenv("NLP_TOOLS_HOSTNAME", "worker_example")
    nlp_tools_port = os.getenv("NLP_TOOLS_PORT", "8001")

    response = requests.post(
        f"http://{nlp_tools_hostname}:{nlp_tools_port}/analyzeText/",
        json=input,
    )

    # return the transcription
    print(response.json())

    # # Will be a post request to the backend to save the transcription in the db
    # response = requests.post(
    #     f"http://{backend_hostname}:{backend_port}/transcribed_text/",
    #     response.json,
    # )


# route : http://127.0.0.1:5000/sendTranscription
# Expected post json:
# {
#     "audio_filename": "short_test_audio"
#     "questions" : ["Slide the box into that empty space.", "She danced like a swan tall and graceful."]
# }
@app.post('/sendTranscription')
async def return_route(request: Request, background_tasks: BackgroundTasks):
    # get the request
    request_json = await request.json()
    audio_filename = request_json['audio_filename']
    questions = request_json['questions']

    background_tasks.add_task(transcribe, audio_filename=audio_filename, questions=questions)
    return {"message": "Transcription has started."}


# to run the server, just run python server.py
if __name__ == '__main__':
    print("Starting the server...")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)