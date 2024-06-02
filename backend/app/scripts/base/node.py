import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from app.scripts.base.constants import MESSAGE_CONTENTS, MESSAGE_KEYS
from app.scripts.base.session import AsyncSession
from app.scripts.base.utils import get_node_default_params
from app.services.log import LogService
from app.services.node import NodeService
from prisma import Prisma
from prisma.models import Account, Setting
from prisma.models import Node as NodeDB


class NodeLogs(ABC):
    account: Account
    log_service: LogService
    id: int

    async def log(self, type: MESSAGE_KEYS, **context):
        level, message = MESSAGE_CONTENTS[type]
        log_fn = getattr(self.log_service, level)
        await log_fn(
            message=message.format(**context),
            account_id=self.account.id,
            node_id=self.id,
        )


class NodeProperties(NodeLogs):
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
    parent: Optional["Node"]
    children: list["Node"]
    session: AsyncSession

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


class Node(NodeProperties):
    def __init__(
        self,
        name: str,
        type: str,
        session: AsyncSession,
        prisma: Prisma,
        account: Account,
        settings: list[Setting],
        status: str = "stopped",
        *,
        id: Optional[int] = None,
        order: Optional[int] = None,
        url: str = "",
        parent: Optional["Node"] = None,
        **extra_infos,
    ):
        self.name = name
        self.type = type
        self.order = order
        self.status = status
        self.url = url
        self.prisma = prisma
        self.session = session
        self.parent = parent
        self.extra_infos = extra_infos
        self.account = account
        self.settings = settings
        self.id = id or -1
        self.children = []

        self.NODE_DEFAULTS = get_node_default_params(self)
        self.NODE_DEFAULTS.update(parent=self)

        self.node_service = NodeService(prisma)
        self.log_service = LogService(prisma)

    async def flush_node_db(self):
        if getattr(self, "_node", None):
            return
        if self.id > 0:
            self._node = await self.node_service.get_node(self.id)
            if not self._node:
                raise ValueError(f"Node with id {self.id} not found")
        else:
            self._node = await self.node_service.create_node(
                {
                    "name": self.name,
                    "type": self.type,
                    "url": self.url,
                    "order": self.order,
                    "parentId": self.parent.id if self.parent else None,
                    "extraInfos": json.dumps(self.extra_infos),
                    "accountId": self.account.id,
                }
            )

        self.id = self._node.id

    @abstractmethod
    async def download(self):
        """Download the node and the children"""
        pass

    @classmethod
    def create_child(cls, **kwargs):
        return cls(**kwargs)

    async def load_children(self):
        """Load children from db or from the platform

        If children are defined in the db, load them from the db
        Otherwise, load them from the platform
        """
        if self.status in ("mapped", "downloaded", "download_error"):
            children_db = await self.node_service.get_children(self.id)
            if len(children_db) > 0:
                self.__instanciate_children(children_db)
        else:
            await self._load_children()

    def __instanciate_children(self, children_db: list[NodeDB]):
        """Instanciate children from db to avoid loading them from the platform"""
        self.children = []
        for child_db in children_db:
            child_dump = child_db.model_dump()
            child_dump.update(self.NODE_DEFAULTS)
            child = self.create_child(**child_dump)
            self.children.append(child)

    @abstractmethod
    async def _load_children(self):
        """Load the children of the node (this is the real implementation of load children)"""
        pass
