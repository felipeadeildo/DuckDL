from app.models import schemas
from fastapi import APIRouter

router = APIRouter()


@router.post("", response_model=schemas.AccountOut)
def create_new_account(account: schemas.AccountCreate): ...


@router.get("/{account_id}/products", response_model=list[schemas.NodeOut])
def list_account_products(account_id: int): ...


@router.post("/{account_id}/map")
def start_mapping(account_id: int): ...
