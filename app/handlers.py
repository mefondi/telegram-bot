from aiogram import F, Router
from aiogram.types import Message, callback_query
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()
 
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('привет, это магазин кроссоовок', reply_markup=kb.main)

@router.message(F.text == 'каталог')
async def catelog(message: Message):
    await message.answer('выберите категорию товара', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('category_'))
async def catelog(callback: callback_query):
    await callback.answer('вы выбрали категорию')
    await callback.message.answer('выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))

@router.callback_query(F.data.startswith('item_'))
async def catelog(callback: callback_query):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('вы выбрали товар')
    await callback.message.answer(f"Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price} руб.",
                                   reply_markup=await kb.items(callback.data.split('_')[1]))





