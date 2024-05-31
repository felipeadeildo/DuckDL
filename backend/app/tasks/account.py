import asyncio


from app.prisma import db
from app.scripts import downloaders
from app.tasks import celery_app
from prisma.models import Account, Platform


async def list_account_products(account: dict):
    if not db.is_connected():
        await db.connect()

    platform = Platform(**account["Platform"])
    downloader = downloaders.get(platform.key)
    if not downloader:
        raise ValueError(
            f"Downloader {platform.name} with key {platform.key} not found"
        )

    settings = await db.setting.find_many()
    account.update({"Platform": platform})
    downloader_instance = downloader(db, Account(**account), settings)

    await downloader_instance.list_products()

    await db.disconnect()


@celery_app.task
def list_account_products_task(account: dict):
    asyncio.run(list_account_products(account))
    return []
