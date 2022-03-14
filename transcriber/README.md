This repo is currently trancsriber audio file stored locally in a folder /audio. 
There are a number of good wav files you can place in this folder for testing located here:
https://www.uclass.psychol.ucl.ac.uk/Release2/Conversation/AudioOnly/wav/
. Update line 25 in server.py with the name of the file to see the transcription. 

This app currently supports only wav audio files. 

To run with docker, use the commands:
docker build -t transcriber:latest .
docker run -p 8000:8000 transcriber

You can send requests to http://0.0.0.0:8000/sendTranscription with the body:

{
"audio_filename": "File1"
}

To run the server locally:
- Create venv using 'python3 -m venv venv' from the root directory.
- Activate virtual environment:
    - For Mac/Linux: 'source venv/bin/activate'
    - For Windows: 'venv\Scripts\activate.bat'
- Install dependencies using 'pip install -r requirements.txt'.
- Start server by running 'python3 server.py' from the root directory.