from pydantic import BaseModel, field_validator
from typing import List, Optional

class Experience(BaseModel):
    company: str
    position: str
    duration: str
    responsibilities: Optional[List[str]] = None
    ### included for deepseek model not for openai
    @field_validator('responsibilities', mode='before')
    def split_responsibilities(cls, v):
        if isinstance(v, str):
            # Split the string into a list of responsibilities
            return [resp.strip() for resp in v.split(". ") if resp.strip()]
        return v

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    duration: str

class Skill(BaseModel):
    name: str
    description : str

class Certification(BaseModel):
    name: str
    
class Resume(BaseModel):
    name: str
    contact_info: str
    summary: str
    experiences: List[Experience]
    education: List[Education]
    skills: List[Skill]
    certifications: Optional[List[Certification]] = None