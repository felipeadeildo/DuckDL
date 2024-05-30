from app.models.schemas import PlatformOut
from fastapi import APIRouter

router = APIRouter()


@router.get("", response_model=list[PlatformOut])
async def list_platforms():
    return await PlatformOut.prisma().find_many()
