from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_PORT: int = Field(..., env="DB_PORT")
    
    OAUTH_SECRET_KEY: str = Field(..., env="OAUTH_SECRET_KEY")
    OAUTH_ALGORITHM: str = Field(..., env="OAUTH_ALGORITHM")
    OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., env="OAUTH_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()