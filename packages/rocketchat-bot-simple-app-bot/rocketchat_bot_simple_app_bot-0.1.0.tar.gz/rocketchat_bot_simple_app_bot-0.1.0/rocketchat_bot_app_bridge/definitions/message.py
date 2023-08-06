import datetime
from typing import TypedDict, Any

from rocketchat_bot_app_bridge.definitions.room import IRoom
from rocketchat_bot_app_bridge.definitions.user import IUser

# todo: attachments interface

class IMessage(TypedDict, total=False):
    id: str
    threadId: str
    room: IRoom
    sender: IUser
    text: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    editor: IUser
    editedAt: datetime.datetime
    emoji: str
    avatarUrl: str
    alias: str
    file: Any
    attachments: Any
    reactions: Any
    groupable: bool
    parseUrls: bool
