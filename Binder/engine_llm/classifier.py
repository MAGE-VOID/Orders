import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from .llm.client import OpenAIClient, ServiceUnavailableError
from .llm.engine import LegalDocumentEngine
from .analyzer import AnalysisResult


@dataclass
class ClassificationResult:
    file: str
    labels: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class DocumentClassifier:
    """
    Encapsula la llamada al LLM para clasificar documentos.
    El parámetro `model` debe venir de Config.
    """

    def __init__(self, instructions: str, api_key: str, model: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = OpenAIClient(api_key=api_key, model=model)
        self.engine = LegalDocumentEngine(instructions=instructions, client=self.client)

    def classify(self, analysis: AnalysisResult) -> ClassificationResult:
        # Si falló el paso de análisis
        if analysis.error:
            return ClassificationResult(file=analysis.file, error=analysis.error)

        try:
            resp = self.engine.classify(analysis.text)
            return ClassificationResult(file=analysis.file, labels=resp)
        except ServiceUnavailableError:
            self.logger.error("Servicio OpenAI no disponible para %s", analysis.file)
            return ClassificationResult(
                file=analysis.file,
                error="Servicio OpenAI no disponible. Intenta de nuevo más tarde.",
            )
        except Exception as e:
            self.logger.error("Error clasificando %s: %s", analysis.file, e)
            return ClassificationResult(file=analysis.file, error=str(e))
