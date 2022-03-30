import os
from typing import List
import requests
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from transcribe_audio import Transcriber
import schemas

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def transcribe(audio_filename: str, questions: List[schemas.Question], interview_object: schemas.Interview):
    model_path = "/opt/vosk-model-en/model"

    transcriber = Transcriber(model_path)
    text = transcriber.transcribe(audio_filename)
    print(text)

    analyze(text=text, questions=questions, interview_object=interview_object)

def analyze(text: str, questions: List[schemas.Question], interview_object: schemas.Interview):
    print(questions)
    input = {}
    input['full_text'] = text
    input['questions'] = questions
    data = schemas.analyzerObj(full_text=text, questions=questions)

    nlp_tools_hostname = os.getenv("NLP_TOOLS_HOSTNAME", "worker_example")
    nlp_tools_port = os.getenv("NLP_TOOLS_PORT", "8001")

    response = requests.post(
        f"http://{nlp_tools_hostname}:{nlp_tools_port}/analyzeText/",
        json = data.dict()
    )
    interview_answers=response.json()
    # return the list of CreateInterviewAnswers
    print(interview_answers)
    createInterview = schemas.CreateInterview(first_name=interview_object.first_name,
                                                          last_name=interview_object.last_name,
                                                          address=interview_object.address,
                                                          interview_answers=interview_answers)
    print(createInterview)
    interview_id = interview_object.id

    backend_hostname = os.getenv("BACKEND_HOSTNAME", "backend")
    backend_port = os.getenv("BACKEND_PORT", "8000")

    # Will be a post request to the backend to save the transcription in the db
    response = requests.post(
        f"http://{backend_hostname}:{backend_port}/interviews/{interview_id}/data",
        json = createInterview.dict()
    )


# route : http://0.0.0.0:8003/sendTranscription
# Expected post body json:
# {
#     "blob": {"id":1, "key":"short_test_audio", "file_type": "str","description": "str","case_id": 1},
#     "questions" : [{"id":1, "text": "Slide the box into that empty space.", "case_id":1}, {"id":2,"text":"She danced like a swan tall and graceful.", "case_id":1}],
#     "interview" : {"id": 12, "blob_id": 1,"is_processed": false,"first_name": "str","last_name": "str","address": "str","case_id": 3}
# }
@app.post('/sendTranscription')
async def send_transcription(body: schemas.TranscriberObj, background_tasks: BackgroundTasks):
    # get the request
    audio_filename= body.blob.key
    questions = body.questions
    interview = body.interview

    background_tasks.add_task(transcribe, audio_filename=audio_filename, questions=questions, interview_object=interview)
    return {"message": "Transcription has started."}


# to run the server, just run python server.py
if __name__ == '__main__':
    print("Starting the server...")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)