import os
import io
from typing import List

from PyPDF2 import PdfReader

def read_pdf_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def count_pages(pdf_bytes: bytes) -> int:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return len(reader.pages)

def extract_selectable_text(pdf_bytes: bytes) -> List[str]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return [page.extract_text() or "" for page in reader.pages]

def list_pdfs(dir_path: str) -> List[str]:
    return sorted(
        os.path.join(dir_path, fname)
        for fname in os.listdir(dir_path)
        if fname.lower().endswith(".pdf")
    )
