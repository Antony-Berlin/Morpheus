#helper function here
import PyPDF2
from pptx import Presentation
from dotenv import load_dotenv
import google.generativeai as genai
import os, json, time


def init():
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API"))
    print("geniai configured...")
    global model 
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("model loaded...")

def extract_text(file_name):
    print("extracting text from file...")
    file_extension = os.path.splitext(file_name)[1].lower()
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', 'Documents', file_name)
    
    if file_extension == '.ppt' or file_extension == '.pptx':
        prs = Presentation(file_path)
        text_runs = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_runs.append(shape.text)
                    text_runs.append("-"*10)
        text =  "\n".join(text_runs)
    
    elif file_extension == '.pdf':
        text_runs = []
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                text_runs.append(page.extractText())
                text_runs.append("-"*10)
        text = "\n".join(text_runs)
    
    else:
        raise ValueError("Unsupported file format. Please provide a PPT, PPTX, or PDF file.")

    return text


def get_topics(text):
    print("generating topics...")
    prompt = "return the list of Major topics sperated by comma in the below paragraph. just the list no any other sentence or context\n" + text
    response = model.generate_content(prompt)
    
    return response.text.split(",")
