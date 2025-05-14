#!/usr/bin/env python3
import sys
import re
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd
from lxml import html

from scraper import WalmartSearchScraper

SEPARATOR = "=" * 80
SUBSEPARATOR = "-" * 80

# =============================================================================
# Funciones de parsing y utilidades
# =============================================================================
def load_products(excel_path: Path) -> list[tuple[str, str]]:
    """
    Lee el Excel y retorna una lista de tuplas (sku_interno, cadena_de_busqueda).
    
    La cadena de búsqueda se compone de Producto + Linea + Categoria.
    """
    df = pd.read_excel(excel_path)
    required = ("SkuProducto", "Producto", "Linea", "Categoria")
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Faltan columnas en el Excel: {missing}")
    
    df = df[["SkuProducto", "Producto", "Linea", "Categoria"]].fillna("")
    return [
        (
            str(row["SkuProducto"]).strip(),
            " ".join([row["Producto"].strip(),
                      row["Linea"].strip(),
                      row["Categoria"].strip()]).strip(),
        )
        for _, row in df.iterrows()
    ]


def significant_tokens(text: str) -> set[str]:
    words = re.findall(r"\w+", text.lower())
    return {w for w in words if w.isalpha() and len(w) > 3}


def shorten_url(full_url: str) -> str:
    p = urlparse(full_url)
    return f"{p.scheme}://{p.netloc}{p.path}"


def extract_walmart_code(prod_elem) -> str:
    code = prod_elem.get("data-id", "")
    if code:
        return code

    variant = prod_elem.xpath(".//div[contains(@data-testid,'variant-')]/@data-testid")
    if variant:
        return variant[0].split("-", 1)[1]
    return ""


def extract_text_or_blank(xpath_result: list) -> str:
    return xpath_result[0].strip() if xpath_result else ""


def parse_product_element(prod_elem, query: str, sku: str) -> dict:
    """
    Dado un elemento <div> que representa un producto,
    extrae toda la info relevante y la retorna en un dict.
    
    Aplica un filtro básico de relevancia usando la intersección de tokens
    del título y la query. Si no coincide, retorna {} (vacío).
    """
    # Título
    raw_titles = prod_elem.xpath(".//a//text()")
    title = next((t.strip() for t in raw_titles if t.strip()), "")
    if not (significant_tokens(title) & significant_tokens(query)):
        return {}  # No coincide con query => descartar

    # Código Walmart
    walmart_code = extract_walmart_code(prod_elem)

    # URL
    link = extract_text_or_blank(prod_elem.xpath(".//a/@href"))
    if link.startswith("/"):
        link = "https://www.walmart.com.mx" + link
    link = shorten_url(link)

    # Precios
    price_div = prod_elem.xpath(".//div[@data-automation-id='product-price']")
    current_price = ""
    list_price = ""
    if price_div:
        # Normalmente hay 1 price_div
        cp_text = price_div[0].xpath("./div[@aria-hidden='true'][1]/text()")
        lp_text = price_div[0].xpath(".//div[contains(@class,'strike')]/text()")
        current_price = extract_text_or_blank(cp_text)
        list_price = extract_text_or_blank(lp_text)

    # Vendedor
    seller_raw = prod_elem.xpath("./div/div/div/div/div[2]/div[2]/text()")
    seller = extract_text_or_blank(seller_raw)

    # Imagen
    img_src = prod_elem.xpath(".//img/@src")
    img_url = shorten_url(extract_text_or_blank(img_src))

    return {
        "sku_interno": sku,
        "walmart_code": walmart_code,
        "title": title,
        "current_price": current_price,
        "list_price": list_price,
        "product_url": link,
        "seller": seller,
        "image_url": img_url,
    }


def process_search_result(
    sku: str, query: str, search_url: str, html_str: str, section_xpath: str
) -> list[dict]:
    """
    Procesa el HTML de la búsqueda de un producto (query) y extrae
    la información de cada producto dentro de la sección especificada.
    """
    doc = html.fromstring(html_str)
    section = doc.xpath(section_xpath)
    if not section:
        return []

    found_items = []
    for prod_elem in section[0].xpath("./*"):
        info = parse_product_element(prod_elem, query, sku)
        if info:
            found_items.append(info)

    return found_items


def display_item_info(item: dict) -> None:
    print(f"{'SKU interno':25}: {item['sku_interno']}")
    print(f"{'Código Walmart':25}: {item['walmart_code']}")
    print(f"{'Título':25}: {item['title']}")
    print(f"{'Precio actual':25}: {item['current_price']}")
    print(f"{'Precio lista':25}: {item['list_price']}")
    print(f"{'URL producto':25}: {item['product_url']}")
    print(f"{'Vendedor':25}: {item['seller']}")
    print(f"{'Imagen':25}: {item['image_url']}\n")


# =============================================================================
# Punto de entrada principal
# =============================================================================
def main():
    excel_path = Path(r"G:\Desktop\Orders\PriceLab\model_file_products.xlsx")
    products = load_products(excel_path)
    if not products:
        print("No hay productos para procesar.", file=sys.stderr)
        return

    scraper = WalmartSearchScraper(
        brave_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        base_url="https://www.walmart.com.mx/search?q={}",
        timeout=30,
        inspect_delay=5,
        verbose=True,
    )

    # Extraemos sólo la porción del HTML que nos interesa
    section_xpath = (
        "/html/body/div/div[1]/div/div/div[1]/main/div/div[2]/div/"
        "div/div[1]/div[2]/div/section/div"
    )

    # Preparar las queries (sin perder el orden original)
    queries = [p[1] for p in products]
    results = scraper.fetch_all(queries)
    print(f"\n📄 Páginas scrapeadas: {len(results)}\n")

    # Iterar en paralelo sobre products y results
    for (sku, query), (_, _, search_url, html_str) in zip(products, results):
        print(SEPARATOR)
        print(f"SKU interno   : {sku}")
        print(f"Búsqueda      : {query}")
        print(f"URL búsqueda  : {search_url}")
        print(SUBSEPARATOR)

        items = process_search_result(sku, query, search_url, html_str, section_xpath)
        if not items:
            print("No se encontraron productos relevantes o sección vacía.\n")
            continue

        for item in items:
            display_item_info(item)

    print(SEPARATOR)


if __name__ == "__main__":
    main()
