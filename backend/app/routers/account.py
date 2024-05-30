from app.models import schemas
from fastapi import APIRouter

router = APIRouter()


@router.post("/accounts/", response_model=schemas.Account)
def create_new_account(account: schemas.AccountCreate): ...


@router.get("/accounts/{account_id}/products", response_model=schemas.Account)
def list_account_products(account_id: int): ...


@router.post("/accounts/{account_id}/map")
def start_mapping(account_id: int): ...
