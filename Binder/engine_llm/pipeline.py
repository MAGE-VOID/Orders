import json
import logging
from pathlib import Path
from dataclasses import asdict

from .config import Config
from .analyzer import PDFAnalyzer, AnalysisResult
from .classifier import DocumentClassifier, ClassificationResult


class JsonPrinter:
    @staticmethod
    def print(obj):
        # Convierte cualquier dataclass a dict y lo serializa a JSON
        print(json.dumps(asdict(obj), ensure_ascii=False))


class DocumentPipeline:
    """
    Orquesta el flujo completo tomando toda la configuración de un único objeto Config.
    """

    def __init__(self, config: Config):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.input_dir = Path(config.input_dir)
        self.analyzer = PDFAnalyzer(max_pages=config.max_pages)
        # Pasamos explícitamente config.model, que viene de Config.DEFAULT_LLM_MODEL
        self.classifier = DocumentClassifier(
            instructions=config.instructions, api_key=config.api_key, model=config.model
        )

    def run(self):
        if not self.input_dir.is_dir():
            raise FileNotFoundError(f"No existe el directorio: {self.input_dir}")

        pdfs = sorted(self.input_dir.glob("*.pdf"))
        if not pdfs:
            raise FileNotFoundError(f"No se encontraron PDFs en: {self.input_dir}")

        for pdf in pdfs:
            self.logger.info("Procesando %s", pdf.name)
            analysis: AnalysisResult = self.analyzer.analyze(pdf)
            classification: ClassificationResult = self.classifier.classify(analysis)
            JsonPrinter.print(classification)
