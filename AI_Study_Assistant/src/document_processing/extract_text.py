from pathlib import Path
from pypdf import PdfReader
from docx import Document

def extract_text(file):
    extension = Path(file.name).suffix.lower()

    if extension == '.txt':
        text = file.read().decode("utf-8-sig")

    elif extension == '.pdf':
        reader = PdfReader(file)
        text = "\n".join(
            page.extractText() or ""
            for page in reader.pages
        )

    elif extension == '.docx':
        document = Document(file)
        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    else:
        raise ValueError("Unsupported file type")

    text = text.strip()

    if not text:
        raise ValueError("Bo text could be extracted from the file.")

    return text