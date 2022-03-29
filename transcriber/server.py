import json
from fastapi import Request, FastAPI
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

# route : http://127.0.0.1:5000/sendTranscription
# Expected post json:
# {
#     "audio_filename": "short_test_audio"
# }
@app.post('/sendTranscription')
async def return_route(request: Request):
    # get the request
    request_json = await request.json()
    audio_filename = request_json['audio_filename']

    model_path = "/opt/vosk-model-en/model"

    transcriber = Transcriber(model_path)
    text = transcriber.transcribe(audio_filename)

    # return the transcription
    to_return = {"transcription": text}
    print(to_return)
    return json.dumps(to_return)

# to run the server, just run python server.py
if __name__ == '__main__':
    print("Starting the server...")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)