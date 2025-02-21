from pydantic import BaseModel
from typing import Optional
from models.resume import Resume

class ResumeEnhancementResponse(BaseModel):
    original_resume: str
    enhanced_resume: str

class InterviewResponse(BaseModel):
    question: str
    answer: Optional[str] = None
    evaluation: Optional[str] = None
    
    
    
class InterviewRequest(BaseModel):
    resume: Resume
    user_question: Optional[str] = None