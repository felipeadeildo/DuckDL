from app.models.schemas import PlatformCreate
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Course Downloader App"
    huey_filename: str = "_tasks.db"

    downloaders: list[PlatformCreate] = [
        PlatformCreate(name="Alura", url="alura.com.br", version=1.0, key="alura"),
    ]


settings = Settings()
