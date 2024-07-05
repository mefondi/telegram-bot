from string import punctuation

from aiogram import F, Router, Bot
from aiogram.types import Message, callback_query
from aiogram.filters import CommandStart, Command, or_f

from app.filters.chat_types import ChatTypeFilter

user_groups_router = Router()
user_groups_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'ff', 'll', 'kk'}

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@user_groups_router.message(Command('add_admin'))
async def add_admin(message: Message, bot: Bot):
    chat_id = message.chat.id
    list_admin = await bot.get_chat_administrators(chat_id)
    list_admin = [
        mem.user.id
        for mem in list_admin
    ]
    if message.from_user.id in list_admin:
        bot.list_admin = list_admin
    await message.delete()
        

@user_groups_router.message()
@user_groups_router.edited_message()
async def cleaner(message: Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.username} соблюддайте порядок")
        await message.delete()
        # await message.chat.ban(message.from_user.id)