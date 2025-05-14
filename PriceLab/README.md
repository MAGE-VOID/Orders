# Walmart Search Scraper

Este proyecto incluye dos scripts para automatizar búsquedas en Walmart México y extraer información de productos:

1.  `scraper.py`
    * Clase `WalmartSearchScraper` que recibe una lista de queries y devuelve el HTML renderizado de cada búsqueda.
    * Utiliza Brave Browser vía `undetected-chromedriver` y Selenium para evadir detección anti-bots.

2.  `main.py`
    * Lee un Excel de entrada (`model_file_products.xlsx`) con las columnas SkuProducto, Producto, Linea y Categoria.
    * Construye las queries, invoca `WalmartSearchScraper` y parsea el HTML para extraer:
        * SKU interno
        * Busqueda
        * Título
        * Precio
        * URL del producto
        * Nombre del vendedor
        * URL de la imagen
    * Exporta los resultados a `resultados_walmart.xlsx`.

---

## Requisitos

* Python 3.8+
* Brave Browser instalado (ruta configurable en `main.py`).
* Dependencias Python:
    ```bash
    pip install undetected-chromedriver selenium pandas lxml openpyxl
    ```

---

## Configuración

1.  Colocar el Excel de entrada `model_file_products.xlsx` en la carpeta raíz.

2.  Verificar que el Excel contiene las columnas:
    * SkuProducto
    * Producto
    * Linea
    * Categoria