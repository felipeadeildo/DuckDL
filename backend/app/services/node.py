from typing import Literal

from prisma import Prisma
from prisma.types import NodeCreateInput


class NodeService:
    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    async def create_node(self, node: NodeCreateInput):
        return await self.prisma.node.create(data=node)

    async def get_node(self, node_id: int):
        return await self.prisma.node.find_unique(
            where={"id": node_id}, include={"Account": {"include": {"Platform": True}}}
        )

    async def set_node_status(
        self,
        node_id: int,
        status: Literal[
            "stopped",
            "downloaded",
            "downloading",
            "download_error",
            "mapping_error",
            "mapping",
            "mapped",
        ],
    ):
        return await self.prisma.node.update(
            where={"id": node_id},
            data={"status": status},
        )
