from fastapi import FastAPI

from app.api.routers import health, config, leads, chat, reports, scenario

app = FastAPI(
    title="MOS Phase 1 Backend",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(config.router)
app.include_router(leads.router)
app.include_router(chat.router)
app.include_router(reports.router)
app.include_router(scenario.router)