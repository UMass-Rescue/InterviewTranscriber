This repo transcribes audio files located in the 596e-backend Azure. It then calls nlp-tools to 
analyze the text and returns the analyzed text in the form of a json.

There are a number of good wav files you can place in this folder for testing located here:
https://www.uclass.psychol.ucl.ac.uk/Release2/Conversation/AudioOnly/wav/
.

This app currently supports only wav audio files. 

This file relies on the nlp-tools server so use the program you must
use the docker-compose file in the root directory of this project.

Note that this model may take around 10 minutes to load.

To run with docker for debugging purposes, use the commands:
docker build -t transcriber:latest .
docker run -p 8000:8000 transcriber

To debug this repo, comment out line 27 in server.py to prevent the call to nlp-tools. 
You can send requests to http://0.0.0.0:8000/sendTranscription with the body:

{
    "audio_filename": "short_test_audio"
    "questions" : ["Slide the box into that empty space.", "She danced like a swan tall and graceful."]
}