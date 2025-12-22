# app/bot.py

import time
import logging
import re
from datetime import datetime

from config import settings
from app import database
from app import notifier
from app.scraper import Scraper

logger = logging.getLogger(__name__)

class WorkanaBot:
    """
    Clase principal que orquesta el proceso de scraping y notificación.
    """
    def __init__(self):
        logger.info("🔧 Inicializando WorkanaBot...")
        database.init_db()
        self.scraper = Scraper()
        self.first_run = True

    def run(self):
        """Inicia el navegador y comienza el bucle infinito de monitoreo."""
        self.scraper.start_browser()
        while True:
            try:
                logger.info("🌐 Iniciando nuevo ciclo de escaneo...")
                self.scraper.navigate_to(settings.WORKANA_URL)
                
                if self.first_run:
                    logger.info("📸 Tomando captura de diagnóstico inicial...")
                    screenshot = self.scraper.page.screenshot(type="jpeg", quality=60)
                    logger.info("✅ Bot iniciado correctamente. Diagnóstico registrado en logs.")
                    self.first_run = False
                
                for page_num in range(1, settings.MAX_PAGES_PER_CYCLE + 1):
                    logger.info(f"📄 Procesando página {page_num}/{settings.MAX_PAGES_PER_CYCLE}...")
                    
                    project_cards = self.scraper.get_project_cards()
                    self._process_cards(project_cards)
                    
                    if page_num < settings.MAX_PAGES_PER_CYCLE:
                        if not self.scraper.go_to_next_page():
                            logger.info("   No hay más páginas en este ciclo.")
                            break
                    else:
                        logger.info("   Fin del ciclo de paginación.")
                
            except Exception as e:
                logger.exception("❌ Error crítico en el ciclo principal.")
                # Aquí se podría añadir lógica para reiniciar el scraper si es necesario
            
            logger.info(f"⏳ Ciclo completado. Esperando {settings.MONITOR_INTERVAL} segundos...")
            time.sleep(settings.MONITOR_INTERVAL)

    def _process_cards(self, cards):
        """Toma una lista de elementos de tarjeta, los procesa y notifica si son nuevos."""
        projects_data = [self.scraper.parse_card(card) for card in cards]

        # Filtra duplicados dentro de la misma página antes de tocar la DB
        seen_pids = set()
        unique_projects_data = []
        for p in projects_data:
            if p and p["pid"] not in seen_pids:
                unique_projects_data.append(p)
                seen_pids.add(p["pid"])

        projects_data = unique_projects_data

        if not projects_data:
            logger.info("   No se encontraron proyectos válidos en la página.")
            return

        all_pids = [p["pid"] for p in projects_data]
        processed_pids = database.get_processed_pids(all_pids)
        new_projects = [p for p in projects_data if p["pid"] not in processed_pids]
        logger.info(f"   Analizando {len(cards)} proyectos. {len(new_projects)} son nuevos.")
        
        projects_to_mark = []
        for project in new_projects:
            full_text = f"{project['raw_title']} {project['desc']} {project['skills']}"
            match = self._check_keywords(full_text)

            if match:
                logger.info(f"✨ MATCH: {project['raw_title'][:30]}... ({match})")
                try:
                    screenshot = project['card_element'].screenshot(type="jpeg", quality=50)
                except:
                    screenshot = None
                payload = {
                    "type": "LEAD", "id": project['pid'], "title": project['raw_title'],
                    "link": project['link'], "match": match, 
                    "budget": project['budget'], "skills": project['skills'],
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                notifier.send_lead_to_n8n(payload, screenshot)
            
            projects_to_mark.append((project['pid'], project['raw_title']))
        
        if projects_to_mark:
            database.mark_batch_as_processed(projects_to_mark)
            
    def _check_keywords(self, text):
        """Comprueba si alguna palabra clave está en el texto."""
        text_lower = text.lower()
        for kw in settings.KEYWORDS:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower):
                return kw
        return None

    def close(self):
        """Detiene los componentes del bot (como el scraper) de forma segura."""
        self.scraper.close_browser()
