import logging
from dataclasses import dataclass
from typing import Any, Dict

from .llm.client import OpenAIClient
from .llm.engine import LegalDocumentEngine
from .analyzer import AnalysisResult


@dataclass
class ClassificationResult:
    file: str
    labels: Dict[str, Any] = None
    error: str = ""


class DocumentClassifier:
    """
    Encapsula la llamada al LLM para clasificar documentos.
    El parámetro `model` debe llegarnos desde Config.
    """

    def __init__(self, instructions: str, api_key: str, model: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = OpenAIClient(api_key=api_key, model=model)
        self.engine = LegalDocumentEngine(instructions=instructions, client=self.client)

    def classify(self, analysis: AnalysisResult) -> ClassificationResult:
        if analysis.error:
            return ClassificationResult(file=analysis.file, error=analysis.error)

        try:
            resp = self.engine.classify(analysis.text)
            return ClassificationResult(file=analysis.file, labels=resp)
        except Exception as e:
            self.logger.error("Error clasificando %s: %s", analysis.file, e)
            return ClassificationResult(file=analysis.file, error=str(e))
