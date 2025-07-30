# document_processor/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# ————— VARIABLES DE CONFIGURACIÓN —————
ENV_FILE_NAME          = ".env"
ENV_VAR_API_KEY        = "OPENAI_API_KEY"

DEFAULT_LLM_MODEL      = "gpt-4.1-nano"
INSTRUCTIONS_FILE_NAME = "prompt_instructions.txt"
PDF_EXAMPLES_DIR       = "pdf_examples"

DEFAULT_MAX_PAGES      = 5
DEFAULT_PRETTY_PRINT   = 1  # 0 = JSON compacto, 1 = JSON con indentación
# —————————————————————————————————————

class Config:
    """
    Carga de configuración centralizada.
    """

    def __init__(self, base_dir: Path = Path(__file__).parent.parent):
        self.base_dir           = base_dir
        self.env_file           = base_dir / ENV_FILE_NAME
        self.instructions_file  = base_dir / INSTRUCTIONS_FILE_NAME
        self.input_dir          = base_dir / PDF_EXAMPLES_DIR

        # Carga variables de .env si existe
        self._load_env()

        # Variable obligatoria
        self.api_key            = self._get_env_var(ENV_VAR_API_KEY)
        # Modelo del LLM
        self.model              = DEFAULT_LLM_MODEL
        # Instrucciones para el LLM
        self.instructions       = self._read_text(self.instructions_file)

        # Parámetros fijos
        self.max_pages          = DEFAULT_MAX_PAGES
        self.pretty_print_json  = bool(DEFAULT_PRETTY_PRINT)

    def _load_env(self) -> None:
        if self.env_file.exists():
            load_dotenv(str(self.env_file))

    def _get_env_var(self, key: str) -> str:
        val = os.getenv(key)
        if not val:
            raise RuntimeError(f"Falta variable de entorno `{key}`")
        return val

    def _read_text(self, path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"No existe: {path}")
        return path.read_text(encoding="utf-8")
