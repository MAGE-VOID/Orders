import logging
from typing import List
from PIL import Image

from .utils.pdf import extract_selectable_text
from .utils.ocr import pdf_to_images, ocr_images


class TextExtractor:
    """
    Extrae todo el texto disponible de un PDF, combinando:
      - Texto 'seleccionable' de cada página
      - Resultado de OCR de la imagen de cada página
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def extract(self, pdf_bytes: bytes) -> str:
        # 1) Sacamos el texto seleccionable por página
        pages_text: List[str] = extract_selectable_text(pdf_bytes)
        # 2) Convertimos cada página a imagen
        images: List[Image.Image] = pdf_to_images(pdf_bytes)

        full_text: List[str] = []
        for idx, page_text in enumerate(pages_text):
            # Añadimos texto seleccionable (puede estar vacío)
            full_text.append(page_text or "")

            # Si tenemos una imagen para esta página, le aplicamos OCR
            if idx < len(images):
                try:
                    ocr_results = ocr_images([images[idx]])
                    # ocr_images devuelve lista; aquí solo una entrada
                    full_text.append(ocr_results[0] or "")
                except Exception as e:
                    self.logger.error("Error OCR en página %d: %s", idx + 1, e)
                    # Continuamos aun si OCR falla

        # Si hubiera más imágenes que páginas (raro), procesamos el resto también
        if len(images) > len(pages_text):
            for extra_img in images[len(pages_text) :]:
                try:
                    ocr_results = ocr_images([extra_img])
                    full_text.append(ocr_results[0] or "")
                except Exception as e:
                    self.logger.error("Error OCR en página extra: %s", e)

        # Unimos todo, filtrando cadenas vacías
        return "\n".join(filter(lambda s: s.strip() != "", full_text))
