import sys
from typing import List

from .utils.pdf import extract_selectable_text
from .utils.ocr import pdf_to_images, ocr_images

# Sólo mostrar esta advertencia una vez
_poppler_warning_shown = False

class TextExtractor:
    """
    Combina texto 'seleccionable' y OCR para retornar el texto completo.
    """

    def __init__(self, ocr_threshold: int = 20):
        self.ocr_threshold = ocr_threshold

    def extract(self, pdf_bytes: bytes) -> str:
        from .utils.pdf import extract_selectable_text

        pages: List[str] = extract_selectable_text(pdf_bytes)
        full_text: List[str] = []
        images = pdf_to_images(pdf_bytes)

        # Advertencia si no hay imágenes pero hay páginas vacías
        global _poppler_warning_shown
        if not images and any(len(p.strip()) < self.ocr_threshold for p in pages):
            if not _poppler_warning_shown:
                print(
                    "Advertencia: Poppler (pdftoppm/pdfinfo) no instalado, OCR omitido.",
                    file=sys.stderr
                )
                _poppler_warning_shown = True

        for idx, txt in enumerate(pages):
            if len(txt.strip()) >= self.ocr_threshold:
                full_text.append(txt)
            elif idx < len(images):
                ocr_txt = ocr_images([images[idx]])
                full_text.extend(ocr_txt)
            # si no hay imagen, omitimos sin error

        return "\n".join(full_text)
