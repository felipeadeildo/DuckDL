from typing import Optional

from prisma import Prisma


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
