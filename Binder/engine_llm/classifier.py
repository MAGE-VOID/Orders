# engine_llm/classifier.py

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
    tokens_usage: Optional[Dict[str, int]] = None


class DocumentClassifier:
    """
    Encapsula la llamada al LLM para clasificar documentos.
    """

    def __init__(self, instructions: str, api_key: str, model: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = OpenAIClient(api_key=api_key, model=model)
        self.engine = LegalDocumentEngine(instructions=instructions, client=self.client)

    def classify(self, analysis: AnalysisResult) -> ClassificationResult:
        if analysis.error:
            return ClassificationResult(
                file=analysis.file,
                error=analysis.error,
                tokens_usage={
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            )
        try:
            labels, usage = self.engine.classify(analysis.text)
            return ClassificationResult(
                file=analysis.file, labels=labels, tokens_usage=usage
            )
        except ServiceUnavailableError:
            msg = "Servicio OpenAI no disponible. Intenta de nuevo más tarde."
            self.logger.error(msg + " para %s", analysis.file)
            return ClassificationResult(
                file=analysis.file,
                error=msg,
                tokens_usage={
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            )
        except Exception as e:
            self.logger.error("Error clasificando %s: %s", analysis.file, e)
            return ClassificationResult(
                file=analysis.file,
                error=str(e),
                tokens_usage={
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            )
