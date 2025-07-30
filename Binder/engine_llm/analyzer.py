import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Union

from .extractor import TextExtractor
from .utils.pdf import read_pdf_bytes, count_pages


@dataclass
class AnalysisResult:
    file: str
    text: str = ""
    error: str = ""


class PDFAnalyzer:
    def __init__(self, max_pages: int = 5):
        self.max_pages = max_pages
        self.extractor = TextExtractor()
        self.logger = logging.getLogger(self.__class__.__name__)

    def analyze(self, pdf_path: Path) -> AnalysisResult:
        name = pdf_path.name
        try:
            data = read_pdf_bytes(pdf_path)
            pages = count_pages(data)
            if pages > self.max_pages:
                raise ValueError(f"{name} tiene {pages} páginas (> {self.max_pages})")
            text = self.extractor.extract(data)
            return AnalysisResult(file=name, text=text)
        except Exception as e:
            self.logger.error("Error analizando %s: %s", name, e)
            return AnalysisResult(file=name, error=str(e))
