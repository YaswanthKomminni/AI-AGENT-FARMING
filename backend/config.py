"""
FarmWise AI — Central Configuration
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("/etc/secrets/.env", ".env", ".env.example"),  # support Render secrets location
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # IBM Watsonx
    ibm_watsonx_api_key: str = ""
    ibm_watsonx_project_id: str = ""
    ibm_watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    ibm_granite_model_id: str = "ibm/granite-13b-chat-v2"

    # Vector DB
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "farming_knowledge"

    # Weather
    weather_api_base_url: str = "https://api.open-meteo.com/v1"

    # Mandi
    mandi_api_key: str = ""
    mandi_api_base_url: str = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    # App
    app_env: str = "development"
    app_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    log_level: str = "INFO"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
