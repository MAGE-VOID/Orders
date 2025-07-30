# document_processor/extractor.py

import io
import logging
from typing import List

import fitz
import pdfplumber
from PIL import Image

from .utils.ocr import pdf_to_images, ocr_images

LOG = logging.getLogger(__name__)


class TextExtractor:
    """
    Extrae texto de un PDF en hasta 3 fases:
      1) PyMuPDF, rápido y preciso.
      2) pdfplumber, para layouts complejos (tablas/columnas).
      3) OCR página-a-página si faltó texto.
    """

    def __init__(self, min_chars_per_page: int = 30):
        self.min_chars = min_chars_per_page

    def extract(self, pdf_bytes: bytes) -> str:
        # 1) Extracción con PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages_text: List[str] = []
        for page in doc:
            txt = page.get_text("text") or ""
            if len(txt.strip()) >= self.min_chars:
                pages_text.append(txt)
            else:
                pages_text.append("")  # marcamos para fallback
        doc.close()

        # 2) Extracción con pdfplumber para páginas vacías
        if any(not t.strip() for t in pages_text):
            try:
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for i, page in enumerate(pdf.pages):
                        if not pages_text[i].strip():
                            t = page.extract_text() or ""
                            pages_text[i] = t
            except Exception as e:
                LOG.warning("pdfplumber falló: %s", e)

        # 3) OCR para lo que quede vacío
        images: List[Image.Image] = pdf_to_images(pdf_bytes)
        full_text: List[str] = []
        for idx, text in enumerate(pages_text):
            if text and text.strip():
                full_text.append(text)
            else:
                # intentamos OCR en esa página
                if idx < len(images):
                    try:
                        ocr_res = ocr_images([images[idx]])[0] or ""
                        full_text.append(ocr_res)
                    except Exception as e:
                        LOG.error("OCR fallo en página %d: %s", idx + 1, e)
                else:
                    full_text.append("")

        # 4) Si quedan imágenes extra (raro), OCR resto
        if len(images) > len(pages_text):
            for img in images[len(pages_text) :]:
                try:
                    full_text.append(ocr_images([img])[0] or "")
                except Exception as e:
                    LOG.error("OCR en página extra: %s", e)

        # Unimos todo filtrando vacíos
        return "\n".join(p for p in full_text if p.strip())
