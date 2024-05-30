from fastapi import APIRouter

router = APIRouter()


@router.post("/{node_id}")
async def download_node(node_id: int): ...
