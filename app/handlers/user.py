from aiogram import F, Router
from aiogram.types import Message, callback_query
from aiogram.filters import CommandStart, Command, or_f

from app.filters.chat_types import ChatTypeFilter

import app.keyboards as kb
import app.database.requests as rq

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']))
 
@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('привет, это магазин кроссоовок', reply_markup=kb.main)

# @user_router.message(Command('catalog'))
@user_router.message(or_f(Command('catalog'), (F.text == 'каталог')))
async def catelog(message: Message): 
    await message.answer('выберите категорию товара', reply_markup=await kb.categories())
    
@user_router.message(Command('about'))
@user_router.message(F.text == 'о нас')
async def catelog(message: Message):   
    await message.answer('о нас:')
    
@user_router.message(Command('basket'))
@user_router.message(F.text == 'корзина')
async def catelog(message: Message):    
    await message.answer('корзина')
    
@user_router.message(Command('contacts'))
@user_router.message(F.text == 'контакты')
async def catelog(message: Message): 
    await message.answer('контакты')



@user_router.callback_query(F.data.startswith('category_'))
async def catelog(callback: callback_query):
    await callback.answer('вы выбрали категорию')
    await callback.message.answer('выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))

@user_router.callback_query(F.data.startswith('item_'))
async def catelog(callback: callback_query):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('вы выбрали товар')
    await callback.message.answer(f"Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price} руб.",
                                   reply_markup=await kb.items(callback.data.split('_')[1]))
    
@user_router.callback_query(F.data == 'main')
async def return_main(callback: callback_query):
    await callback.answer('вы вернулись в каталог товаров')
    await callback.message.answer('выберете категорию товара', reply_markup = await kb.categories())
    






