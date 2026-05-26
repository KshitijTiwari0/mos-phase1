from app.schemas.agent_schema import BusinessConfig


class BusinessConfigCreate(BusinessConfig):
    """API DTO for creating a tenant business config.

    Inherits every field from the canonical BusinessConfig used by agents,
    and adds the tenant identifier. Keeping a single base prevents config
    drift between the API surface and what the agents actually consume.
    """

    tenant_id: str


class BusinessConfigResponse(BusinessConfigCreate):
    """Full read-model returned by GET /config/{tenant_id}."""

    pass
