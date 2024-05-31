import json

import dramatiq
from app.prisma import db
from app.scripts import downloaders
from prisma.models import Account, Platform


@dramatiq.actor
async def list_account_products_task(account_raw: str):
    account = json.loads(account_raw)
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
