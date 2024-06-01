from typing import Mapping

from app.scripts.platform.alura import AluraDownloader
from app.scripts.base.platform import PlatformDownloader

downloaders: Mapping[str, type[PlatformDownloader]] = {
    "alura": AluraDownloader,
}
