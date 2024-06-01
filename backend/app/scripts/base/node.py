import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from app.scripts.base.session import AsyncSession
from app.services.node import NodeService
from prisma import Prisma
from prisma.models import Account, Setting


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
    parent: Optional["Node"]
    children: list["Node"] = []
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
        *,
        id: Optional[int] = None,
        order: Optional[int] = None,
        url: str = "",
        parent: Optional["Node"] = None,
        children: list["Node"] = [],
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
        self.account = account
        self.settings = settings
        self.__id = id

        self.node_service = NodeService(prisma)

    async def flush_node_db(self):
        if getattr(self, "_node", None):
            return
        if self.__id:
            self._node = await self.node_service.get_node(self.__id)
            if not self._node:
                raise ValueError(f"Node with id {self.__id} not found")
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

    @abstractmethod
    async def load_children(self):
        """Load the children of the node"""
        pass
