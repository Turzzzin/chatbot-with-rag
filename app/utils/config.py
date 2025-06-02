import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    EMBEDDINGS_MODEL: str = "all-MiniLM-L6-v2"
    CHROMA_DB_PATH: str = "app/data/vectorstores/medicacoes_db"
    PPLX_API_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
