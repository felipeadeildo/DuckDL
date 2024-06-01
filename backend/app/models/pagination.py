from typing import List

from app.models.schemas import LogOut, NodeOut
from pydantic import BaseModel


class NodePagination(BaseModel):
    total: int
    nodes: List[NodeOut]


class LogPagination(BaseModel):
    total: int
    data: list[LogOut]
