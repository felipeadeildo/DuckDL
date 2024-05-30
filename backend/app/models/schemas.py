from typing import List, Optional

from pydantic import BaseModel


class NodeBase(BaseModel):
    name: str
    type: str
    url: Optional[str] = None
    status: Optional[str] = None


class Node(NodeBase):
    id: int
    order: Optional[int] = None
    parent_id: Optional[int] = None
    totalSize: Optional[int] = None
    currentSize: Optional[int] = None
    unit: Optional[str] = None

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    username: str
    password: str
    name: str
    platformId: int


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    extraInfos: str
    products: List[Node] = []

    class Config:
        orm_mode = True
