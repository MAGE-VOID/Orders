from typing import List
from PIL import Image
from pdf2image import convert_from_bytes
from pdf2image.exceptions import PDFInfoNotInstalledError
import pytesseract


def pdf_to_images(pdf_bytes: bytes, dpi: int = 300) -> List[Image.Image]:
    try:
        return convert_from_bytes(pdf_bytes, dpi=dpi)
    except PDFInfoNotInstalledError:
        return []
    except Exception:
        return []


def ocr_images(images: List[Image.Image], lang: str = "spa") -> List[str]:
    return [pytesseract.image_to_string(img, lang=lang) for img in images]
