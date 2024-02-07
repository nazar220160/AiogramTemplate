import io
from typing import List, Optional, Union

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from telethon import TelegramClient
from telethon.errors import ChatForwardsRestrictedError
from telethon.sessions import Session
from telethon.tl import types

from src.bot.core.models import MyBot
from src.core.config import Config


class TelegramApplication(TelegramClient):

    def __init__(
        self,
        user_id: int,
        config: Config,
        session: "Union[str, Session]",
        database_id: Optional[int] = None,
        phone_number: Optional[int] = None,
        session_factory: Optional[async_sessionmaker[AsyncSession]] = None,
        bot: Optional[MyBot] = None,
    ) -> None:
        super().__init__(session, **config.telegram.params)
        self.config = config
        self.user_id = user_id
        self.database_id = database_id
        self.phone_number = phone_number
        self.session_factory = session_factory
        self.bot = bot

    async def copy_message(
        self, message: types.Message, chat_id: int, reply_to: Optional[int] = None
    ):
        try:
            result = await self.send_message(chat_id, message, reply_to=reply_to)
        except ChatForwardsRestrictedError:
            with io.BytesIO() as bytes_io:
                await self.download_media(message, bytes_io)
                bytes_io.seek(0)

                if isinstance(message, types.Message):
                    msg_media = message.media
                else:
                    msg_media = message

                file = await self.upload_file(file=bytes_io, file_name="photo.jpg")

                if isinstance(msg_media, (types.MessageMediaPhoto, types.Photo)):
                    media = types.InputMediaUploadedPhoto(
                        file=file,
                        spoiler=msg_media.spoiler,
                        ttl_seconds=msg_media.ttl_seconds,
                    )
                elif isinstance(msg_media, (types.MessageMediaDocument, types.Document)):
                    media = types.InputMediaUploadedDocument(
                        file=file,
                        mime_type=msg_media.document.mime_type,
                        attributes=msg_media.document.attributes,
                        spoiler=msg_media.spoiler,
                        ttl_seconds=msg_media.ttl_seconds,
                    )
                message.media = media
                result = await self.send_message(chat_id, message, reply_to=reply_to)
        return result


class TelegramAppManager:
    def __init__(self, apps: List[TelegramApplication]):
        self.apps: List[TelegramApplication] = apps

    def get_client(self, **kwargs) -> Optional[TelegramApplication]:
        filtered_clients = self.apps

        for key, value in kwargs.items():
            filtered_clients = [
                client_info
                for client_info in filtered_clients
                if getattr(client_info, key) == value
            ]

        if not filtered_clients:
            return None

        return filtered_clients[0]
