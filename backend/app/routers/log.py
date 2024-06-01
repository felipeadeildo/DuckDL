from typing import Optional

from app.models.pagination import LogPagination
from app.prisma import db
from app.services.log import LogService
from fastapi import APIRouter

router = APIRouter()

service = LogService(db)


@router.get("", response_model=LogPagination)
async def list_logs(
    account_id: Optional[int] = None, page: int = 1, per_page: int = 30
):
    skip = (page - 1) * per_page
    take = per_page
    return await service.get_logs(account_id, skip, take)
