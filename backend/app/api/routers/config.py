from fastapi import APIRouter

from app.schemas.config_schema import BusinessConfigCreate, BusinessConfigResponse
from app.services.config.config_service import ConfigService

router = APIRouter(prefix="/config", tags=["Config"])


@router.post("/create")
def create_config(payload: BusinessConfigCreate):
    return ConfigService.create_config(payload)


@router.get("/{tenant_id}", response_model=BusinessConfigResponse)
def get_config(tenant_id: str):
    return ConfigService.get_config(tenant_id)