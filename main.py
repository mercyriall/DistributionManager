import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from interface_bot.handlers import router
from database.init_db import database as db


load_dotenv()

bot_token = os.getenv('BOT_TOKEN')


async def main():
    logging.basicConfig(level=logging.INFO)

    await db.init_pool()

    bot = Bot(token=bot_token)

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    # удаляет запросы пришедшие в нерабочем состоянии
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())
