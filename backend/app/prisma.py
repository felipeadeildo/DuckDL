from app.config import settings
from prisma import Prisma
from prisma.models import Log, Platform

db = Prisma(auto_register=True)


async def startup():
    await db.connect()

    await Log.prisma().create(
        {
            "message": "Inicia aplicação e base de dados",
            "logLevel": "INFO",
        }
    )

    for platform_downloder in settings.downloaders:
        downloader = await Platform.prisma().find_first(
            where={
                "key": platform_downloder.key,
            }
        )

        if not downloader:
            await Platform.prisma().create(
                {
                    "name": platform_downloder.name,
                    "url": platform_downloder.url,
                    "version": platform_downloder.version,
                    "key": platform_downloder.key,
                }
            )
        else:
            if downloader.version != platform_downloder.version:
                await Platform.prisma().update(
                    where={
                        "id": downloader.id,
                    },
                    data={
                        "version": platform_downloder.version,
                        "name": platform_downloder.name,
                        "url": platform_downloder.url,
                    },
                )


async def shutdown():
    await db.disconnect()
