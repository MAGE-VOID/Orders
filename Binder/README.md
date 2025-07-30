# Document Processor

Una herramienta de procesamiento y clasificación de documentos PDF basada en LLMs y OCR.

## Descripción

Este proyecto permite:

- Leer y procesar archivos PDF de un directorio  
- Extraer texto de forma robusta (PyMuPDF, pdfplumber y OCR)  
- Enviar el texto a un LLM para clasificar documentos legales siguiendo instrucciones predefinidas  
- Imprimir el resultado en formato JSON (metadatos, estado, etiquetas y uso de tokens)  

Está diseñado para ser sencillo de configurar y ejecutar, ideal para flujos de trabajo batch de clasificación de PDFs.

## Características

- **Extracción de texto multilayer**
  - PyMuPDF para texto selectable  
  - pdfplumber para layouts complejos  
  - OCR página-a-página con Tesseract  
- **Clasificación con LLM**
  - Cliente OpenAI con reintentos  
  - Motor que asegura salida JSON válida  
- **Control de páginas**
  - Límite configurable de páginas (por defecto 5)  
  - Errores claros si se excede el límite  
- **Salida JSON**
  - Metadatos del archivo (tamaño, páginas, imágenes)  
  - Estado del procesamiento  
  - Etiquetas resultantes y uso de tokens  
- **Estructura modular**
  - Código dividido en extractor, analizador, clasificador y pipeline

## Estructura de Directorios

├── main.py  
├── requirements.txt  
├── prompt_instructions.txt  
├── pdf_examples/  
│ ├── 1.pdf  
│ └── ...  
└── document_processor/  
├── config.py  
├── pipeline.py  
├── analyzer.py  
├── classifier.py  
├── extractor.py  
├── llm/  
│ ├── client.py  
│ └── engine.py  
└── utils/  
├── pdf.py  
└── ocr.py

## Requisitos

- Python ≥ 3.8  
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) instalado  
- Variables de entorno en un archivo \`.env\` (ver más abajo)

## Instalación

git clone <url-del-repo>
cd <nombre-del-repo>

## Configuración

1. Crear un archivo `.env` en la raíz del proyecto:

OPENAI_API_KEY=tu_api_key_de_openai

2. Personaliza el archivo `prompt_instructions.txt` para definir cómo debe clasificar el LLM.
3. Puedes ajustar parámetros por defecto en `document_processor/config.py`.

## Uso

Ejecuta el siguiente comando para procesar todos los PDFs en `pdf_examples/`:

python main.py

Cada documento genera una salida JSON como esta:

{
  "version": "1.0",
  "metadata": {
    "count": 1,
    "file": "1.pdf",
    "timestamp": "2025-07-30T15:42:10Z",
    "llm_model": "gpt-4.1-nano",
    "file_size_bytes": 34567,
    "page_count": 3,
    "processing_time_ms": 870,
    "has_images": false
  },
  "classification": {
    "status": {
      "state": "ok",
      "error_code": "",
      "description": ""
    },
    "labels": {
      "tipo_documento": "Contrato",
      "justificacion": "..."
    },
    "tokens_usage": {
      "prompt_tokens": 64,
      "completion_tokens": 32,
      "total_tokens": 96
    }
  }
}


## Personalización

- **Máximo de páginas**: cambia `DEFAULT_MAX_PAGES` en `config.py`.
- **Formato del JSON**: ajusta `DEFAULT_PRETTY_PRINT`.
- **Modelo del LLM**: cambia `DEFAULT_LLM_MODEL`.