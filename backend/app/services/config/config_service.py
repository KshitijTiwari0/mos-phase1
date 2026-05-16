from app.schemas.config_schema import BusinessConfigCreate


class ConfigService:
    @staticmethod
    def create_config(payload: BusinessConfigCreate):
        # TODO: persist config using ConfigRepository
        return {
            "success": True,
            "tenant_id": payload.tenant_id
        }

    @staticmethod
    def get_config(tenant_id: str):
        # TODO: fetch config using ConfigRepository
        return {
            "tenant_id": tenant_id,
            "business_name": "Demo Business",
            "industry": "Education"
        }