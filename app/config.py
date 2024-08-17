from pydantic import BaseSettings

class Settings(BaseSettings):
    sqlite_uri: str
    sqlite_db: str
    sqlite_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()