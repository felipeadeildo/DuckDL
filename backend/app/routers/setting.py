from app.models.schemas import SettingOut
from fastapi import APIRouter

router = APIRouter()


@router.get("", response_model=list[SettingOut])
async def list_settings():
    return await SettingOut.prisma().find_many()
