import asyncio
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Optional

import requests
from app.services import AccountService, LogService
from app.services.node import NodeService
from bs4 import BeautifulSoup, NavigableString, Tag
from prisma import Prisma
from prisma.models import Account, Setting


class PlatformDownloader(ABC):
    BASE_URL: str
    session: requests.Session

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
        if use_cloudscraper:
            from cloudscraper import create_scraper

            self.session = create_scraper()
        else:
            self.session = requests.Session()
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
    async def list_products(self):
        """This will list all products with depth of 1 only for select the product to map"""
        pass

    def get_soup(self, method: Callable, url: str, *args, **kwargs):
        res = method(url, *args, **kwargs)
        return BeautifulSoup(res.content, "html.parser")

    @classmethod
    def valid_tag(cls, tag: Optional[Tag | NavigableString]) -> Optional[Tag]:
        if isinstance(tag, NavigableString) or tag is None:
            return None
        return tag


class NodeProperties(ABC):
    id: int
    name: str
    type: str
    url: str
    status: str
    order: Optional[int]
    parent_id: int
    total_size: int
    current_size: int
    unit: str
    extra_infos: dict
    custom_name: Optional[str]
    parent: Optional["NodeBase"]
    children: list["NodeBase"] = []
    session: requests.Session

    @property
    def formatted_name(self) -> str:
        if self.custom_name:
            return self.custom_name

        # TODO: Sanitize the name; remove special characters
        if self.order:
            return f"{self.order}. {self.name}"
        else:
            return self.name

    @property
    def height(self) -> int:
        return 0 if not self.parent else self.parent.height + 1

    @property
    def path(self) -> Path:
        path = (
            self.parent.path / self.formatted_name
            if self.parent
            else Path("Cursos") / self.formatted_name
        )
        # TODO: Identify when its a leaf node, beacause probabily we not will create folders for leaf nodes, just files;
        path.mkdir(parents=True, exist_ok=True)

        return path


class NodeBase(NodeProperties):
    def __init__(
        self,
        name: str,
        type: str,
        session: requests.Session,
        prisma: Prisma,
        *,
        id: Optional[int] = None,
        order: Optional[int] = None,
        url: str = "",
        parent: Optional["NodeBase"] = None,
        children: list["NodeBase"] = [],
        **extra_infos,
    ):
        self.name = name
        self.type = type
        self.order = order
        self.url = url
        self.prisma = prisma
        self.session = session
        self.parent = parent
        self.children = children
        self.extra_infos = extra_infos

        self.node_service = NodeService(prisma)

        if asyncio.get_event_loop().is_running():
            asyncio.create_task(self._load_node_db(id))
        else:
            asyncio.run(self._load_node_db(id))

    async def _load_node_db(self, node_id: Optional[int]):
        if node_id:
            self._node = await self.node_service.get_node(node_id)
            if not self._node:
                raise ValueError(f"Node with id {node_id} not found")
            else:
                self.id = self._node.id
        else:
            self._node = await self.node_service.create_node(
                {
                    "name": self.name,
                    "type": self.type,
                    "url": self.url,
                    "order": self.order,
                    "parentId": self.parent.id if self.parent else None,
                    "extraInfos": json.dumps(self.extra_infos),
                }
            )

    @abstractmethod
    async def download(self):
        """Download the node and the children"""
        pass

    @abstractmethod
    async def load_children(self):
        """Load the children of the node"""
        pass
