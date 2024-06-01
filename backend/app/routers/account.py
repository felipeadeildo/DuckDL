from app.models.pagination import NodePagination
from app.models.schemas import AccountCreate, AccountOut
from app.prisma import db
from app.services import AccountService
from app.tasks.account import list_account_products_task
from fastapi import APIRouter
from prisma.types import AccountUpdateInput

router = APIRouter()


service = AccountService(db)


@router.post("", response_model=AccountOut)
async def create_account(account: AccountCreate):
    return await service.create_account(account)  # type: ignore


@router.get("/{account_id}", response_model=AccountOut)
async def get_account(account_id: int):
    return await service.get_account(account_id)


@router.get("", response_model=list[AccountOut])
async def get_accounts(query: str = ""):
    return await service.get_accounts(query)


@router.put("/{account_id}", response_model=AccountOut)
async def update_account(account_id: int, account: AccountUpdateInput):
    return await service.update_account(account_id, account)


@router.delete("{account_id}", response_model=AccountOut)
async def delete_account(account_id: int):
    return await service.delete_account(account_id)


@router.post("/{account_id}/start_list_products")
async def list_account_products(account_id: int):
    account = await service.get_account(account_id)
    if not account:
        raise ValueError(f"Account {account_id} not found")

    list_account_products_task(account.model_dump_json())
    return "ok"


@router.get("/{account_id}/products", response_model=NodePagination)
async def get_account_products(
    account_id: int, query: str = "", page: int = 1, per_page: int = 10
):
    skip = (page - 1) * per_page
    take = per_page
    return await service.get_account_products(account_id, query, skip, take)
