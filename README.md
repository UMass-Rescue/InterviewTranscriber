# InterviewTranscriber

This tool will achieve the following tasks: transcribe an audio file to text, create sentence segments from the transcription,
identify the interview questions and corresponding answers, and identify key elements of the answers. 

There are two microservices contained in this repo.  The first is transcriber which takes an audio files and returns the 
text for that audio file.  Note that this text will not include capitalization or punctuation.
The second service is nlp-tools.  This service will take in the name of the audio files and list of questions in that 
text and return a list of question/answer pairs along with NER objects for each answer.

Each service can be run with docker or locally.  See the corresponding READMEs for more details. 