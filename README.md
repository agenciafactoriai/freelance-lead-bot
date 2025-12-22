# Workana Bot – Automated Lead Detection & Notification

## 💼 Business Overview

Many professionals and agencies miss valuable opportunities on Workana due to manual monitoring, delayed responses, or lack of structured lead management.

This system automates the entire process:
- Detects new projects in real time
- Filters only relevant opportunities
- Centralizes leads in one place
- Notifies instantly through preferred channels

The result: **faster response times, better lead visibility, and higher conversion potential**.

## 🎯 Who is this for?

This solution is designed for:
- Freelancers managing multiple platforms
- Agencies sourcing projects at scale
- Consultants who rely on fast lead response
- Teams that want visibility without manual effort


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
    A[Workana Platform]
    B[Python Bot\nPlaywright + Docker]
    C[Secure Webhook\nn8n]
    D[Validation & Routing\nn8n]
    E[Google Sheets]
    F[Telegram]
    G[Email]

    A --> B
    B -->|POST + X-Webhook-Secret| C
    C --> D
    D --> E
    D --> F
    D --> G

