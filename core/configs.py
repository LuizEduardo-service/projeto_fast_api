

from pydantic import  AnyHttpUrl
from typing import Any
from pydantic_settings import BaseSettings
from decouple import config

user = config('USER')
password = config('USER')
port = config('USER')
database = config('USER')

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = f"postgresql+asyncpg://{user}:{password}@localhost:{port}/{database}"

    class Config:
        case_sensitive = True


settings = Settings()