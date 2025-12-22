# main.py

import logging
from app.bot import WorkanaBot # Importa la clase principal desde su nuevo hogar

# --- CONFIGURACIÓN DE LOGS ---
# Es importante que esto esté aquí, al inicio de la ejecución, para que todos
# los módulos que importemos usen esta misma configuración de logging.
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    # El punto de entrada ahora es muy claro:
    # 1. Crea una instancia del bot.
    # 2. La ejecuta.
    # 3. Se asegura de que se cierre correctamente.
    
    bot = WorkanaBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        logging.info("🛑 Detectado Ctrl+C. Apagado iniciado por el usuario.")
    finally:
        bot.close()
