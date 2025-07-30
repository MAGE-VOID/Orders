import logging
from typing import List
from PIL import Image

from .utils.pdf import extract_selectable_text
from .utils.ocr import pdf_to_images, ocr_images


class TextExtractor:
    def __init__(self, ocr_threshold: int = 20):
        self.ocr_threshold = ocr_threshold
        self.logger = logging.getLogger(self.__class__.__name__)
        self._warned = False

    def extract(self, pdf_bytes: bytes) -> str:
        pages = extract_selectable_text(pdf_bytes)
        images: List[Image.Image] = pdf_to_images(pdf_bytes)

        if not images and any(len(p.strip()) < self.ocr_threshold for p in pages):
            if not self._warned:
                self.logger.warning(
                    "Poppler no está instalado: OCR omitido en páginas vacías"
                )
                self._warned = True

        result: List[str] = []
        for i, text in enumerate(pages):
            if len(text.strip()) >= self.ocr_threshold:
                result.append(text)
            elif i < len(images):
                result.extend(ocr_images([images[i]]))
        return "\n".join(result)
