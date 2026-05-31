# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import api_router
from app.db.database import engine
from app.db import models

# Initialize and create all SQLite tables on application startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Agent Operating System (MOS) - Phase 1")

# Standard production-ready CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the core assembled endpoint layout network
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "MOS Backend Root Engine Running Securely"}