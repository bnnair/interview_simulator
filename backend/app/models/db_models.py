from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass

# Database setup
DATABASE_URL = "sqlite:///interview.db"  # Use SQLite for simplicity
engine = create_engine(DATABASE_URL,pool_timeout=10.0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

class ResumeDB(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    resume_data = Column(JSON)  # Stores the entire resume as JSON

# Define the InterviewSession model
class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, index=True)  # Reference to the resume
    question = Column(JSON)
    answer = Column(JSON)

# Create the database tables
Base.metadata.create_all(bind=engine)


if __name__=="__main__":
    print("Database tables created successfully")