To run with docker, use the commands:
docker build -t nlp-tools:latest .
docker run -p 8000:8000 nlp-tools

Note that this model may take around 15 minutes to load. 

You can send requests to http://0.0.0.0:8000/analyzeText with the body:

{
"audio_filename": "File1",
"questions" : ["Question1", "Question 2"]
}

When after sending the first request to the server you may get an error:

Detected change in '/root/.theano/compiledir_Linux-5.10-linuxkit-x86_64-with-glibc2.31--3.9.10-64/cutils_ext/__init__.py', reloading

Simply resend the request and the program should function as expected

To run the server locally:
- Create venv using 'python3 -m venv venv' from the root directory.
- Activate virtual environment:
    - For Mac/Linux: 'source venv/bin/activate'
    - For Windows: 'venv\Scripts\activate.bat'
- Install dependencies using 'pip install -r requirements.txt'.
- Start server by running 'python3 server.py' from the root directory.