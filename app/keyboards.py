from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                            InlineKeyboardMarkup,InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='каталог')],
                                     [KeyboardButton(text='о нас')],
                                     [KeyboardButton(text='корзина'), KeyboardButton(text='контакты')]],
                                     resize_keyboard = True,
                                     input_field_placeholder='выберите пункт меню...')

catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='футболки', callback_data='t-shirt')],
                                                [InlineKeyboardButton(text='кроссовки', callback_data='sneakers')],
                                                [InlineKeyboardButton(text='кепки', callback_data='cap')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='отправить номер телефона', request_contact=True)]], 
                                 resize_keyboard = True) 