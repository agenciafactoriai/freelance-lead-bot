# app/notifier.py

import requests
import base64
import time
import logging
from config import settings
from app.utils import fix_encoding

logger = logging.getLogger(__name__)

def send_lead_to_n8n(data: dict, screenshot_bytes: bytes = None):
    """
    Envía los datos de un lead (proyecto encontrado) al webhook de n8n,
    incluyendo opcionalmente una captura de pantalla.
    """
    if not settings.N8N_WEBHOOK_URL:
        logger.warning("N8N_WEBHOOK_URL no configurada. No se enviará el lead.")
        return False

    # Normaliza campos de texto para evitar caracteres rotos en n8n/Gmail
    data = data.copy()
    for key in ("title", "budget", "match", "skills", "message"):
        if key in data:
            data[key] = fix_encoding(data[key])
    
    headers = {"Content-Type": "application/json"}
    if settings.N8N_SECRET_TOKEN:
        headers["X-Webhook-Secret"] = settings.N8N_SECRET_TOKEN

    if screenshot_bytes:
        data["screenshot_b64"] = base64.b64encode(screenshot_bytes).decode('utf-8')

    for attempt in range(3):
        try:
            response = requests.post(settings.N8N_WEBHOOK_URL, json=data, headers=headers, timeout=20)
            if response.status_code == 200:
                title = data.get('title', 'LEAD SIN TITULO')
                logger.info(f"🚀 Lead enviado a n8n: {title[:40]}...")
                return True
            logger.warning(f"⚠️ n8n respondió {response.status_code}. Reintento {attempt+1}/3.")
        except requests.RequestException as e:
            logger.error(f"❌ Error de conexión con n8n: {e}. Reintento {attempt+1}/3.")
        time.sleep(2 ** attempt)
        
    logger.error(f"❌ Fallo final al enviar lead a n8n: {data.get('title', 'LEAD SIN TITULO')}")
    return False

def send_diagnostic_to_n8n(message: str, screenshot_bytes: bytes = None):
    """Envía un mensaje de diagnóstico (ej. arranque del bot) a n8n."""
    payload = {
        "type": "DIAGNOSTIC",
        "message": message,
        "date": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    # Reutilizamos la misma lógica de envío
    send_lead_to_n8n(payload, screenshot_bytes)

