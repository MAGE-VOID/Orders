# engine_llm/pipeline.py

import json
import time
from pathlib import Path
from typing import Dict, Any
from collections import OrderedDict
from datetime import datetime

from PyPDF2 import PdfReader
from .config import Config
from .analyzer import PDFAnalyzer, AnalysisResult
from .classifier import DocumentClassifier, ClassificationResult
from .utils.pdf import read_pdf_bytes, count_pages


class JsonPrinter:
    @staticmethod
    def print(obj: Dict[str, Any], pretty: bool = False):
        text = json.dumps(obj, ensure_ascii=False, indent=2) if pretty else json.dumps(obj, ensure_ascii=False)
        print(text)


class DocumentPipeline:
    VERSION = "1.0"

    def __init__(self, config: Config):
        self.input_dir    = Path(config.input_dir)
        self.analyzer     = PDFAnalyzer(max_pages=config.max_pages)
        self.classifier   = DocumentClassifier(
            instructions=config.instructions,
            api_key=config.api_key,
            model=config.model,
        )
        self.pretty        = config.pretty_print_json
        self.llm_model     = config.model
        self.max_pages     = config.max_pages

    def _has_images(self, path: Path) -> bool:
        """
        Recorre todas las XObject de cada página, resolviendo IndirectObject
        hasta llegar al diccionario, y busca /Subtype == /Image.
        """
        reader = PdfReader(str(path))
        for page in reader.pages:
            resources = page.get("/Resources")
            if resources is None:
                continue
            resources = resources.get_object()

            xobj = resources.get("/XObject")
            if xobj is None:
                continue
            xobj = xobj.get_object()

            for obj in xobj.values():
                # si es indirecto, lo resolvemos
                try:
                    obj = obj.get_object()
                except AttributeError:
                    pass
                if obj.get("/Subtype") == "/Image":
                    return True
        return False

    def _error_code(self, msg: str) -> str:
        if msg is None:
            return None
        if "páginas" in msg:
            return "PAGE_LIMIT_EXCEEDED"
        if "no disponible" in msg:
            return "LLM_UNAVAILABLE"
        return "UNKNOWN_ERROR"

    def run(self):
        if not self.input_dir.is_dir():
            raise FileNotFoundError(f"No existe el directorio: {self.input_dir}")

        pdfs = sorted(self.input_dir.glob("*.pdf"))
        if not pdfs:
            raise FileNotFoundError(f"No se encontraron PDFs en: {self.input_dir}")

        count = 0

        for pdf in pdfs:
            count += 1
            start = time.perf_counter()

            # Metadatos del archivo
            raw_bytes    = read_pdf_bytes(pdf)
            size_b       = pdf.stat().st_size
            pages        = count_pages(raw_bytes)
            has_imgs     = self._has_images(pdf)

            # Etapas de análisis y clasificación
            analysis      = self.analyzer.analyze(pdf)
            classification = self.classifier.classify(analysis)

            elapsed_ms = int((time.perf_counter() - start) * 1000)

            status   = "error" if classification.error else "ok"
            err_msg  = classification.error or None
            err_code = self._error_code(err_msg)
            labels   = classification.labels or {
                "tipo_documento": "",
                "justificacion": ""
            }
            usage    = classification.tokens_usage or {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }

            # Construcción del JSON
            metadata = OrderedDict([
                ("count", count),
                ("file", classification.file),
                ("timestamp", datetime.utcnow().isoformat() + "Z"),
                ("llm_model", self.llm_model),
                ("file_size_bytes", size_b),
                ("page_count", pages),
                ("processing_time_ms", elapsed_ms),
                ("has_images", has_imgs),
            ])

            classification_section = OrderedDict([
                ("status", status),
                ("error_code", err_code),
                ("error", err_msg),
                ("labels", labels),
                ("tokens_usage", usage),
            ])

            result = OrderedDict([
                ("version", self.VERSION),
                ("metadata", metadata),
                ("classification", classification_section),
            ])

            JsonPrinter.print(result, pretty=self.pretty)
            print()  # línea en blanco entre archivos
