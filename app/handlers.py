from aiogram import F, Router
from aiogram.types import Message, callback_query
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('привет, это магазин кроссоовок', reply_markup=kb.main)

@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer('кнопка помощи')

@router.message(F.text == 'z')
async def zov(message: Message):
    await message.answer('zov')

@router.message()
async def repit(message: Message):
    await message.answer(message.text)



@router.message(F.text == 'каталог')
async def zov(message: Message):
    await message.answer('выберите категорию товара', reply_markup=kb.catalog)

@router.callback_query(F.data == 't-shirt')
async def t_shirt(callback: callback_query):
    await callback.answer('Вы выбрали категорию футболок')
    await callback.message.answer('Вы выбрали категорию футболок')



@router.message(Command('register'))
async def register(message: Message, state:FSMContext):
    await state.set_state(Register.name)
    await message.answer('введите ваше имя')

@router.message(Register.name)
async def register_name(message: Message, state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('введите ваш возраст')


@router.message(Register.age)
async def register_age(message: Message, state:FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer('введите ваш номер телефона', reply_markup=kb.get_number)


@router.message(Register.number, F.contact)
async def register_number(message: Message, state:FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f"ваше имя {data['name']} ваш возраст {data['age']} ваш номер телефона {data['number']}")
    await state.clear()






