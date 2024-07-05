from typing import Any
from aiogram.filters import Filter
from aiogram import types, Bot

class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types
    
class is_admin(Filter):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.list_admin