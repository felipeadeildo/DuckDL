from app.prisma import db
from app.scripts.platform import downloaders
from app.services.account import AccountService
from app.services.node import NodeService
from app.tasks import huey_app, run_async_task


@huey_app.task()
@run_async_task
async def list_account_products_task(account_id: int):
    if not db.is_connected():
        await db.connect()

    account = await AccountService(db).get_account(account_id)

    if account is None:
        raise ValueError(f"Account {account_id} not found")

    platform = account.Platform
    if not platform:
        raise ValueError("Account query must includes a platform")
    downloader = downloaders.get(platform.key)
    if not downloader:
        raise ValueError(
            f"Downloader {platform.name} with key {platform.key} not found"
        )

    settings = await db.setting.find_many()
    downloader_instance = downloader(db, account, settings)

    await downloader_instance.list_products()

    await db.disconnect()


@huey_app.task()
@run_async_task
async def download_product_task(product_id: int):
    if not db.is_connected():
        await db.connect()

    settings = await db.setting.find_many()
    product = await NodeService(db).get_node(product_id)

    if not product:
        raise ValueError(f"Product {product_id} not found")

    account = product.Account
    if not account:
        raise ValueError("Account must be included in the product query")

    platform = account.Platform
    if not platform:
        raise ValueError("Account query must includes a platform")

    downloader = downloaders.get(platform.key)
    if not downloader:
        raise ValueError(
            f"Downloader {platform.name} with key {platform.key} not found"
        )

    downloader_instance = downloader(db, account, settings)

    await downloader_instance.start_download(product)

    await db.disconnect()
