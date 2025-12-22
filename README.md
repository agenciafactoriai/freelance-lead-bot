# Workana Bot – Automated Lead Detection & Notification

End-to-end automation system for detecting new opportunities on Workana and securely distributing them across multiple channels using n8n.

## 🚀 What it does
- Monitors Workana projects using Playwright
- Detects relevant leads based on keywords
- Stores results locally
- Sends normalized leads securely to n8n
- Distributes data to Google Sheets, Telegram and Email

## 🧱 Architecture
Python Bot (Docker) → Secure Webhook → n8n → Channels (Sheets / Telegram / Gmail)

## 🔐 Security
- Webhook protected via `X-Webhook-Secret` header
- Sensitive values managed through environment variables
- Server-side validation in n8n before workflow execution

## 🛠️ Tech Stack
- Python
- Playwright
- Docker
- n8n
- Google Sheets API
- Telegram Bot API

## 📂 Project Structure

app/
config/
Dockerfile
main.py
requirements.txt


## ▶️ Execution
The bot runs as a Docker service and executes in configurable cycles.

## 📌 Note
This project is a functional example of an end-to-end automation system focused on lead acquisition.

## n8n Workflow Template

This repository includes a **sanitized n8n workflow template**:

**Path:** `config/N8N/workana-lead-automation.n8n.json`

Purpose:
- Receives leads via secure webhook
- Validates request headers
- Stores data in Google Sheets
- Sends Telegram notifications
- Sends email alerts

This file is safe for public repositories.  
Secrets and credentials must be configured manually in n8n.

## 🧩 Architecture Diagram

```mermaid
flowchart LR
    A[Workana Platform] --> B[Python Bot<br/>(Playwright + Docker)]
    B -->|POST + X-Webhook-Secret| C[Secure Webhook<br/>(n8n)]
    C --> D[Validation & Routing<br/>(n8n)]
    D --> E[Google Sheets]
    D --> F[Telegram]
    D --> G[Email]

