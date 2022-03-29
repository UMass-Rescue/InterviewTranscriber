FROM python:3.9

WORKDIR /usr/src/app

#download the spacy model so it is cached for faster builds in the future
COPY ./requirements/spacy.txt ./requirements/spacy.txt

RUN pip install -r requirements/spacy.txt
RUN python -m spacy download en_core_web_lg

COPY ./requirements/base.txt ./requirements/base.txt

RUN pip install -r requirements/base.txt

#not sure why this was not working so added download_model method in nlp_tools to get the model
#RUN mkdir /root/.punctuator && cd /root/.punctuator && wget https://drive.google.com/uc?id=0B7BsN5f2F1fZd1Q0aXlrUDhDbnM&confirm=t

WORKDIR /usr/src/app

COPY . .

CMD ["python", "server.py"]