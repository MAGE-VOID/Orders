import io
from typing import List
from PyPDF2 import PdfReader
from pathlib import Path


def read_pdf_bytes(path: Path) -> bytes:
    return path.read_bytes()


def count_pages(pdf_bytes: bytes) -> int:
    return len(PdfReader(io.BytesIO(pdf_bytes)).pages)


def extract_selectable_text(pdf_bytes: bytes) -> List[str]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return [p.extract_text() or "" for p in reader.pages]
