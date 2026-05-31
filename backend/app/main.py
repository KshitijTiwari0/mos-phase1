# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import api_router
from app.db.database import engine
from app.db import models

# Application startup par saare SQLite tables ko generate karna
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Agent Operating System (MOS) - Phase 1")

# Clean CORS Policy - Allows ALL Origins, Methods, and Headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Saare domains/origins ko explicitly allow karta hai
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS saare standard methods allow karta hai
    allow_headers=["*"],  # Content-Type, Authorization saare headers allow karta hai
)

# Core API router network assignment loading
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "MOS Backend Root Engine Running Securely"}