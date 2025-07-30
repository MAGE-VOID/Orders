from pathlib import Path
import logging

from engine_llm.config import Config
from engine_llm.pipeline import DocumentPipeline


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    config = Config()

    pipeline = DocumentPipeline(
        input_dir=config.input_dir,
        analyzer_max_pages=config.max_pages,
        classifier_instructions=config.instructions,
        classifier_model=config.model,
        classifier_api_key=config.api_key,
    )
    pipeline.run()


if __name__ == "__main__":
    main()
