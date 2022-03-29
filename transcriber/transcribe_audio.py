import json
import os
from vosk import Model, KaldiRecognizer
import wave
from azure.storage.blob import BlobClient

class Transcriber:

    blob_account_url = os.getenv("BLOB_ACCOUNT_URL")
    blob_credential = os.getenv("BLOB_CREDENTIAL")
    blob_container = os.getenv("BLOB_CONTAINER")

    def __init__(self, model_path):
        """
        Parameters:
          language : the language for the sentence segmenter
          model : model for the sentence transformer
        """
        self.model = Model(model_path)

    #get the blob wav file and save it locally
    def read_blob(self, blob_key: str):
        blob = BlobClient(
            account_url=self.blob_account_url,
            container_name=self.blob_container,
            blob_name=blob_key,
            credential=self.blob_credential,
        )
        file_name = blob_key+'.wav'
        with open(file_name, "wb") as my_blob:
            download_stream = blob.download_blob()
            my_blob.write(download_stream.readall())
        return file_name

    def transcribe(self, audio_filename):

        audio_file = self.read_blob(audio_filename)

        wf = wave.open(audio_file, "rb")

        rec = KaldiRecognizer(self.model, wf.getframerate())
        rec.SetWords(True)

        # get the list of JSON dictionaries
        results = []
        # recognize speech using vosk model
        while True:
            data = wf.readframes(500)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                part_result = json.loads(rec.Result())
                results.append(part_result)
        part_result = json.loads(rec.FinalResult())
        results.append(part_result)

        # convert list of JSON dictionaries to string
        text = ''
        for sentence in results:
            text = text + sentence["text"] + ' '

        wf.close()  # close audiofile

        #delete local wav file created for this function
        if os.path.exists(audio_file):
            os.remove(audio_file)

        return text
