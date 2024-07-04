from string import punctuation

from aiogram import F, Router
from aiogram.types import Message, callback_query
from aiogram.filters import CommandStart, Command, or_f

from app.filters.chat_types import ChatTypeFilter

user_groups_router = Router()
user_groups_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'ff', 'll', 'kk'}

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@user_groups_router.message()
@user_groups_router.edited_message()
async def cleaner(message: Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.username} соблюддайте порядок")
        await message.delete()
        # await message.chat.ban(message.from_user.id)