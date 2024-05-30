from app.models.schemas import PlatformCreate
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Course Downloader App"
    broker_url: str = "amqp://guest:guest@rabbitmq//"
    result_backend: str = "rcp://"

    downloaders: list[PlatformCreate] = [
        PlatformCreate(name="Youtube", url="youtube.com", version=1.0),
    ]


settings = Settings()
