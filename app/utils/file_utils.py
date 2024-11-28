import fitz  # PyMuPDF for PDF parsing
import docx
import io

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extracts text from a PDF file using PyMuPDF (fitz).
    """
    doc = fitz.open(stream=file_content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_word(file_content: bytes) -> str:
    """
    Extracts text from a Word document using python-docx.
    """
    doc = docx.Document(io.BytesIO(file_content))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
