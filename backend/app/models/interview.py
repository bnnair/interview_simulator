from pydantic import BaseModel
from typing import Optional
from typing import List


class InterviewQuestion(BaseModel):
    question: str
    category: str  # e.g., Technical, Behavioral, Cultural Fit

class InterviewAnswer(BaseModel):
    question: str
    answer: Optional[str] = None
    evaluation: Optional[str] = None  # LLM's evaluation of the answer

class InterviewSession(BaseModel):
    resume_id: str  # Reference to the resume being interviewed
    questions: List[InterviewQuestion]
    answers: List[InterviewAnswer]