import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from Bot import bot_config,adminHandlers,userHandlers


bot = Bot(token=bot_config.token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
logger = logging.getLogger(__name__)


async def main():

    dp = Dispatcher(storage=MemoryStorage())

    await bot.set_my_commands([BotCommand(command="/start", description="Перезапуск бота | Возвращение в главное меню")])

    dp.include_router(adminHandlers.router)
    dp.include_router(userHandlers.router)

    logger.addHandler(adminHandlers.router)
    logger.addHandler(userHandlers.router)
    logger.setLevel(logging.INFO)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    
    logging.basicConfig(filename='BotLogs.log', level=logging.INFO, 
                    format='[%(asctime)s] - [%(name)s] - [%(levelname)s] - [%(message)s]')


    asyncio.run(main())