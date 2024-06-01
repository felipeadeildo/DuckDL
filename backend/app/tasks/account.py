import json

from app.prisma import db
from app.scripts import downloaders
from app.tasks import huey_app, run_async_task
from prisma.models import Account, Platform


@huey_app.task()
@run_async_task
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

    return True
