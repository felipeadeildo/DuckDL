from abc import ABC, abstractmethod
from typing import Callable, Optional

from app.scripts.base.constants import MESSAGE_CONTENTS, MESSAGE_KEYS
from app.scripts.base.session import AsyncSession
from app.services import AccountService, LogService
from bs4 import BeautifulSoup, NavigableString, Tag
from prisma import Prisma
from prisma.models import Account, Setting


class PlatformLogs:
    account: Account
    log_service: LogService

    async def log(self, type: MESSAGE_KEYS, **context):
        level, message = MESSAGE_CONTENTS[type]
        log_fn = getattr(self.log_service, level)
        await log_fn(account_id=self.account.id, message=message.format(**context))


class PlatformDownloader(ABC, PlatformLogs):
    BASE_URL: str
    session: AsyncSession

    def __init__(self, prisma: Prisma, account: Account, settings: list[Setting]):
        self.prisma = prisma
        self.account = account
        self.account_service = AccountService(prisma)
        self.log_service = LogService(prisma)
        self.is_logged = False

        for setting in settings:
            # TODO; Consider the `setting.valueType` before setting the value
            setattr(self, setting.key, setting.value)

    def _create_session(self, use_cloudscraper: bool = False):
        """Create a requests.Session instance to make requests "completely" safe"""
        async_session = AsyncSession()
        if use_cloudscraper:
            from cloudscraper import create_scraper

            self.session = create_scraper(async_session)  # type: ignore
        else:
            self.session = async_session
            # TODO: get a user-agent from a random.choice()
            self.session.headers.update(
                {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
                }
            )

    @abstractmethod
    async def _login(self):
        """Do the login process"""
        pass

    @abstractmethod
    async def start_download(self, node: ...):
        """This will start the download process of the given node (product)"""
        pass

    @abstractmethod
    async def map_product(self, node: ...):
        """This will map all the tree of the given product (node)"""
        pass

    @abstractmethod
    async def _list_products(self):
        """This will list all products with depth of 1 only for select the product to map"""
        pass

    async def list_products(self):
        """
        This will list all products with depth of 1 only for select the product to map
        """
        current_status = await self.account_service.get_account_status(self.account.id)
        if current_status not in ("stopped", "error", "products_listed"):
            await self.log("account_status_block_product_list", status=current_status)
            return

        if current_status == "products_listed":
            await self.account_service.delete_products(self.account.id)
            await self.log("account_products_deleted")

        await self.account_service.set_account_status(
            self.account.id, "listing_products"
        )

        await self.log("account_start_listing_products")

        return await self._list_products()

    async def get_soup(self, method: Callable, url: str, *args, **kwargs):
        res = await method(url, *args, **kwargs)
        return BeautifulSoup(res.content, "html.parser")

    @classmethod
    def valid_tag(cls, tag: Optional[Tag | NavigableString]) -> Optional[Tag]:
        if isinstance(tag, NavigableString) or tag is None:
            return None
        return tag
