FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV MODEL_VERSION 0.22
RUN mkdir /opt/vosk-model-en \
   && cd /opt/vosk-model-en \
   && wget -q http://alphacephei.com/kaldi/models/vosk-model-en-us-${MODEL_VERSION}.zip \
   && unzip vosk-model-en-us-${MODEL_VERSION}.zip \
   && mv vosk-model-en-us-${MODEL_VERSION} model \
   && rm -rf vosk-model-en-us-${MODEL_VERSION}.zip

#this is needed if we need to convert mps to wav
#FROM katalonstudio/katalon
#RUN apt-get install -y ffmpeg

WORKDIR /usr/src/app

COPY . .

CMD ["python", "server.py"]