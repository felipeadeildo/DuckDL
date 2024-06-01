from typing import Literal

from app.models.schemas import AccountCreate, AccountStatus
from prisma import Prisma
from prisma.types import AccountUpdateInput


class AccountService:
    def __init__(self, prisma: Prisma):
        self.prisma = prisma

    async def create_account(self, account: AccountCreate):
        return await self.prisma.account.create(
            {
                "username": account.username,
                "password": account.password,
                "platformId": account.platformId,
                "extraInfos": account.extraInfos,
                "status": "stopped",
            }
        )

    async def update_account(self, account_id: int, account: AccountUpdateInput):
        return await self.prisma.account.update(data=account, where={"id": account_id})

    async def delete_account(self, account_id: int):
        # TODO: Delete products tree
        return await self.prisma.account.delete(where={"id": account_id})

    async def get_account(self, account_id: int):
        return await self.prisma.account.find_unique(
            where={"id": account_id}, include={"Platform": True}
        )

    async def get_accounts(self, query: str):
        return await self.prisma.account.find_many(
            where={"username": {"contains": query}},
            include={"Platform": True},
        )

    async def get_account_status(self, account_id: int) -> str:
        account = await AccountStatus.prisma().find_unique(
            where={"id": account_id},
        )

        if not account:
            raise ValueError(f"Account {account_id} not found")

        return account.status

    async def set_account_status(
        self,
        account_id: int,
        status: Literal[
            "stopped",
            "error",
            "listing_products",
            "products_listed",
            "downloading_products",
        ],
    ):
        account = await self.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        return await self.update_account(account_id, {"status": status})

    async def get_account_products(
        self, account_id: int, query: str, skip: int, take: int
    ):
        account = await self.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        async with self.prisma.tx() as transaction:
            products = await transaction.node.find_many(
                where={
                    "accountId": account_id,
                    "name": {"contains": query},
                    "parentId": None,
                },
                skip=skip,
                take=take,
            )

            count = await transaction.node.count(
                where={
                    "accountId": account_id,
                    "name": {"contains": query},
                    "parentId": None,
                }
            )

        return {"nodes": products, "total": count}

    async def delete_products(self, account_id: int):
        return await self.prisma.node.delete_many(
            where={"accountId": account_id, "parentId": None}
        )
