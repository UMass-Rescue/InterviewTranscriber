# Interview Transcriber

## Motivation

Human transcription of audio files takes time and uses resources that could be allocated to other tasks.
By automating the process of transcribing audio files, resources will be free to do more analytical tasks to 
help quickly solve cases.  Additionally, the data structure which stores the transcription will be easy to navigate and 
provide analytics like when times and places are seen in the interview.  This will make it easier for those working on 
the case to see patterns and search for text.


## Features

This tool will achieve the following tasks: transcribe an audio file to text, create sentence segments from the transcription,
identify the interview questions and corresponding answers, and identify key elements of the answers.

There are two microservices contained in this repo.  The first is transcriber which retrieves an audio file from Azure 
and transcribes it to text without punctuation or capitalization. 
The transcriber then passes this text along with a list of questions to the analysis service in order to analyze the text.  
The analysis service (nlp-tools) first adds capitalization and punctuation to the text before finding each of the questions within the 
text.  Once the questions are found, the corresponding answers are identified along with any named entities like 
times or places within the answer. 
The service then returns this analysis as a json to the backend server to save it to the database.


## Tech Stack
This service is run with FastAPI and utilizes a back end built for the UMass Rescue Lab.
Azure is used for file storage. Additional packages are used to complete tasks in each service.

Transcription:
* vosk Kaldi Recognizer

Analysis:
* Spacy
* Punctuator
* NNSplit
* Sentence Transformer

## Improvements

In the future, the program could be improved in the following ways:
* Train custom punctuator model on data from transcribed interviews for better accuracy
* Find faster model for audio transcription
* Include summaries of text along with the interview data
* Include functionality for multiple languages 
    * Most tools have models in multiple languages but metadata about the language will need to be integrated


## How to use

Begin by cloning the repo locally. After cloning the repo, you will need to create a .env file in the root directory 
and include the following fields:
```
BLOB_ACCOUNT_URL=""
BLOB_ACCOUNT_CREDENTIAL=""
BLOB_CONTAINER=""
NLP_TOOLS_HOSTNAME="nlp_tools"
NLP_TOOLS_PORT="8001"
BACKEND_HOSTNAME="backend"
BACKEND_PORT="8000"
# PostgreSQL Container Secrets
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```
Please note that you will need to specify the first three and last three fields.

Next, you will need to upload the audio file you would like to transcribe to your Azure container.  You must know the 
blob key of the audio file for use later.
Note that at this time, the service only works with .wav files.

The services can be run concurrently using the docker-compose file in the root folder.
The services can be run using the following commands in the root directory with the .env file:

```
docker compose build
docker compose up
```

This service replies on a backend created for the UMass Rescue Lab. The latest image of this package will be pulled
using docker-compose. We now need to set up the database manually before running the Interview Transcriber.
Instructions for the setting up the database can be found at:
https://luxuriant-save-c5e.notion.site/Setting-Up-Backend-Docker-Container-dd2ce1e805e84b44a245991c96d46591.

Note that if you want the service to write results to the database, metadata will need to be added to the database 
before the transcription begins. These objects include:

* Blob
* Question

Further information about object structure can be found here:
https://github.com/UMass-Rescue/596-S22-Backend/blob/main/app/models.py. The Blob object will contain data for the 
.wav file to be transcribed. You can add as many questions to look for in the interview as you need one at a time. 
If you do not include these object, you will be able to see the results in the console.

Requests can then be made to the server using any API interface you prefer, we recommend Postman. 


At this time, you can send requests to the backend to add objects to the database if you choose. To create a Blob,
use http://0.0.0.0:8002/{case}/blob with the body:
```
{
"key": {str},
"file_type": {str},
"description": {str},
}
```
To create a Questions, use http://0.0.0.0:8002/{case}/blob with the body:
```
{
"text": {str}
}
```
We can now use the transcriber. 

If you did not include the additional objects in the back end, you can send requests 
to http://0.0.0.0:8002/sendTranscription with the body:
```
{
"audio_filename": "short_test_audio",
"questions" : ["Slide the box into that empty space.", "She danced like a swan tall and graceful."]
}
```
These requests will not write data to the database but will print the results in the console.

If you did include additional objects in the backend, you can send the request to
http://0.0.0.0:8002/{case}/create_interview_shell_for with the body:
```
{
"first_name": {str},
"last_name": {str},
"address": {str},
"blob_id": {int}
}
```
Note that you will need to fill in the fields with the appropriate data, including the id of the Blob object 
you created earlier.

The transcription service may take several minutes to run but when it completes you will be able to use
http://0.0.0.0:8002/interviews/{interview_id}/answers to get the results. 

Each service can be run with docker locally to debug.  See the corresponding READMEs for more details. 
