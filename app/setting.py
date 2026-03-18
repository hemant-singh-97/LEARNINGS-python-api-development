from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_PORT: int = Field(..., env="DB_PORT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()