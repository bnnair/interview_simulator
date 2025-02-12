from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from models.resume import Resume
from utils.pdf_parser import load_pdf

llm = ChatOpenAI()

parser = JsonOutputParser(pydantic_object=Resume)


prompt = PromptTemplate(
    template="Extract the information as specified.\n{format_instructions}\n{context}\n",
    input_variables=["context"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

if __name__=="__main__":
    
    pages = load_pdf("D:\workspaces\workspace-5\interview-simulator copy\data\BijuNair-resume.pdf")

    chain = prompt | llm | parser

    response = chain.invoke({
        "context": pages
    })
    print(response)
    Resume(**response)
    print(Resume)