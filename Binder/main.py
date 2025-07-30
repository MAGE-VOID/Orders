from pathlib import Path
import logging

from engine_llm.config import Config
from engine_llm.pipeline import DocumentPipeline


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    # Cargo TODO: rutas, API key, instrucciones y parámetros
    config = Config()

    # Le paso TODO el config al pipeline
    pipeline = DocumentPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main()
