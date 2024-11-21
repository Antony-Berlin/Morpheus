#helper function here
import PyPDF2
from pptx import Presentation
from dotenv import load_dotenv
from openai import OpenAI
import os, json, time


def init():
    load_dotenv()
    global client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    )
    print("generative AI client initialized ...")

def chat(system_message : str , prompt : str):
    completion = client.chat.completions.create(

        model="meta-llama/llama-3.2-3b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
            "role": "user",
            "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

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
    system_message = "you are expert in providing the list of topics given a paragraph.you're response is always comma seperated topics no other sentence is required. help the student by giving the topics from his notes"
    prompt = "give me the topics from the below student notes:\n" + text
    response = chat(system_message, prompt)
    
    return response.split(",")
