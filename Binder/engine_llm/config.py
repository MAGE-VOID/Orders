import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    def __init__(self, base_dir: Path = Path(__file__).parent.parent):
        self.base_dir = base_dir
        self.env_file = base_dir / ".env"
        self.instructions_file = base_dir / "prompt_instructions.txt"
        self.input_dir = base_dir / "pdf_examples"

        self._load_env()
        self.api_key = self._get("OPENAI_API_KEY")
        self.instructions = self._read_text(self.instructions_file)
        self.max_pages = int(os.getenv("MAX_PDF_PAGES", "5"))
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    def _load_env(self):
        if self.env_file.exists():
            load_dotenv(self.env_file)

    def _get(self, key: str) -> str:
        v = os.getenv(key)
        if not v:
            raise RuntimeError(f"Falta variable de entorno `{key}`")
        return v

    def _read_text(self, path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"No existe: {path}")
        return path.read_text(encoding="utf-8")
