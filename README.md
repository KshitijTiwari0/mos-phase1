# README.md

# MOS Phase 1

MOS (Multi-Agent Operating System) is a configurable AI workforce system for businesses.

The system is designed to:

* analyze incoming leads
* generate sales conversations
* provide support workflows
* detect conversational patterns
* generate reports and business insights

---

# Phase 1 Goal

The Phase 1 demo focuses on:

```text
Business Config
→ Lead Submission
→ Analytics AI
→ Sales AI
→ Conversation Logging
→ Manager Summary
```

This phase is intended to validate:

* multi-agent orchestration
* business-config-driven behavior
* modular architecture
* reusable AI workflows

---

# Tech Stack

## Backend

* Python
* FastAPI
* Pydantic

## Frontend

* React + Vite

## AI

* OpenRouter / OpenAI-compatible APIs

## Database

* SQLite (temporary Phase 1 setup)

## Future Additions

* PostgreSQL
* Redis
* Docker
* Celery
* n8n integrations

---

# Project Structure

```text
mos-phase1/

  backend/
    app/
      api/
      agents/
      services/
      db/
      prompts/
      workers/
      main.py

  frontend/

  workflows/
    n8n/

  docs/
    architecture/
    contracts/
    stories/
    MASTER_REFERENCE.md
```

---

# Prerequisites

Install the following before setup:

## Required

* Git
* Python 3.11+
* Node.js LTS
* VS Code
* GitHub Desktop

## Recommended

* Postman
* SQLite Viewer extension
* Thunder Client extension

---

# Local Setup Instructions

# 1. Clone Repository

```bash
git clone <your-repo-url>
cd mos-phase1
```

---

# 2. Backend Setup

## Navigate to backend

```bash
cd backend
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

---

## Activate Virtual Environment

### Windows CMD

```bash
.venv\Scripts\activate
```

### Windows PowerShell

```bash
.venv\Scripts\Activate.ps1
```

---

## Install Backend Dependencies

```bash
pip install fastapi uvicorn openai pydantic python-dotenv sqlalchemy
```

---

## Save Requirements

```bash
pip freeze > requirements.txt
```

---

# 3. Create Backend Entry File

Create:

```text
backend/app/main.py
```

Add:

```python
from fastapi import FastAPI

app = FastAPI(title="MOS Phase 1 API")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mos-phase1-backend"
    }
```

---

# 4. Run Backend

From `backend/` directory:

```bash
uvicorn app.main:app --reload
```

---

# 5. Test Backend

Open browser:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "mos-phase1-backend"
}
```

---

# 6. Frontend Setup

Open new terminal.

Navigate to frontend:

```bash
cd frontend
```

---

## Create React App

```bash
npm create vite@latest . -- --template react
```

---

## Install Frontend Dependencies

```bash
npm install
```

---

## Run Frontend

```bash
npm run dev
```

Frontend should run on:

```text
http://localhost:5173
```

---

# 7. Environment Variables

Create:

```text
backend/.env
```

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

---

# 8. Documentation Setup

Important project documents are inside:

```text
docs/
```

## Most Important Document

```text
docs/MASTER_REFERENCE.md
```

This document is the project's:

* architecture reference
* workflow reference
* contract reference
* onboarding reference

All implementation must follow this document.

---

# Development Workflow

## Important Rules

### 1. Follow Contracts

Do not change:

* API contracts
* agent schemas
* orchestrator flow

without updating documentation.

---

### 2. Modular Architecture

Each module should remain isolated.

Example:

* agents should not directly manipulate frontend
* services should not tightly couple

---

### 3. Config-Driven Logic

Do NOT hardcode business-specific behavior.

Use:

* configs
* prompts
* business settings

instead.

---

# Current Phase 1 Scope

## Included

* Business Config
* Lead Submission
* Analytics AI
* Sales AI
* Logging
* Manager Summary

---

## Excluded

* Live WhatsApp integration
* Calling systems
* Enterprise deployment
* Autonomous learning
* Production infra

---

# Initial Development Order

## Step 1

Backend health route

## Step 2

Business Config APIs

## Step 3

Lead Submission API

## Step 4

Orchestrator Service

## Step 5

Analytics AI

## Step 6

Sales AI

## Step 7

Conversation Logging

## Step 8

Manager Summary

---

# Useful Commands

## Backend

Run backend:

```bash
uvicorn app.main:app --reload
```

Install dependency:

```bash
pip install package_name
```

Save dependencies:

```bash
pip freeze > requirements.txt
```

---

## Frontend

Run frontend:

```bash
npm run dev
```

Install package:

```bash
npm install package_name
```

---

# Notes

This project currently prioritizes:

* workflow validation
* architecture quality
* modularity
* AI orchestration

over:

* production infrastructure
* containerization
* scaling

These will be added later after the core system is validated.

---

# Future Infrastructure

Planned additions:

* PostgreSQL
* Redis
* Docker
* Celery
* n8n workflows
* deployment pipeline
* CI/CD
* monitoring
