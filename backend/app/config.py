from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CoursesDownloader"
    broker_url: str = "redis://localhost:6379/0"
    result_backend: str = "redis://localhost:6379/0"


settings = Settings()
