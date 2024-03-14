import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from interface_bot.handlers import router

from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=bot_token)

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    # Чтобы бот не обрабатывал апдейты, которые пришли до его запуска,
    # только непосредственно те, что во время работы,
    # то, что пришло во время "простоя" он удаляет
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
