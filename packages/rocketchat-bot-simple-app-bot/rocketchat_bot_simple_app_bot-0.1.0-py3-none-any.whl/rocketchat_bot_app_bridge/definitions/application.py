from typing import TypedDict, Union, Literal, List, NewType, Optional

from rocketchat_bot_app_bridge.definitions.message import IMessage
from rocketchat_bot_app_bridge.definitions.user import IUser


class IButton(TypedDict):
    text: str
    action: str
    style: Optional[Literal['primary', 'danger']]


class IFromBackendRequestSendMessage(TypedDict):
    message: IMessage
    buttons: List[IButton]


class IToBackendButtonClick(TypedDict):
    action: str
    message: IMessage
    user: IUser


EventType = NewType('EventType', Literal['message_from_backend', 'new_message'])


class IBackendRequest(TypedDict):
    event: EventType
    bot: IUser
    payload: Union[IFromBackendRequestSendMessage, IMessage, IToBackendButtonClick]
