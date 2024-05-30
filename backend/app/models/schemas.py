from datetime import datetime
from typing import List, Optional

from prisma.bases import BaseAccount, BaseLog, BaseNode, BasePlatform, BaseSetting

# TODO: Split into different files;


# Modelos Account
class AccountCreate(BaseAccount):
    username: str
    password: str
    name: str
    platformId: int
    extraInfos: Optional[str] = None


class AccountUpdate(BaseAccount):
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    platformId: Optional[int] = None
    extraInfos: Optional[str] = None


class AccountOut(BaseAccount):
    id: int
    username: str
    password: str
    name: str
    platformId: int
    extraInfos: str
    products: List["NodeOut"] = []

    class Config:
        from_attributes = True


# Modelos Platform
class PlatformCreate(BasePlatform):
    name: str
    url: str
    version: float


class PlatformUpdate(BasePlatform):
    name: Optional[str] = None
    url: Optional[str] = None


class PlatformOut(BasePlatform):
    id: int
    name: str
    url: str
    version: float

    class Config:
        from_attributes = True


# Modelos Log
class LogCreate(BaseLog):
    message: str
    logLevel: str
    nodeId: Optional[int] = None
    accountId: Optional[int] = None


class LogUpdate(BaseLog):
    message: Optional[str] = None
    logLevel: Optional[str] = None
    nodeId: Optional[int] = None
    accountId: Optional[int] = None


class LogOut(BaseLog):
    id: int
    message: str
    logLevel: str
    dateTime: datetime
    nodeId: Optional[int] = None
    accountId: Optional[int] = None
    Node: Optional["NodeOut"] = None
    Account: Optional["AccountOut"] = None

    class Config:
        from_attributes = True


# Modelos Node
class NodeCreate(BaseNode):
    name: str
    type: str
    url: Optional[str] = None
    status: Optional[str] = None
    order: Optional[int] = None
    parentId: Optional[int] = None
    totalSize: Optional[int] = None
    currentSize: Optional[int] = None
    unit: Optional[str] = None
    extraInfos: str
    customName: Optional[str] = None


class NodeUpdate(BaseNode):
    name: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None
    order: Optional[int] = None
    parentId: Optional[int] = None
    totalSize: Optional[int] = None
    currentSize: Optional[int] = None
    unit: Optional[str] = None
    extraInfos: Optional[str] = None
    customName: Optional[str] = None


class NodeOut(BaseNode):
    id: int
    name: str
    type: str
    url: Optional[str] = None
    status: Optional[str] = None
    order: Optional[int] = None
    parentId: Optional[int] = None
    totalSize: Optional[int] = None
    currentSize: Optional[int] = None
    unit: Optional[str] = None
    extraInfos: str
    customName: Optional[str] = None
    children: List["NodeOut"] = []

    class Config:
        from_attributes = True


# Modelos Setting
class SettingCreate(BaseSetting):
    key: str
    value: str
    valueType: str


class SettingUpdate(BaseSetting):
    key: Optional[str] = None
    value: Optional[str] = None
    valueType: Optional[str] = None


class SettingOut(BaseSetting):
    id: int
    key: str
    value: str
    valueType: str

    class Config:
        from_attributes = True
