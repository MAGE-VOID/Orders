import time
from typing import List, Dict, Protocol
import openai


class ServiceUnavailableError(Exception):
    """Indica que el servicio de OpenAI no respondió tras agotar reintentos."""

    pass


class LLMClient(Protocol):
    def chat(self, messages: List[Dict], **kwargs) -> str: ...


class OpenAIClient:
    """
    Cliente de OpenAI con reintentos en caso de cualquier excepción al llamar al API.
    Tras agotar reintentos, lanza ServiceUnavailableError.
    """

    def __init__(self, api_key: str, model: str):
        # Usa el cliente de la librería OpenAI
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def chat(
        self, messages: List[Dict], max_retries: int = 3, retry_delay: float = 2.0
    ) -> str:
        for attempt in range(max_retries):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model, messages=messages
                )
                return resp.choices[0].message.content
            except Exception as e:
                # Espera y reintenta
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2**attempt))
                    continue
                # Si tras todos los reintentos sigue fallando => servicio no disponible
                raise ServiceUnavailableError("OpenAI service unavailable") from e
