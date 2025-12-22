# app/database.py

import os
import sqlite3
import logging
from config import settings

logger = logging.getLogger(__name__)

def init_db():
    """Inicializa la base de datos y la tabla de proyectos si no existen."""
    try:
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        with sqlite3.connect(settings.DB_FILE) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, title TEXT, processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        logger.info("✅ Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"❌ Error crítico inicializando la DB: {e}")
        raise

def get_processed_pids(pids: list) -> set:
    """
    Dada una lista de IDs de proyectos, consulta la base de datos y
    devuelve un conjunto (set) con los IDs que ya existen.
    """
    if not pids:
        return set()
    try:
        with sqlite3.connect(settings.DB_FILE) as conn:
            placeholders = ','.join('?' for _ in pids)
            query = f"SELECT id FROM projects WHERE id IN ({placeholders})"
            return {row[0] for row in conn.execute(query, pids)}
    except sqlite3.Error as e:
        logger.error(f"⚠️ Error consultando la DB: {e}")
        return set() # En caso de error, devolvemos un set vacío para no detener el bot

def mark_batch_as_processed(projects: list):
    """Marca una lista de proyectos (tuplas de id, title) como procesados."""
    if not projects:
        return
    try:
        with sqlite3.connect(settings.DB_FILE) as conn:
            conn.executemany("INSERT OR IGNORE INTO projects (id, title) VALUES (?, ?)", projects)
        logger.info(f"💾 Guardados {len(projects)} nuevos proyectos en la DB.")
    except sqlite3.Error as e:
        logger.error(f"⚠️ Error guardando en lote en la DB: {e}")
