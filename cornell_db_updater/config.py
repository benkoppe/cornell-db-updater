from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CORNELL_API_HOST: str
    CORNELL_API_VERSION: str

    class Config:
        env_file = ".env"


settings = Settings()
