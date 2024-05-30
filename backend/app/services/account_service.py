from app.models.schemas import AccountCreate
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
            }
        )

    async def update_account(self, account_id: int, account: AccountUpdateInput):
        return await self.prisma.account.update(data=account, where={"id": account_id})

    async def delete_account(self, account_id: int):
        # TODO: Delete products tree
        return await self.prisma.account.delete(where={"id": account_id})

    async def get_account(self, account_id: int):
        return await self.prisma.account.find_unique(where={"id": account_id})

    async def get_accounts(self, query: str):
        return await self.prisma.account.find_many(
            where={"username": {"contains": query}},
            include={"Platform": True},
        )
