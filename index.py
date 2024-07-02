import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main()
    bot = Bot(token='7168793031:AAE-sqCrG2Z-BOOwUCb6dA6vzwGVQbgDvtM')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('бот выключен')