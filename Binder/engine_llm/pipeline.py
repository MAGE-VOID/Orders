import json
import logging
from pathlib import Path
from dataclasses import asdict

from .analyzer import PDFAnalyzer, AnalysisResult
from .classifier import DocumentClassifier, ClassificationResult


class JsonPrinter:
    @staticmethod
    def print(obj):
        print(json.dumps(asdict(obj), ensure_ascii=False))


class DocumentPipeline:
    def __init__(
        self,
        input_dir: Path,
        analyzer_max_pages: int,
        classifier_instructions: str,
        classifier_api_key: str,
        classifier_model: str,
    ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.input_dir = Path(input_dir)
        self.analyzer = PDFAnalyzer(max_pages=analyzer_max_pages)
        self.classifier = DocumentClassifier(
            instructions=classifier_instructions,
            api_key=classifier_api_key,
            model=classifier_model,
        )

    def run(self):
        if not self.input_dir.is_dir():
            raise FileNotFoundError(f"No existe: {self.input_dir}")
        pdfs = sorted(self.input_dir.glob("*.pdf"))
        if not pdfs:
            raise FileNotFoundError(f"Ningún PDF en: {self.input_dir}")

        for pdf in pdfs:
            self.logger.info("Procesando %s", pdf.name)
            analysis: AnalysisResult = self.analyzer.analyze(pdf)
            classification: ClassificationResult = self.classifier.classify(analysis)
            JsonPrinter.print(classification)
