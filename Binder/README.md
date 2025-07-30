# Document Classification Pipeline

Este proyecto implementa una **pipeline** completa para la clasificación de documentos jurídicos en formato PDF, incluyendo:

- **Extracción de texto** (nativo + OCR)  
- **Análisis de páginas** (límite configurable)  
- **Detección de imágenes**  
- **Clasificación mediante LLM** (OpenAI GPT‑3.5/4)  
- **Salida JSON enriquecido** con metadatos y métricas

---

## 📝 Estructura del proyecto

├── README.md
├── requirements.txt
├── .env ← configuración de variables de entorno
├── prompt_instructions.txt
├── main.py
├── pdf_examples/ ← PDFs de prueba
└── engine_llm/
├── analyzer.py
├── classifier.py
├── config.py
├── extractor.py
├── pipeline.py
├── llm/
│ ├── client.py
│ └── engine.py
└── utils/
├── pdf.py
└── ocr.py

markdown
Copiar
Editar

---

## 🚀 Características

- **Conteo de páginas** y **limitación** (`MAX_PDF_PAGES`)  
- **OCR** automatizado (Pillow + pytesseract + pdf2image)  
- **Detección de imágenes** embebidas en el PDF  
- **Clasificación** con OpenAI GPT (prompt configurado en `prompt_instructions.txt`)  
- **JSON output**:
  - Metadatos: `count`, `file`, `timestamp`, `llm_model`, `file_size_bytes`, `page_count`, `processing_time_ms`, `has_images`
  - Classification: `status`, `error_code`, `error`, `labels` (`tipo_documento` + `justificacion`), `tokens_usage`

---

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://turepo.git
   cd Binder