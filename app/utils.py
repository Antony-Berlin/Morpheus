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
    response = chat(system_message=system_message,prompt=prompt)
    
    return response.split(",")



def get_questions_and_answers(topic, text, about_proff, proff_sample_question, no_of_questions):
  
    request_count = 0
    max_requests_per_minute = 15
    start_time = time.time()
    qa = []

    
    if request_count >= max_requests_per_minute:
        elapsed_time = time.time() - start_time
        remaining_time = 65 - elapsed_time
        if remaining_time > 0:
            print(f"Rate limit reached. Waiting for {remaining_time:.2f} seconds...")
            time.sleep(remaining_time)
        start_time = time.time()  # Reset the start time after waiting
        request_count = 0  # Reset the request count after waiting


    System_message = "you are expert in mimicing the professor in generating question, options and its answer.Provide the JSON response directly without wrapping it in backticks or marking it as a code block. "

    prompt = (
        
        "as a professor return the list of mcq questions with options and answers as dictionary object, the response must only have the array, shouldn't have any context or extra sentence. \n"+
        "example: [{'question': 'what is the capital of india?', 'options': ['delhi', 'mumbai', 'kolkata', 'chennai'], 'answer': 'delhi'}, {'question': 'what is the capital of usa?', 'options': ['new york', 'washington dc', 'los angeles', 'chicago'], 'answer': 'washington dc'}]"+
        "passage: " + text + "\n" +
        "topics: " + topic + "\n" +
        "about professor: " + about_proff + "\n" +
        "professor sample question: " + proff_sample_question + "\n" +
        "no of questions: " + str(no_of_questions) + "\n" 
    )
    response = chat(system_message=System_message, prompt=prompt)
    
    try:
        response_data = json.loads(response)
        qa.extend(response_data)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")
        print(f"Response text: {response}")
        return {"error": "Failed to decode JSON response"}, 400
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Response text: {response}")
        return {"error": "An error occurred"}, 400

    return qa, 200

def handle_file_upload(file):
    if file.filename == '':
        return {"error": "No selected file"}, 400
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(os.getcwd(), "Documents", filename)
        
        if os.path.exists(file_path):
            return {"error": "File already exists"}, 409
        
        file.save(file_path)
        print("Document uploaded successfully")
        return {"message": "File uploaded successfully", "file_path": file_path}, 201
    else:
        return {"error": "File type not allowed"}, 415

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS