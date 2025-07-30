# engine_llm/llm/engine.py

import json
from typing import Dict, Tuple
from .client import LLMClient


class LegalDocumentEngine:
    """
    Envuelve instrucciones y devuelve (labels_dict, tokens_usage).
    """

    MAX_JSON_RETRIES = 2

    def __init__(self, instructions: str, client: LLMClient):
        strict = (
            instructions
            + "\n\nIMPORTANTE: responde únicamente con un JSON válido, sin texto adicional."
        )
        self.instructions = strict
        self.client = client

    def classify(self, text: str) -> Tuple[Dict[str, str], Dict[str, int]]:
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": text},
        ]

        raw, usage = self.client.chat(messages)
        try:
            labels = json.loads(raw)
            return labels, usage
        except json.JSONDecodeError:
            for _ in range(self.MAX_JSON_RETRIES):
                fix_prompt = (
                    "La salida anterior no era un JSON válido:\n"
                    f"```\n{raw}\n```\n"
                    "Por favor, responde AHORA _solo_ con el JSON válido."
                )
                messages.append({"role": "user", "content": fix_prompt})
                raw, usage = self.client.chat(messages)
                try:
                    labels = json.loads(raw)
                    return labels, usage
                except json.JSONDecodeError:
                    continue
            raise ValueError("No se pudo obtener JSON válido tras múltiples intentos.")
