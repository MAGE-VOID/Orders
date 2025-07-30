import os
from typing import Dict

from .extractor import TextExtractor
from .utils.pdf import read_pdf_bytes, count_pages

class PDFAnalyzer:
    """
    Lee un PDF, valida recuento de páginas y extrae su texto.
    Devuelve {'file': ..., 'text': ...} o {'file': ..., 'error': ...}.
    """

    def __init__(self, max_pages: int = 5):
        self.max_pages = max_pages
        self.extractor = TextExtractor()

    def analyze(self, file_path: str) -> Dict[str, str]:
        fname = os.path.basename(file_path)
        try:
            data  = read_pdf_bytes(file_path)
            pages = count_pages(data)
            if pages > self.max_pages:
                raise ValueError(f"{fname} tiene {pages} páginas (> {self.max_pages})")
            text = self.extractor.extract(data)
            return {"file": fname, "text": text}
        except Exception as e:
            return {"file": fname, "error": str(e)}
