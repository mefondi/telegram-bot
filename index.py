import os
import asyncio
from aiogram import Bot, Dispatcher, F, types

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from app.handlers.user import user_router
from app.handlers.user_group import user_groups_router
from app.handlers.admin import admin_router
from app.database.models import async_main
from common.bot_cmds_list import privet


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    bot.list_admin = []
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(user_groups_router)
    dp.include_router(admin_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=privet, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('бот выключен')