import time
from typing import List, Dict, Protocol
from openai import OpenAI


class LLMClient(Protocol):
    def chat(self, messages: List[Dict], **kwargs) -> str: ...


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(
        self, messages: List[Dict], max_retries: int = 3, retry_delay: float = 2
    ) -> str:
        for attempt in range(max_retries):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model, messages=messages
                )
                return resp.choices[0].message.content
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * 2**attempt)
                else:
                    raise
