from abc import ABC, abstractmethod

from app.scripts.base.constants import MESSAGE_CONTENTS, MESSAGE_KEYS
from app.scripts.base.session import AsyncSession
from app.scripts.base.utils import get_node_default_params
from app.scripts.node import nodes
from app.services import AccountService, LogService
from prisma import Prisma
from prisma.models import Account, Node, Setting


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
        self.settings = settings
        # TODO: Implements the `use_cloudscraper` condition call
        self._create_session()
        self.NODE_DEFAULTS = get_node_default_params(self)

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

    async def login(self):
        if self.is_logged:
            return
        await self._login()
        self.NODE_DEFAULTS.update(session=self.session)

    @abstractmethod
    async def _login(self):
        """Do the login process"""
        pass

    async def start_download(self, node: Node):
        """This will start the download process of the given node (product)"""
        current_status = node.status
        if current_status not in ("stopped", "downloaded", "download_error", "mapped"):
            return await self.log("node_status_block_download", status=current_status)

        await self.login()

        key = node.Account.Platform.key  # type: ignore [account > platform > key isnt None]

        node_class = nodes.get(key)
        if node_class is None:
            return await self.log("node_class_not_found", key=key)

        node_dump = node.model_dump()
        node_dump.update(self.NODE_DEFAULTS)

        node_instance = node_class(**node_dump)
        await node_instance.download()

    @abstractmethod
    async def map_product(self, node: Node):
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

        await self.login()
        return await self._list_products()
