from prisma import Prisma
from prisma.types import NodeCreateInput


class NodeService:
    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    async def create_node(self, node: NodeCreateInput):
        return await self.prisma.node.create(data=node)

    async def get_node(self, node_id: int):
        return await self.prisma.node.find_unique(where={"id": node_id})
