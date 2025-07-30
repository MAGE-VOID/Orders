import json
from typing import Dict
from .client import LLMClient


class LegalDocumentEngine:
    def __init__(self, instructions: str, client: LLMClient):
        self.instructions = instructions
        self.client = client

    def classify(self, text: str) -> Dict[str, str]:
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": text},
        ]
        raw = self.client.chat(messages)
        return self._safe_parse(raw)

    def _safe_parse(self, raw: str) -> Dict[str, str]:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            s, e = raw.find("{"), raw.rfind("}") + 1
            return json.loads(raw[s:e])
