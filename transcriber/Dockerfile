FROM python:3.9

WORKDIR /usr/src/app

ENV MODEL_VERSION 0.22
RUN mkdir /opt/vosk-model-en \
   && cd /opt/vosk-model-en \
   && wget -q http://alphacephei.com/kaldi/models/vosk-model-en-us-${MODEL_VERSION}.zip \
   && unzip vosk-model-en-us-${MODEL_VERSION}.zip \
   && mv vosk-model-en-us-${MODEL_VERSION} model \
   && rm -rf vosk-model-en-us-${MODEL_VERSION}.zip

RUN apt-get -y update
RUN apt-get --yes install libsndfile1

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .

CMD ["python", "server.py"]