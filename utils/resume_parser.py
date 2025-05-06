import os
from PyPDF2 import PdfReader
import docx

def extract_text_from_resume(file):
    try:
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            return extract_text_from_pdf(file)
        elif filename.endswith(".docx"):
            return extract_text_from_docx(file)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return ""

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    text = ""
    doc = docx.Document(file)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
