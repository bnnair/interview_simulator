# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import tempfile
from loguru import logger

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
        MODEL_TYPE = "openai"
        # Call the LLM to enhance the resume
        config = ConfigManager.update_config()
        logger.debug(f"config : {config}")
        aiadapter = AIAdapter(config, MODEL_TYPE)
        logger.debug(f"adapter : {aiadapter}")

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
        
        logger.info("calling aiadapter invoke method")
        response = aiadapter.invoke(prompt.format(context=pages))
        response1 = parser.invoke(response)
        
        logger.debug(f"response-------------- : {response1}")   
                
        logger.info("completed Response")
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
        logger.debug(enhanced_resume)
        interview_manager = InterviewManager(enhanced_resume, MODEL_TYPE)
        question = interview_manager.generate_question()
        logger.debug(f"question : {question}")
        llmanswer = interview_manager.generate_answer(question)
        logger.debug(f"llmanswer : {llmanswer}")
        return InterviewResponse(
            question=question,
            answer=llmanswer
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting interview: {str(e)}"
        )

@app.get("/api/healthcheck")
async def health_check():
    """
    Service health check endpoint
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000))
    )