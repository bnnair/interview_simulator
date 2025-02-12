from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ResumeDB(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    resume_data = Column(JSON)  # Stores the entire resume as JSON

class InterviewDB(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, index=True)
    questions = Column(JSON)  # Stores list of questions
    answers = Column(JSON)    # Stores list of answers