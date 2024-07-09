from aiogram import Router, F
from aiogram.types import Message, callback_query, ReplyKeyboardRemove
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.filters.chat_types import ChatTypeFilter, is_admin
import app.database.requests as re
import app.keyboards as kb

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), is_admin())

class addproduct(StatesGroup):
    name = State()
    categories = State()
    description = State()
    price = State()
    image = State()
    
    item_for_change = None


@admin_router.message(Command('admin'))
async def admin1(message: Message):
    await message.answer('добро пожаловать: администратор',reply_markup=kb.admin)
   
         
@admin_router.message(F.text == 'список товаров 📁')
async def admin2(message: Message):
    for item in await re.get_items():
        await message.answer_photo(
            item.image,
            caption=f"название: {item.name}\nописание: {item.description}\nстоимость: {round(item.price, 2)}",
            reply_markup=await kb.item(item.id)
        )


@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_product(callback: callback_query):
    item_id = callback.data.split("_")[-1]
    await re.delete_item(int(item_id))
    await callback.answer("товар удален")
    await callback.message.answer("товар удален")

    
@admin_router.callback_query(StateFilter(None),F.data.startswith('change_'))
async def delete_product(callback: callback_query, state : FSMContext):
    item_id = callback.data.split("_")[-1]
    item_for_change = await re.get_item(int(item_id))
    addproduct.item_for_change = item_for_change
    await callback.answer()
    await callback.message.answer("введите название товара", reply_markup=ReplyKeyboardRemove())
    await state.set_state(addproduct.name)

 
@admin_router.message(StateFilter(None), F.text == 'добавить товар ✔️')
async def admin3(message: Message, state: FSMContext):
    await message.answer('введите название товара', reply_markup=ReplyKeyboardRemove())
    await state.set_state(addproduct.name)


@admin_router.message(StateFilter('*'), Command('отмена'))    
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def admin4(message: Message, state: FSMContext) -> None:
    curren = await state.get_state()
    if curren is None:
        return
    await state.clear()
    await message.answer('действие отмены', reply_markup=kb.admin)

    
@admin_router.message(StateFilter('*'), Command('назад'))    
@admin_router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def admin5(message: Message, state: FSMContext) -> None:
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
    
    
@admin_router.message(addproduct.name, or_f(F.text, F.text == '.'))
async def admin6(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=addproduct.item_for_change.name)
    else:
        await state.update_data(name=message.text)
    await message.answer('выберите категорию товара', reply_markup=await kb.categories_for_admin())
    await state.set_state(addproduct.categories)
      
      
@admin_router.message(addproduct.name)
async def admin7(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')
 
       
@admin_router.message(addproduct.categories, F.text == '.')
async def admin8( message: Message, state: FSMContext):
    await state.update_data(categories=addproduct.item_for_change.category)
    await message.answer('введите описание товара')
    await state.set_state(addproduct.description)

     
@admin_router.callback_query(addproduct.categories, F.data)
async def admin8( callback: callback_query, state: FSMContext):
    await state.update_data(categories=callback.data)
    await callback.answer('категория принята')
    await callback.message.answer('введите описание товара')
    await state.set_state(addproduct.description)


@admin_router.message(addproduct.categories)
async def admin9(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')
   
    
@admin_router.message(addproduct.description, or_f(F.text, F.text == '.'))
async def admin0(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(description=addproduct.item_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer('введите стоимость товара')
    await state.set_state(addproduct.price)


@admin_router.message(addproduct.description)
async def admin10(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')


@admin_router.message(addproduct.price, or_f(F.text, F.text == '.'))
async def admin11(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(price=addproduct.item_for_change.price)
    else:
        await state.update_data(price=message.text)
    await message.answer('загрузите изображение товара')
    await state.set_state(addproduct.image)


@admin_router.message(addproduct.price)
async def admin12(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')
   
    
@admin_router.message(addproduct.image, or_f(F.photo, F.text == '.'))
async def admin13(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(image=addproduct.item_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    await message.answer('товар добавлен', reply_markup=kb.admin)
    data = await state.get_data()
    if addproduct.item_for_change:
        await re.update_items(addproduct.item_for_change.id, data)
    else:
        await re.add_item(data)
    await state.clear()
    addproduct.item_for_change = None


@admin_router.message(addproduct.image)
async def admin14(message: Message, state: FSMContext):
    await message.answer('введины не допустимые данные')