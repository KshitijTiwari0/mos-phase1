# backend/app/api/routers/__init__.py
from fastapi import APIRouter
from app.api.routers.chat import router as chat_router
from app.api.routers.config import router as config_router
from app.api.routers.health import router as health_router
from app.api.routers.leads import router as leads_router
from app.api.routers.reports import router as reports_router
from app.api.routers.scenario import router as scenario_router

# Central multi-router wrapper network assembly
api_router = APIRouter()

# Attach all functional feature modules explicitly
api_router.include_router(health_router)
api_router.include_router(config_router)
api_router.include_router(leads_router)
api_router.include_router(chat_router)
api_router.include_router(reports_router)
api_router.include_router(scenario_router)