import fitz  # PyMuPDF
from docx import Document
from app.utils.logger import logger

def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        raise

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    except Exception as e:
        logger.error(f"Docx extraction failed: {e}")
        raise

def process_document(file_path: str) -> str:
    try:
        if file_path.lower().endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            raise ValueError("Only PDF and DOCX supported")
        
        text = " ".join(text.split())[:50000]  # Support 500+ pages
        logger.info(f"Document processed: {file_path}, length: {len(text)}")
        return text
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise        