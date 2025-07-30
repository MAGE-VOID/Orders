from pathlib import Path
import logging

from document_processor.config import Config
from document_processor.pipeline import DocumentPipeline

def main():
    config = Config()
    pipeline = DocumentPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main()
