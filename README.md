# InterviewTranscriber
##Description
This tool will achieve the following tasks: transcribe an audio file to text, create sentence segments from the transcription,
identify the interview questions and corresponding answers, and identify key elements of the answers.

There are two microservices contained in this repo.  The first is transcriber which takes an audio files key 
and transcribes the file to text with punctuation or capitalization. The services then passes the text and questions to
the nlp-tools service in order to analyze the text. The analysis will include return a list of question/answer pairs 
along with NER objects for each answer. It can then return this analysis as a json to a backend server. 

## Quick Start
These services can be run concurrently using the docker-compose file in the root folder. 
You will need a .env file to store the credentials for these services. Please message Colette Basiliere for this file.
The services can be run using the following commands in the root directory with the .env file:

```
docker compose build
docker compose up
```

For full details, please see the manual. The audio file will already need to exist as a Blob in Azure. 

You can send requests to http://0.0.0.0:8002/sendTranscription with the body:

{
"audio_filename": "short_test_audio"
"questions" : ["Slide the box into that empty space.", "She danced like a swan tall and graceful."]
}

This will display the results in the console but show an error when trying to write to the database. See the full manual 
for instructions to set up the database. 

Each service can be run with docker locally to debug.  See the corresponding READMEs for more details. 