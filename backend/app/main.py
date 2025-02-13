# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import os
from dotenv import load_dotenv
import openai
import json
import tempfile

# Import services
from services.resume_enhancer import enhance_resume
from services.interview_simulator import InterviewManager
from utils.pdf_parser import parse_pdf, load_pdf

# Import models
from models.interview import InterviewQuestion, InterviewAnswer
from models.responses import InterviewResponse
from models.errors import HTTPError
from models.resume import Resume, Experience, Education, Skill

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain  

from utils.config_manager import ConfigManager
from services.llm_manager import AIAdapter

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Resume Enhancer & Interview Simulator",
    description="API for resume enhancement and AI-powered interview simulations",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], ## for production, this should be limited to specific domains
    allow_methods=["*"], ## for production, this should be limited to specific methods
    allow_headers=["*"], ## for production, this should be limited to specific headers
)

# Custom exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.post(
    "/api/upload-resume",
    response_model=Resume, #ResumeEnhancementResponse,
    responses={
        400: {"model": HTTPError, "description": "Invalid file format"},
        500: {"model": HTTPError, "description": "Resume processing error"}
    }
)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a PDF resume and get back an enhanced version
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    try:
        # Parse PDF
        # resume_text = parse_pdf(file.file)
        # print(resume_text)
        MODEL_TYPE = "openai"
        # Call the LLM to enhance the resume
        config = ConfigManager.update_config()
        print(f"config : {config}")
        aiadapter = AIAdapter(config, MODEL_TYPE)
        print(f"adapter : {aiadapter}")

        # llm = ChatOpenAI()

        parser = JsonOutputParser(pydantic_object=Resume)

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        pages = load_pdf(temp_file_path)
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        prompt = PromptTemplate(
        template="Extract the information as specified.  \
            do not extract any other information other than the specified\n{format_instructions}\n{context}\n",
        input_variables=["context"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        
        print("calling aiadapter invoke method")
        response = aiadapter.invoke(prompt.format(context=pages))
        response1 = parser.invoke(response)
        
        print(f"response-------------- : {response1}")   
                
        # Enhance resume
        # enhanced_resume = enhance_resume(resume_text)
        # print(enhanced_resume)
        
        # return ResumeEnhancementResponse(
        #     original_resume=resume_text,
        #     enhanced_resume=enhanced_resume
        # )
        print("completed Response")
        return Resume(**response1)        
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing resume: {str(e)}"
        )

@app.post(
    "/api/start-interview",
    response_model=InterviewResponse,
    responses={
        400: {"model": HTTPError, "description": "Invalid resume format"},
        500: {"model": HTTPError, "description": "Interview generation error"}
    }
)
async def start_interview(enhanced_resume: Resume):
    """
    Start a new interview session based on the provided resume
    """
    print("Received Resume:", enhanced_resume.model_dump_json())
    print("inside start interview")
    try:
        MODEL_TYPE = "deepseek"
        # # Parse the enhanced resume into a structured Resume object
        # resume = parse_enhanced_resume(enhanced_resume)
        print(enhanced_resume)
        interview_manager = InterviewManager(enhanced_resume, MODEL_TYPE)
        question = interview_manager.generate_question()
        llmanswer = interview_manager.generate_answer(question)
        return InterviewResponse(
            question=question,
            answer=llmanswer
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting interview: {str(e)}"
        )

# @app.post(
#     "/api/submit-answer",
#     response_model=InterviewResponse,
#     responses={
#         400: {"model": HTTPError, "description": "Missing required fields"},
#         500: {"model": HTTPError, "description": "Answer processing error"}
#     }
# )
# async def submit_answer(
#     enhanced_resume: Resume
#     # question: str,
#     # answer: str
# ):
#     """
#     Submit an answer to the current interview question and get evaluation
#     """
#     print("inside the submit answer")

#     if not enhanced_resume:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Resume is required"
#         )

#     try:
#         # # Parse the enhanced resume into a structured Resume object
#         # resume = parse_enhanced_resume(enhanced_resume)
#         print("enhanced_resume", enhanced_resume)
#         interview_manager = InterviewManager(enhanced_resume)
#         # evaluation = interview_manager.generate_answer(question)
        
#         # Generate next question
#         next_question = interview_manager.generate_question()
        
#         return InterviewResponse(
#             question=next_question
#             # evaluation=evaluation
#         )
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error processing answer: {str(e)}"
#         )

@app.get("/api/healthcheck")
async def health_check():
    """
    Service health check endpoint
    """
    return {"status": "healthy"}


# # Helper function to parse enhanced resume into a Resume object
# def parse_enhanced_resume(enhanced_resume: str) -> Resume:
#     """
#     Parse the enhanced resume text into a structured Resume object.
#     This function uses an LLM to extract structured data from the text.
#     """
#     prompt = f"""
#     Extract the following details from the resume text below and return them as a JSON object:
#     - name: Full name of the individual
#     - contact_info: Contact information (email, phone, etc.)
#     - summary: Professional summary
#     - experiences: List of work experiences (company, position, duration, responsibilities)
#     - education: List of educational qualifications (institution, degree, field_of_study, duration)
#     - skills: List of skills (name, proficiency)
#     - certifications: List of certifications (optional)

#     Resume Text:
#     {enhanced_resume}
#     """

#     # Call the LLM to extract structured data
#     response = openai.chat.completions.create(
#         model="gpt-4o",
#         messages=[{"role": "user", "content": prompt}],
#         response_format={"type": "json_object"}
#     )

#     # Parse the JSON response into a Resume object
#     resume_data = json.loads(response.choices[0].message.content)
#     return Resume(**resume_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000))
    )