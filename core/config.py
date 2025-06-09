from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    # Security
    SECRET_KEY: str
    ALGORITHM: str
    

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    DATABASE_URL: str
    DATABASE_ALEMBIC_URL : str

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int
    RATE_LIMIT_PER_HOUR: int

    # CORS
    # CORS_ORIGINS: List[str] # AnyHttpUrl
    # CORS_CREDENTIALS: bool
    # CORS_METHODS: List[str]
    # CORS_HEADERS: List[str]

    # Telegram Bot Token 
    TOKEN : str

    # Max age seconds
    MaxAuth : int 

    # Channel ID 
    Channel : int 


    # @validator("CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    


settings = Settings()