# Imagen oficial de Playwright con Chromium
FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

# Directorio de trabajo
WORKDIR /app

# Copiamos requirements e instalamos dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalamos navegadores necesarios
RUN playwright install --with-deps chromium

# Copiamos el resto del código
COPY . .

# Crear carpeta de datos y asignar permisos
RUN mkdir -p /app/data && chown -R pwuser:pwuser /app

# Variables recomendadas
ENV PYTHONUNBUFFERED=1

# Ejecutar como usuario no-root
USER pwuser

# Comando de arranque
CMD ["python", "main.py"]
