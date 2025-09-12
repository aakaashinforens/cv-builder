import docx2txt
from PyPDF2 import PdfReader

#just extracting text from pdf or docx. Give the text directly to perplexity instead of having to extract sections.

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)


def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Please provide PDF or DOCX.")
