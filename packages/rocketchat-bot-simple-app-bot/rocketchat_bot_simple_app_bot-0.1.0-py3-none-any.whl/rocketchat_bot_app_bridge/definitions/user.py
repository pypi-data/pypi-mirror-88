import datetime
from typing import TypedDict, Literal, Dict, List, Any


class IUserEmail(TypedDict):
    address: str
    verified: bool


class IUser(TypedDict, total=False):
    id: str
    username: str
    emails: List[IUserEmail]
    type: Literal['app', 'user', 'bot', 'unknown']
    isEnabled: bool
    name: str
    roles: List[str]
    bio: str
    status: str
    statusConnection: Any
    statusText: str
    utcOffset: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    lastLoginAt: datetime.datetime
    appId: str
    customFields: Dict[str, Any]
