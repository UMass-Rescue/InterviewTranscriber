To run with docker, use the commands:
docker build -t nlp-tools:latest .
docker run -p 8000:8000 nlp-tools

Note that this model may take around 15 minutes to load. 

You can send requests to http://0.0.0.0:8000/analyzeText with the body:

{
     "full_text": "slide the box into that empty space the plant grew large and green in the window the beam dropped down on the workmen's head pink clouds floated with the breeze she danced like a swan tall and graceful the tube was blown and a tire flat and useless it is late in the morning on the old all cock let's all join as we sang the last chorus the last switch cannot be turned off the fight will end in just six minutes",
     "questions" : ["Slide the box into that empty space.", "She danced like a swan tall and graceful."]
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