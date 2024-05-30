from app.models.schemas import LogOut
from fastapi import APIRouter

router = APIRouter()


@router.get("", response_model=list[LogOut])
async def list_logs():
    return await LogOut.prisma().find_many()
