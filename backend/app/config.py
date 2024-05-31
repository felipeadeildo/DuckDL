from app.models.schemas import PlatformCreate
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Course Downloader App"
    broker_url: str = "amqp://guest:guest@localhost:5672//"
    result_backend: str = "rpc://"

    downloaders: list[PlatformCreate] = [
        PlatformCreate(name="Alura", url="alura.com.br", version=1.0, key="alura"),
    ]


settings = Settings()
