from pydantic import BaseModel
from typing import Optional

class ResumeEnhancementResponse(BaseModel):
    original_resume: str
    enhanced_resume: str

class InterviewResponse(BaseModel):
    question: str
    answer: Optional[str] = None
    evaluation: Optional[str] = None