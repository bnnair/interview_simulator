from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader
from loguru import logger

def parse_pdf(file):
    logger.debug("inside parse_pdf")
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text


def load_pdf(file):
    logger.debug("inside load_pdf")
    logger.debug(file)
    loader = PyPDFLoader(file)
    pages = loader.load()
    
    return pages 
