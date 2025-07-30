import json
from typing import Dict
from .client import LLMClient


class LegalDocumentEngine:
    """
    Envuelve las instrucciones (prompt), fuerza salida JSON y reintenta si no lo es.
    """

    # Número de veces que intentaremos corregir la salida JSON
    MAX_JSON_RETRIES = 2

    def __init__(self, instructions: str, client: LLMClient):
        # Añadimos al prompt una instrucción clara de salida JSON estricta
        strict_instructions = (
            instructions
            + "\n\nIMPORTANTE: responde únicamente con un JSON válido, sin ningún texto adicional."
        )
        self.instructions = strict_instructions
        self.client = client

    def classify(self, text: str) -> Dict[str, str]:
        # Construimos el mensaje inicial
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": text},
        ]

        raw = self.client.chat(messages)
        # Intento directo de parseo
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Si falla, reintentamos pedirle que corrija la salida
            for _ in range(self.MAX_JSON_RETRIES):
                fix_prompt = (
                    "La salida anterior no era un JSON válido:\n"
                    "```\n" + raw + "\n```\n"
                    "Por favor, responde AHORA _solo_ con el JSON válido."
                )
                messages.append({"role": "user", "content": fix_prompt})
                raw = self.client.chat(messages)
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    continue

            # Si después de todos los reintentos sigue mal, consideramos el error
            raise ValueError("No se pudo obtener JSON válido tras múltiples intentos.")
