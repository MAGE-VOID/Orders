import time
from urllib.parse import quote_plus
from typing import List, Tuple
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WalmartSearchScraper:
    """
    Recibe una lista de queries, construye la URL con base_url
    y devuelve la lista de tuplas (id, query, url, html).
    Si el usuario cierra la ventana manualmente, se interrumpe limpiamente.
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
        self.brave_path = brave_path
        self.base_url = base_url
        self.timeout = timeout
        self.inspect_delay = inspect_delay
        self.verbose = verbose
        self.user_agent = user_agent
        self.driver = None

    def _log(self, *args, **kwargs) -> None:
        if self.verbose:
            print(*args, **kwargs)

    def _init_driver(self) -> None:
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
        Construye URLs con base_url.format(quote_plus(query)),
        navega, espera y devuelve (idx, query, url, html).
        Si se cierra o hay timeout, se detiene.
        """
        if not queries:
            return []

        if self.driver is None:
            self._init_driver()

        results = []
        for idx, query in enumerate(queries, start=1):
            url = self.base_url.format(quote_plus(query))
            self._log(f"[{idx}/{len(queries)}] Cargando '{query}' -> {url}")
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "a[link-identifier]")
                    )
                )
            except (WebDriverException, TimeoutException):
                self._log(f"⚠️ Error o timeout en '{query}'. Deteniendo.")
                break

            time.sleep(self.inspect_delay)

            try:
                html = self.driver.page_source
            except WebDriverException:
                self._log("⚠️ No se pudo extraer HTML. Navegador cerrado.")
                break

            results.append((idx, query, url, html))

        self.close()
        return results

    def close(self) -> None:
        """Cierra el navegador si está abierto."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None
                self._log("[STOP] Navegador cerrado.")
