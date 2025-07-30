import json
from typing import Dict

from .client import call_chat_model

def _safe_parse(raw: str) -> Dict[str, str]:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}") + 1
        return json.loads(raw[start:end])

class LegalDocumentEngine:
    """
    Envuelve el modelo LLM con tu prompt de instrucciones.
    """

    def __init__(self, instructions: str, model: str = "gpt-3.5-turbo"):
        self.instructions = instructions
        self.model = model

    def classify(self, text: str) -> Dict[str, str]:
        messages = [
            {"role": "system",  "content": self.instructions},
            {"role": "user",    "content": text}
        ]
        raw = call_chat_model(messages, model=self.model)
        return _safe_parse(raw)
