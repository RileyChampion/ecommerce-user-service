from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App settings
    PROJECT_NAME: str = "User Service API"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"


# Instantiate the settings object
settings = Settings()
