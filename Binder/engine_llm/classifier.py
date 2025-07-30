import os
from typing import Dict, List

from .llm.engine import LegalDocumentEngine

class SingleFileClassifier:
    """
    Toma la salida de PDFAnalyzer.analyze() y devuelve clasificación con LLM.
    """

    def __init__(self, instructions: str, api_key: str, model: str = "gpt-3.5-turbo"):
        os.environ["OPENAI_API_KEY"] = api_key
        self.engine = LegalDocumentEngine(instructions=instructions, model=model)

    def classify(self, analysis: Dict[str, str]) -> Dict[str, str]:
        # Propagar error de análisis si existe
        if "error" in analysis:
            return analysis

        try:
            result = self.engine.classify(analysis["text"])
            return {"file": analysis["file"], **result}
        except Exception as e:
            return {"file": analysis["file"], "error": str(e)}
