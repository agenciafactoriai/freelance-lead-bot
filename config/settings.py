# config/settings.py

import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# --- Configuración de Conexiones ---
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
N8N_SECRET_TOKEN = os.getenv("N8N_SECRET_TOKEN")
WORKANA_URL = os.getenv("WORKANA_URL", "https://www.workana.com/jobs?language=es")

# --- Configuración de Comportamiento del Bot ---
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", 300))
MAX_PAGES_PER_CYCLE = int(os.getenv("MAX_PAGES_PER_CYCLE", 5))

# --- Rutas de Archivos y Base de Datos ---
# __file__ se refiere a este archivo (settings.py)
# os.path.dirname(__file__) es la carpeta 'config'
# os.path.dirname(os.path.dirname(...)) es la carpeta raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_FILE = os.path.join(DATA_DIR, "workana_projects.db")

# --- Constantes de Scraping ---
KEYWORDS = [
    "Automatización", "Automatizacion", "Automation", "Automations", "Integración", 
    "Integracion", "Integration", "API", "Webhook", "n8n", "Make.com", "Zapier", 
    "Power Automate", "RPA", "UiPath", "IA", "Inteligencia Artificial", 
    "Machine Learning", "OpenAI", "GPT", "ChatGPT", "Claude", "Gemini", "LLM", 
    "Chatbot", "BotPress", "Voiceflow", "ManyChat", "Python", "Scraping"
]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]
SELECTORS = {
    "project_card": ".project-item",
    "title_link": "h2 a",
    "description": ".expander, p.description",
    "skills": ".skills",
    "budget": ".values",
    "next_button": "a[rel='next']",
}
