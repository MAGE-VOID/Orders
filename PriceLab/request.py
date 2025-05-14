from scraper import WalmartSearchScraper

if __name__ == "__main__":
    queries = [
        "Push Car Prinsel Adventure Rojo",
        "PlayHouse 2 en 1 Prinsel Unisex",
        # ...
    ]

    scraper = WalmartSearchScraper(
        brave_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        base_url="https://www.walmart.com.mx/search?q={}",
        timeout=30,
        inspect_delay=5,
        verbose=True,
    )

    results = scraper.fetch_all(queries)

    print(f"\n📄 Páginas scrapeadas: {len(results)}\n")
    for idx, query, url, html in results:
        print(f'- {idx}, "{query}", {url}, longitud HTML = {len(html)}')
