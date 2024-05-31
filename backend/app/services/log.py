from typing import Optional

from prisma import Prisma
from prisma.types import LogWhereInput


class LogService:
    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    async def __log(
        self,
        level: str,
        message: str,
        node_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ):
        return await self.prisma.log.create(
            data={
                "message": message,
                "logLevel": level.upper(),
                "nodeId": node_id,
                "accountId": account_id,
            }
        )

    async def log(
        self,
        message: str,
        node_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ):
        return await self.__log(
            level="log", message=message, node_id=node_id, account_id=account_id
        )

    async def info(
        self,
        message: str,
        node_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ):
        return await self.__log(
            level="info", message=message, node_id=node_id, account_id=account_id
        )

    async def warning(
        self,
        message: str,
        node_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ):
        return await self.__log(
            level="warning", message=message, node_id=node_id, account_id=account_id
        )

    async def debug(
        self,
        message: str,
        node_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ):
        return await self.__log(
            level="debug", message=message, node_id=node_id, account_id=account_id
        )

    async def error(
        self,
        message: str,
        node_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ):
        return await self.__log(
            level="error", message=message, node_id=node_id, account_id=account_id
        )

    async def get_logs(
        self, account_id: Optional[int] = None, skip: int = 0, take: int = 30
    ):
        query: Optional[LogWhereInput] = (
            None if account_id is None else {"accountId": account_id}
        )

        async with self.prisma.tx() as transaction:
            result = await transaction.log.find_many(
                skip=skip,
                take=take,
                where=query,
                include={"Account": {"include": {"Platform": True}}, "Node": True},
                order={"id": "desc"},
            )

            count = await transaction.log.count(where=query)

        return {"data": result, "total": count}
