from typing import Optional

from app.models.schemas import LogOut
from app.prisma import db
from app.services.log import LogService
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

service = LogService(db)


class LogPagination(BaseModel):
    total: int
    data: list[LogOut]


@router.get("", response_model=LogPagination)
async def list_logs(
    account_id: Optional[int] = None, page: int = 1, per_page: int = 30
):
    skip = (page - 1) * per_page
    take = per_page
    return await service.get_logs(account_id, skip, take)
