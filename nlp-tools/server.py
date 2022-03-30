import json
from typing import List

from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nlp_tools import NLP_Tools
import schemas

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# route : http://127.0.0.1:5000/analyzeText
# Expected post json:
# {
#     "full_text": "slide the box into that empty space the plant grew large and green in the window the beam dropped down on the workmen's head pink clouds floated with the breeze she danced like a swan tall and graceful the tube was blown and a tire flat and useless it is late in the morning on the old all cock let's all join as we sang the last chorus the last switch cannot be turned off the fight will end in just six minutes",
#     "questions" : ["Slide the box into that empty space.", "She danced like a swan tall and graceful."]
# }
@app.post('/analyzeText')
async def analyze_text(analyzer_data: schemas.analyzerObj):
    # get the request
    text = analyzer_data.full_text
    interview_questions = analyzer_data.questions

    #download the models
    punct_model = 'Demo-Europarl-EN.pcl'
    sentence_model = 'all-MiniLM-L6-v2'
    nlp_tool = NLP_Tools(punct_model, sentence_model)

    q_and_a = nlp_tool.get_questions_and_answers(text, interview_questions)
    print(q_and_a)
    # return the question and answer pairs
    return q_and_a

# to run the server, just run python server.py
if __name__ == '__main__':
    print("Starting the server...")
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)