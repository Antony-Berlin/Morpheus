#helper function here
import PyPDF2
from pptx import Presentation
import os

def extract_text(file):
    file_extension = os.path.splitext(file)[1].lower()
    
    if file_extension == '.ppt' or file_extension == '.pptx':
        prs = Presentation(file)
        text_runs = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_runs.append(shape.text)
                    text_runs.append("-"*10)
        return "\n".join(text_runs)
    
    elif file_extension == '.pdf':
        text_runs = []
        with open(file, 'rb') as pdf_file:
            reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                text_runs.append(page.extract_text())
                text_runs.append("-"*10)
        return "\n".join(text_runs)
    
    else:
        raise ValueError("Unsupported file format. Please provide a PPT, PPTX, or PDF file.")
