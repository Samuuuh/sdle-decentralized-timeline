from __future__ import annotations
from typing import Tuple, TypedDict, TYPE_CHECKING

import asyncio

from src.connection.message.message import MessageInterface, MessageType

if TYPE_CHECKING:
    from src.connection.message.message import MessageHeader
    from src.connection.dispatcher import MessageDispatcher
    from src.api.user import User, UserData

class RequestPostMessage(TypedDict):
    header: MessageHeader

class RequestPostType(MessageInterface):
    def __init__(self, user : User, sender : MessageDispatcher) -> None:
        super().__init__(user, sender)

    def build(self, followed_user : str) -> Tuple[UserData, RequestPostMessage]:
        username = self.user.username
        followed_info = self.user.get_user(followed_user)

        message = {
            'header': {
                'user': username,
                'followed' : followed_user,
                'type': MessageType.REQUEST_POSTS.value
            },
        }

        return (followed_info, message)

    def send(self, followed_info, msg):
        try:
            asyncio.run(self.sender.publish_one(followed_info, msg))
        except Exception as e:
            print(e)