import os
import sys
import json

from dotenv import load_dotenv
from engine_llm.pipeline import DocumentPipeline


def load_api_key(env_path: str) -> str:
    if os.path.isfile(env_path):
        load_dotenv(env_path)
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            f"No se encontró OPENAI_API_KEY ni en entorno ni en {env_path}"
        )
    return key


def load_instructions(instr_path: str) -> str:
    if not os.path.isfile(instr_path):
        raise FileNotFoundError(f"No existe el archivo de instrucciones: {instr_path}")
    with open(instr_path, encoding="utf-8") as f:
        return f.read()


def run_pipeline(input_dir: str, instructions_file: str, env_file: str) -> None:
    api_key = load_api_key(env_file)
    instructions = load_instructions(instructions_file)

    pipeline = DocumentPipeline(instructions=instructions, api_key=api_key)
    pipeline.run(input_dir)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(BASE_DIR, "pdf_examples")
    INSTRUCTIONS_FILE = os.path.join(BASE_DIR, "prompt_instructions.txt")
    ENV_FILE = os.path.join(BASE_DIR, ".env")

    try:
        run_pipeline(INPUT_DIR, INSTRUCTIONS_FILE, ENV_FILE)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
