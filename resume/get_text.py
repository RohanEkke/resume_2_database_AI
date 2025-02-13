import os
from .pdf_to_text import pdf_to_text
from .docx_to_text import docx_to_text

def check_file_type(file_path):
    if not os.path.isfile(file_path):
        print("The provided path does not point to a valid file.")
        return
    
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    
    if extension == ".pdf":
        text = pdf_to_text(file_path)
        return text or "No text extracted from the PDF."
    elif extension == ".docx":
        text = docx_to_text(file_path)
        return text or "No text extracted from the DOCX file."
    else:
        print("The file is neither a PDF nor a DOCX document.")





  