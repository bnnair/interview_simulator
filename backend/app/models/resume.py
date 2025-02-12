from pydantic import BaseModel, Field
from typing import List, Optional

class Experience(BaseModel):
    company: str
    position: str
    duration: str
    responsibilities: Optional[List[str]] = None

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