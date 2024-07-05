from aiogram import Router, F
from aiogram.types import Message, callback_query, ReplyKeyboardRemove
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.filters.chat_types import ChatTypeFilter, is_admin
import app.keyboards as kb

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), is_admin())

@admin_router.message(Command('admin'))
async def admin(message: Message):
    await message.answer('добро пожаловать: администратор',reply_markup=kb.admin)
        
@admin_router.message(F.text == 'удалить товар ❌')
async def admin(message: Message):
    await message.answer('добро пожаловать: администратор')
    
@admin_router.message(F.text == 'изменить товар ♻️')
async def admin(message: Message):
    await message.answer('добро пожаловать: администратор')
    
@admin_router.message(F.text == 'список товаров 📁')
async def admin(message: Message):
    await message.answer('добро пожаловать: администратор')
    
class addproduct(StatesGroup):
    name = State()
    categories = State()
    description = State()
    price = State()
    image = State()
 
@admin_router.message(StateFilter(None), F.text == 'добавить товар ✔️')
async def admin(message: Message, state: FSMContext):
    await message.answer('введите название товара', reply_markup=ReplyKeyboardRemove())
    await state.set_state(addproduct.name)

@admin_router.message(StateFilter('*'), Command('отмена'))    
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def admin(message: Message, state: FSMContext) -> None:
    curren = await state.get_state()
    if curren is None:
        return
    await state.clear()
    await message.answer('действие отмены', reply_markup=kb.admin)
    
@admin_router.message(StateFilter('*'), Command('назад'))    
@admin_router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def admin(message: Message, state: FSMContext) -> None:
    curren = await state.get_state()
    if curren == addproduct.name:
        await message.answer('предыдущего шага нет')
        return
    previous = None
    for step in addproduct.__all_states__:
        if step.state == curren:
            await state.set_state(previous)
            await message.answer(f"введите {previous.state[11:]} заново")
            return
        previous = step
    
@admin_router.message(addproduct.name, F.text)
async def admin(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('выберите категорию товара', reply_markup=await kb.categories_for_admin())
    await state.set_state(addproduct.categories)
      
@admin_router.message(addproduct.name)
async def admin(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')
    
@admin_router.callback_query(addproduct.categories, F.data)
async def admin(callback: callback_query, state: FSMContext):
    await state.update_data(categories=callback.data)
    await callback.answer('категория принята')
    await callback.message.answer('введите описание товара')
    await state.set_state(addproduct.description)

@admin_router.message(addproduct.categories)
async def admin(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')
    
@admin_router.message(addproduct.description, F.text)
async def admin(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('введите стоимость товара')
    await state.set_state(addproduct.price)

@admin_router.message(addproduct.description)
async def admin(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')

@admin_router.message(addproduct.price, F.text)
async def admin(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer('загрузите изображение товара')
    await state.set_state(addproduct.image)

@admin_router.message(addproduct.price)
async def admin(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')
    
@admin_router.message(addproduct.image, F.photo)
async def admin(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer('товар добавлен', reply_markup=kb.admin)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

@admin_router.message(addproduct.image)
async def admin(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')