from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='каталог 📁')],
                                     [KeyboardButton(text='о нас 😇')],
                                     [KeyboardButton(text='корзина 🗑️'), KeyboardButton(text='контакты 📱')]],
                                     resize_keyboard = True,
                                     input_field_placeholder='выберите пункт меню...')

get = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='отправить номер ☎️', request_contact=True)],
                                        [KeyboardButton(text='отправить локацию 🌐', request_location=True)],
                                        [KeyboardButton(text='создать опрос 📨', request_poll=KeyboardButtonPollType())]],
                                        resize_keyboard = True,
                                        input_field_placeholder='выберите пункт меню...')

admin = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='добавить товар ✔️'), KeyboardButton(text='изменить товар ♻️')],
                                      [KeyboardButton(text='удалить товар ❌')],
                                      [KeyboardButton(text='список товаров 📁')]],
                                        resize_keyboard = True,
                                        input_field_placeholder='выберите пункт меню...')
async def categories_for_admin():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"{category.id}"))
    return keyboard.adjust(2).as_markup()

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='на главную ', callback_data='main'))
    return keyboard.adjust(2).as_markup()

async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='на главную', callback_data='main'))
    return keyboard.adjust(2).as_markup()