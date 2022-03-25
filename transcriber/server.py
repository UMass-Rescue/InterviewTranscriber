import json
from flask import Flask, request
from flask_cors import CORS
from transcribe_audio import Transcriber

app = Flask(__name__)
CORS(app)

# route : http://127.0.0.1:5000/sendTranscription
# Expected post json:
# {
#     "audio_filename": "short_test_audio"
# }
@app.route('/sendTranscription', methods=['POST'])
def return_route():
    # get the request
    request_str = request.data.decode('utf-8')

    request_json = json.loads(request_str)
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
    app.run(host='0.0.0.0', debug=True,port='8000')