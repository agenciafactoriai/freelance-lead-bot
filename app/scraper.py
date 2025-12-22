# app/scraper.py

import logging
import random
import time
import re
import hashlib
from playwright.sync_api import sync_playwright, Page, Browser, Playwright, BrowserContext
from config import settings
from app.utils import get_stealth_runner

logger = logging.getLogger(__name__)
stealth_sync = get_stealth_runner()

class Scraper:
    """
    Clase que encapsula toda la interacción con Playwright para hacer web scraping.
    """
    def __init__(self):
        self.playwright: Playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    def start_browser(self):
        """Inicializa Playwright y lanza una instancia del navegador."""
        logger.info("🚀 Lanzando navegador con Playwright...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
        )
        self.context = self.browser.new_context(
            user_agent=random.choice(settings.USER_AGENTS),
            viewport={'width': 1920, 'height': 1080}
        )
        self.page = self.context.new_page()
        stealth_sync(self.page)
        logger.info("✅ Navegador listo.")

    def navigate_to(self, url: str):
        """Navega a la URL especificada."""
        self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
        time.sleep(random.uniform(4, 7))

    def get_project_cards(self):
        """Hace scroll y devuelve todos los elementos de las tarjetas de proyecto."""
        self._scroll_to_load_all()
        return self.page.query_selector_all(settings.SELECTORS["project_card"])

    def go_to_next_page(self) -> bool:
        """
        Busca el botón 'siguiente' y, si existe y es visible, hace clic en él.
        Devuelve True si pudo pasar de página, False en caso contrario.
        """
        next_btn = self.page.query_selector(settings.SELECTORS["next_button"])
        if next_btn and next_btn.is_visible():
            logger.info("   Navegando a la siguiente página...")
            next_btn.click()
            self.page.wait_for_load_state("domcontentloaded")
            time.sleep(random.uniform(3, 5))
            return True
        return False

    @staticmethod
    def parse_card(card_element) -> dict | None:
        """Extrae la información de un único elemento de tarjeta de proyecto."""
        title_el = card_element.query_selector(settings.SELECTORS["title_link"])
        if not title_el: return None
        
        raw_link = title_el.get_attribute("href")
        if not raw_link: return None

        link = "https://www.workana.com" + raw_link.split('?')[0]
        pid_match = re.search(r'/(\d+)', link)
        pid = pid_match.group(1) if pid_match else hashlib.md5(link.encode()).hexdigest()

        raw_title = title_el.inner_text().strip()
        desc = (el.inner_text() if (el := card_element.query_selector(settings.SELECTORS["description"])) else "").strip()
        skills = (el.inner_text().replace("\n", ", ") if (el := card_element.query_selector(settings.SELECTORS["skills"])) else "").strip()
        budget = (el.inner_text() if (el := card_element.query_selector(settings.SELECTORS["budget"])) else "").strip()
        
        return {
            "pid": pid, "raw_title": raw_title, "link": link,
            "desc": desc, "skills": skills, "budget": budget,
            "card_element": card_element  # Importante para tomar la captura después
        }

    def _scroll_to_load_all(self):
        """Realiza un scroll gradual para cargar todo el contenido dinámico."""
        try:
            self.page.wait_for_load_state("networkidle", timeout=3000)
        except Exception:
            pass
        for _ in range(random.randint(4, 6)):
            self.page.mouse.wheel(0, random.randint(600, 900))
            time.sleep(random.uniform(0.5, 1.2))
            
    def close_browser(self):
        """Cierra el navegador y libera los recursos de Playwright."""
        if self.browser: self.browser.close()
        if self.playwright: self.playwright.stop()
        logger.info("✅ Navegador cerrado de forma segura.")

