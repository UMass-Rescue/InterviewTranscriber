import json
from flask import Flask, request
from flask_cors import CORS
from transcribe_audio import Transcriber

app = Flask(__name__)
CORS(app)

@app.route('/sendTranscription', methods=['POST'])
def return_route():
    # get the request
    request_str = request.data.decode('utf-8')

# route : http://127.0.0.1:5000/sendTranscription
# Expected post json:
# {
#     "audio_filename": "File1"
# }

    request_json = json.loads(request_str)
    audio_filename = request_json['audio_filename'] #use "audio/Casual_English_Conversation.mp3"

    model_path = "/opt/vosk-model-en/model"
    #model_path = '/Users/colettebasiliere/Desktop/vosk-model-en-us-0.22' # for local testing
    audio_filename = "audio/M_0399_12y4m_1.wav"  #can comment out this line when testing complete

    transcriber = Transcriber(model_path)
    text = transcriber.transcribe(audio_filename)

    # return the points
    to_return = {"transcription": text}
    print(to_return)
    return json.dumps(to_return)

# to run the server, just run python server.py
if __name__ == '__main__':
    print("Starting the server...")
    app.run(host='0.0.0.0', debug=True,port='8000')