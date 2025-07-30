import os
import json
from typing import Dict

from .analyzer import PDFAnalyzer
from .classifier import SingleFileClassifier
from .utils.pdf import list_pdfs

class DocumentPipeline:
    """
    Orquesta el procesamiento de cada PDF en un directorio:
      1) PDFAnalyzer -> extrae texto
      2) SingleFileClassifier -> clasifica con LLM
      3) Imprime el JSON de cada archivo inmediatamente
    """

    def __init__(self, instructions: str, api_key: str, max_pages: int = 5, model: str = "gpt-3.5-turbo"):
        self.analyzer   = PDFAnalyzer(max_pages=max_pages)
        self.classifier = SingleFileClassifier(instructions=instructions, api_key=api_key, model=model)

    def run(self, input_dir: str) -> None:
        if not os.path.isdir(input_dir):
            raise FileNotFoundError(f"No existe el directorio de entrada: {input_dir}")

        pdf_files = list_pdfs(input_dir)
        if not pdf_files:
            raise FileNotFoundError(f"No se encontraron PDFs en: {input_dir}")

        for path in pdf_files:
            result = self._process_one(path)
            print(json.dumps(result, ensure_ascii=False))

    def _process_one(self, path: str) -> Dict:
        analysis       = self.analyzer.analyze(path)
        classification = self.classifier.classify(analysis)
        return classification
