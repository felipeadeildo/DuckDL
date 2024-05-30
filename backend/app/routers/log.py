from app.models import schemas
from fastapi import APIRouter
from prisma.models import Log

router = APIRouter()


@router.get("", response_model=list[schemas.LogOut])
async def list_logs():
    logs = await Log.prisma().find_many()

    return logs
