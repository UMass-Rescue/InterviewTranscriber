from typing import List
from pydantic import BaseModel
from datetime import datetime

class Blob(BaseModel):
    id: int
    key: str
    file_type: str
    description: str
    case_id: int
    date_uploaded = datetime.now()

    class Config:
        orm_mode = True

class Question(BaseModel):
    id: int
    text: str
    case_id: int

    class Config:
        orm_mode = True

class CreateInterviewAnswerNER(BaseModel):
    label: str
    start_index: int
    end_index: int

class InterviewAnswerNER(BaseModel):
    id: int
    label: str
    start_index: int
    end_index: int
    interview_answer_id:  int

    class Config:
        orm_mode = True

#TODO: add field for actual question text from transcription
class CreateInterviewAnswer(BaseModel):
    question_id: int
    answer: str
    interview_answer_ners: List[CreateInterviewAnswerNER] = []

class InterviewAnswer(BaseModel):
    id: int
    answer: str
    question_id: int
    interview_id: int

    class Config:
        orm_mode = True

class CreateInterview(BaseModel):
    first_name: str
    last_name: str
    address: str
    interview_answers: List[CreateInterviewAnswer] = []

class Interview(BaseModel):
    id: int
    blob_id: int
    is_processed: int
    first_name: str
    last_name: str
    date_uploaded: datetime = datetime.now()
    address: str
    case_id: int

    class Config:
        orm_mode = True

class TranscriberObj(BaseModel):
    blob: Blob
    questions: List[Question]
    interview: Interview

class analyzerObj(BaseModel):
    full_text: str
    questions: List[Question]
