# Workana Bot – Automated Lead Detection & Notification

Sistema automatizado para la detección de oportunidades en Workana y su distribución segura a distintos canales mediante n8n.

## 🚀 Qué hace
- Monitoriza proyectos en Workana usando Playwright
- Detecta nuevos leads relevantes por keywords
- Persiste resultados en base de datos local
- Envía leads de forma segura a n8n
- Distribuye a Google Sheets, Telegram y Email

## 🧱 Arquitectura
Bot Python (Docker) → Webhook seguro → n8n → Canales (Sheets / Telegram / Gmail)

## 🔐 Seguridad
- Webhook protegido con header `X-Webhook-Secret`
- Variables sensibles gestionadas por entorno (no hardcoded)
- Validación en n8n antes de ejecutar flujos

## 🛠️ Stack
- Python
- Playwright
- Docker
- n8n
- Google Sheets API
- Telegram Bot API

## 📂 Estructura:
app/
config/
Dockerfile
main.py
requirements.txt

## ▶️ Ejecución
El bot se ejecuta como servicio Docker y funciona en ciclos configurables.

## 📌 Nota
Este proyecto es un ejemplo funcional de automatización end-to-end orientada a captación de leads.

