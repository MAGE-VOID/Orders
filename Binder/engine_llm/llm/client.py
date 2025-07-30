# engine_llm/llm/client.py

import time
from typing import List, Dict, Protocol, Tuple
import openai


class ServiceUnavailableError(Exception):
    """Indica que el servicio de OpenAI no respondió tras agotar reintentos."""

    pass


class LLMClient(Protocol):
    def chat(self, messages: List[Dict], **kwargs) -> Tuple[str, Dict[str, int]]: ...


class OpenAIClient:
    """
    Cliente de OpenAI con reintentos. Ahora devuelve (content, tokens_usage).
    """

    def __init__(self, api_key: str, model: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def chat(
        self, messages: List[Dict], max_retries: int = 3, retry_delay: float = 2.0
    ) -> Tuple[str, Dict[str, int]]:
        for attempt in range(max_retries):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model, messages=messages
                )
                content = resp.choices[0].message.content
                usage = resp.usage
                tokens_usage = {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                }
                return content, tokens_usage
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2**attempt))
                    continue
                raise ServiceUnavailableError("OpenAI service unavailable") from e
