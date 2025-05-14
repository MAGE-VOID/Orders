import sys
import re
from pathlib import Path
from urllib.parse import urlparse
import pandas as pd
from lxml import html
from scraper import WalmartSearchScraper

SECTION_XPATH = (
    "/html/body/div/div[1]/div/div/div[1]/main/div/div[2]/div/"
    "div/div[1]/div[2]/div/section/div"
)


def load_products(excel_path: Path) -> list[tuple[str, str]]:
    """
    Lee el Excel y devuelve [(sku_interno, query), …].
    """
    df = pd.read_excel(excel_path)
    for col in ("SkuProducto", "Producto", "Linea", "Categoria"):
        if col not in df.columns:
            raise KeyError(f"Falta columna en el Excel: {col}")
    df = df[["SkuProducto", "Producto", "Linea", "Categoria"]].fillna("")
    products = []
    for _, row in df.iterrows():
        sku = str(row["SkuProducto"]).strip()
        query = " ".join(
            [row["Producto"].strip(), row["Linea"].strip(), row["Categoria"].strip()]
        ).strip()
        products.append((sku, query))
    return products


def significant_tokens(text: str) -> set[str]:
    """
    Obtiene tokens relevantes (>3 letras) en minúscula.
    """
    tokens = re.findall(r"\w+", text.lower())
    return {t for t in tokens if t.isalpha() and len(t) > 3}


def shorten_url(full_url: str) -> str:
    """
    Acorta un URL dejando esquema://dominio/path.
    """
    p = urlparse(full_url)
    return f"{p.scheme}://{p.netloc}{p.path}"


def extract_text(xpath_result: list[str]) -> str:
    """
    Toma el primer elemento de la lista y lo limpia, o cadena vacía.
    """
    return xpath_result[0].strip() if xpath_result else ""


def parse_product(prod_elem, query: str, sku: str) -> dict[str, str]:
    """
    Extrae datos de un elemento <div> de producto.
    Retorna {} si el título no coincide con la query.
    """
    title = next((t.strip() for t in prod_elem.xpath(".//a//text()") if t.strip()), "")
    if not (significant_tokens(title) & significant_tokens(query)):
        return {}

    href = extract_text(prod_elem.xpath(".//a/@href"))
    url = f"https://www.walmart.com.mx{href}" if href.startswith("/") else href
    url = shorten_url(url)

    price_div = prod_elem.xpath(".//div[@data-automation-id='product-price']")
    price = ""
    if price_div:
        price = extract_text(price_div[0].xpath("./div[@aria-hidden='true'][1]/text()"))

    seller = extract_text(prod_elem.xpath("./div/div/div/div/div[2]/div[2]/text()"))
    img = extract_text(prod_elem.xpath(".//img/@src"))
    img = shorten_url(img)

    return {
        "SKU interno": sku,
        "Busqueda": query,
        "Título": title,
        "Precio": price,
        "URL": url,
        "Vendedor": seller,
        "Imagen": img,
    }


def process_search(sku: str, query: str, html_str: str) -> list[dict[str, str]]:
    """
    Procesa el HTML de una búsqueda y devuelve la lista de productos.
    """
    doc = html.fromstring(html_str)
    sec = doc.xpath(SECTION_XPATH)
    if not sec:
        return []
    return [
        info
        for elem in sec[0].xpath("./*")
        for info in (parse_product(elem, query, sku),)
        if info
    ]


def main():
    excel_path = Path(r"G:\Desktop\Orders\PriceLab\model_file_products.xlsx")
    output_file = excel_path.parent / "resultados_walmart.xlsx"

    try:
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

        queries = [q for _, q in products]
        results = scraper.fetch_all(queries)

        all_data = []
        for (sku, query), (_, _, _, html_str) in zip(products, results):
            all_data.extend(process_search(sku, query, html_str))

        if all_data:
            df = pd.DataFrame(
                all_data,
                columns=[
                    "SKU interno",
                    "Busqueda",
                    "Título",
                    "Precio",
                    "URL",
                    "Vendedor",
                    "Imagen",
                ],
            )
            df.to_excel(output_file, index=False)
            print(f"Datos guardados en: {output_file}")
        else:
            print("No se encontraron productos relevantes.", file=sys.stderr)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            scraper.close()
        except NameError:
            pass


if __name__ == "__main__":
    main()
