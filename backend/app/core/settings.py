from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MOS Phase 1 Backend"
    database_url: str = "sqlite:///./mos_phase1.db"
    llm_provider: str = "gemini"

    class Config:
        env_file = ".env"


settings = Settings()