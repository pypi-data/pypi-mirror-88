import datetime
from typing import TypedDict, Literal, Dict, Type, List, Any

from rocketchat_bot_app_bridge.definitions.user import IUser


class RoomType:
    CHANNEL = "c",
    PRIVATE_GROUP = "p",
    DIRECT_MESSAGE = "d",
    LIVE_CHAT = "l"


class IRoom(TypedDict, total=False):
    id: str
    displayName: str
    slugifiedName: str
    type: RoomType
    creator: IUser
    userIds: List[str]
    isDefault: bool
    isReadOnly: bool
    displaySystemMessages: bool
    messageCount: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    lastModifiedAt: datetime.datetime
    customFields: Dict[str, Any]
    parentRoom: Type[Literal['IRoom']]
    livechatData: Any
