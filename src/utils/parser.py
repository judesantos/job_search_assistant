import os

import tempfile
import fitz  # PyMuPDF
from docx import Document

TMP_DIR = "/tmp"
PDF_EXT = ".pdf"
DOCX_EXT = ".docx"


def read_docx(file_path):
    """
    Read the content of a DOCX file and return it as text.
    Args:
        file_path (str): The path to the DOCX file.
    Returns:
        str: The text content of the DOCX file.
    """
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def read_pdf(file_path):
    """
    Read the content of a PDF file and return it as text.
    Args:
        file_path (str): The path to the PDF file.
    Returns:
        str: The text content of the PDF file.
    """
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def process_file(file) -> tuple[str | None, str | None]:
    """
    Process the uploaded file and extract text from it.
    Args:
        file (FileStorage): The uploaded file.
    Returns:
        str: The extracted text from the file.
    """
    error = None
    text = None
    try:
        file_extension = os.path.splitext(file.filename)[1].lower()
        with tempfile.NamedTemporaryFile(
            delete_on_close=True,
            dir=TMP_DIR,
            suffix=file_extension
        ) as temp_file:
            # Save to a temporary file
            file.save(temp_file.name)
            temp_file_path = temp_file.name
            # Extract text based on file type: docx, pdf
            if file_extension == DOCX_EXT:
                return read_docx(temp_file_path), None
            elif file_extension == PDF_EXT:
                return read_pdf(temp_file_path), None

    except Exception as e:
        print(f"Error processing file: {e}")
        return None, "Error processing file"

    return error, text
