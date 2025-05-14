import time
import undetected_chromedriver as uc
from urllib.parse import quote_plus
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Tuple


class WalmartSearchScraper:
    """
    Scraper que recibe una lista de queries,
    construye la URL de búsqueda usando `base_url`,
    y devuelve una lista de tuplas:
      [
        (id, query, url, html_renderizado),
        ...
      ]
    Si el usuario cierra la ventana manualmente, interrumpe y sale limpiamente.
    """

    def __init__(
        self,
        brave_path: str,
        base_url: str,
        timeout: int = 30,
        inspect_delay: int = 5,
        verbose: bool = True,
        user_agent: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/136.0.7103.93 Safari/537.36"
        ),
    ):
        """
        :param brave_path: ruta al ejecutable de Brave
        :param base_url: plantilla de URL con un `{}` para el término
        :param timeout: segundos a esperar por carga de elementos
        :param inspect_delay: pausa tras carga antes de extraer HTML
        :param verbose: si es True, muestra los mensajes por pantalla
        :param user_agent: cadena UA a usar
        """
        self.brave_path = brave_path
        self.base_url = base_url
        self.timeout = timeout
        self.inspect_delay = inspect_delay
        self.verbose = verbose
        self.user_agent = user_agent
        self.driver = None

    def _log(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)

    def _init_driver(self):
        opts = uc.ChromeOptions()
        opts.binary_location = self.brave_path
        opts.add_argument("--start-minimized")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_argument("--lang=es-ES")
        opts.add_argument(f"user-agent={self.user_agent}")
        self.driver = uc.Chrome(options=opts)
        try:
            self.driver.minimize_window()
        except Exception:
            pass

    def fetch_all(self, queries: List[str]) -> List[Tuple[int, str, str, str]]:
        """
        Para cada término en `queries`:
          1) Construye la URL con `base_url.format(quote_plus(query))`
          2) Navega, espera y extrae HTML
        Retorna lista de tuplas (id, query, url, html).
        Si el navegador se cierra inesperadamente, detiene el proceso.
        """
        if not queries:
            return []

        if self.driver is None:
            self._init_driver()

        results: List[Tuple[int, str, str, str]] = []
        for idx, query in enumerate(queries, start=1):
            search_url = self.base_url.format(quote_plus(query))
            self._log(f"[{idx}/{len(queries)}] Cargando «{query}» → {search_url}")

            try:
                self.driver.get(search_url)
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "a[link-identifier]")
                    )
                )
            except (WebDriverException, TimeoutException):
                self._log(f"⚠️ Navegador cerrado o timeout en «{query}». Deteniendo.")
                break

            # pausa para asegurar renderizado completo
            time.sleep(self.inspect_delay)

            try:
                html = self.driver.page_source
            except WebDriverException:
                self._log("⚠️ No se pudo extraer HTML; navegador posiblemente cerrado.")
                break

            results.append((idx, query, search_url, html))

        self.close()
        return results

    def close(self):
        """Cierra el navegador si está abierto."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
            self._log("🛑 Navegador cerrado.")


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
