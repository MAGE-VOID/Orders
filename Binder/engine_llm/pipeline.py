# engine_llm/pipeline.py

import json
from pathlib import Path
from dataclasses import asdict
from typing import Dict, Any

from .config import Config
from .analyzer import PDFAnalyzer, AnalysisResult
from .classifier import DocumentClassifier, ClassificationResult


class JsonPrinter:
    @staticmethod
    def print(obj: Dict[str, Any], pretty: bool = False):
        """
        Recibe un dict ya preparado (con el contador incluido) y lo imprime como JSON.
        """
        if pretty:
            text = json.dumps(obj, ensure_ascii=False, indent=2)
        else:
            text = json.dumps(obj, ensure_ascii=False)
        print(text)


class DocumentPipeline:
    """
    Orquesta el flujo completo tomando toda la configuración de un único objeto Config.
    """

    def __init__(self, config: Config):
        self.input_dir = Path(config.input_dir)
        self.analyzer = PDFAnalyzer(max_pages=config.max_pages)
        self.classifier = DocumentClassifier(
            instructions=config.instructions,
            api_key=config.api_key,
            model=config.model,
        )
        self.pretty = config.pretty_print_json

    def run(self):
        if not self.input_dir.is_dir():
            raise FileNotFoundError(f"No existe el directorio: {self.input_dir}")

        pdfs = sorted(self.input_dir.glob("*.pdf"))
        if not pdfs:
            raise FileNotFoundError(f"No se encontraron PDFs en: {self.input_dir}")

        # Contador global de archivos procesados
        contador = 0

        for pdf in pdfs:
            contador += 1

            # 1) Análisis del PDF
            analysis: AnalysisResult = self.analyzer.analyze(pdf)

            # 2) Clasificación con LLM
            classification: ClassificationResult = self.classifier.classify(analysis)

            # 3) Convertimos el resultado a dict y filtramos campos vacíos
            data: Dict[str, Any] = asdict(classification)
            filtrado = {
                k: v
                for k, v in data.items()
                if v is not None and not (isinstance(v, dict) and not v)
            }

            # 4) Agregamos el contador global al JSON de salida
            filtrado["count"] = contador

            # 5) Imprimimos el JSON enriquecido
            JsonPrinter.print(filtrado, pretty=self.pretty)
            print()  # salto de línea extra al final
