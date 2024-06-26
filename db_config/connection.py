from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):

    DATABASE_URL: Optional[str] = None
    TEST_DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = None
    ACCESS_TOKEN_EXPIRE_SECONDS: int = None
    BUCKET_URL: str = None
    BUCKET_NAME: str = None
    GOOGLE_APPLICATION_CREDENTIALS: str = None

    def get_db_url(self):
        return self.DATABASE_URL

    class Config:
        env_file = ".env"


settings = Settings()
