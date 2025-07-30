from pathlib import Path
import logging

from engine_llm.config import Config
from engine_llm.pipeline import DocumentPipeline


def main():
    config = Config()
    pipeline = DocumentPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main()
