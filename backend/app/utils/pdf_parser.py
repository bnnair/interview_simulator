from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFLoader


def parse_pdf(file):
    print("inside parse_pdf")
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text


def load_pdf(file):
    print("inside load_pdf")
    print(file)
    loader = PyPDFLoader(file)
    pages = loader.load()
    
    return pages 



    
    # print(parse_pdf("D:\workspaces\workspace-5\interview-simulator copy\data\BijuNair-resume.pdf"))