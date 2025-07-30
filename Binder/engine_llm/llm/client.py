import os
import time
from typing import Any, Dict, List

import openai

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("No se encontró OPENAI_API_KEY para el cliente OpenAI")

client = openai.OpenAI(api_key=API_KEY)

def call_chat_model(
    messages: List[Dict[str, Any]],
    model: str = "gpt-3.5-turbo",
    max_retries: int = 3,
    retry_delay: float = 2.0
) -> str:
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
            else:
                raise
