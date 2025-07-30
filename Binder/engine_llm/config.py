import os
from pathlib import Path
from dotenv import load_dotenv

# ————— VARIABLES DE CONFIGURACIÓN —————
ENV_FILE_NAME           = ".env"
INSTRUCTIONS_FILE_NAME  = "prompt_instructions.txt"
PDF_EXAMPLES_DIR        = "pdf_examples"

ENV_VAR_API_KEY         = "OPENAI_API_KEY"
ENV_VAR_MAX_PAGES       = "MAX_PDF_PAGES"
ENV_VAR_PRETTY_PRINT    = "PRETTY_PRINT_JSON"

DEFAULT_LLM_MODEL       = "gpt-3.5-turbo"
DEFAULT_MAX_PAGES       = 5
DEFAULT_PRETTY_PRINT    = 1  # 0 = JSON compacto, 1 = JSON con indentación
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

        self._load_env()
        self.api_key            = self._get_env_var(ENV_VAR_API_KEY)
        self.model              = DEFAULT_LLM_MODEL
        self.instructions       = self._read_text(self.instructions_file)
        self.max_pages          = int(os.getenv(ENV_VAR_MAX_PAGES, str(DEFAULT_MAX_PAGES)))

        # Nuevo flag para JSON formateado en terminal
        pretty_flag             = os.getenv(ENV_VAR_PRETTY_PRINT, str(DEFAULT_PRETTY_PRINT))
        self.pretty_print_json = bool(int(pretty_flag))

    def _load_env(self) -> None:
        if self.env_file.exists():
            load_dotenv(self.env_file)

    def _get_env_var(self, key: str) -> str:
        val = os.getenv(key)
        if not val:
            raise RuntimeError(f"Falta variable de entorno `{key}`")
        return val

    def _read_text(self, path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"No existe: {path}")
        return path.read_text(encoding="utf-8")
