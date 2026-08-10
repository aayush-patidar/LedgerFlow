from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings=Settings()