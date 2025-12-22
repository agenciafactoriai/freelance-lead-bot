# app/utils.py
import logging

logger = logging.getLogger(__name__)

def get_stealth_runner():
    """Intenta importar y devolver la función stealth_sync."""
    try:
        from playwright_stealth import stealth_sync
        logger.info("✅ Stealth cargado correctamente.")
        return stealth_sync
    except ImportError as e:
        logger.warning(f"⚠️ No se pudo cargar playwright-stealth: {e}. Usando modo SIN Stealth.")
        def dummy_stealth(page): pass
        return dummy_stealth

def fix_encoding(text: str) -> str:
    """Corrige problemas de doble codificación (latin1 -> utf-8)."""
    if not text or not isinstance(text, str):
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text
