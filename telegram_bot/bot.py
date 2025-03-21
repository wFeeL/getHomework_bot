import asyncio
import logging
import locale

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from telegram_bot.states import (edit_homework, edit_admins, add_homework, bot_message, add_class, edit_class,
                                 add_subject, edit_subject, add_teacher)
from telegram_bot.handlers import bot_commands
from telegram_bot.config_reader import config

# Getting logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create a telegram_bot by token
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main() -> None:
    # Include all routers
    routers = [
        edit_homework.router, add_homework.router, edit_admins.router, add_class.router, edit_class.router,
        bot_message.router, add_subject.router, add_teacher.router, edit_subject.router, bot_commands.router,
    ]
    dp.include_routers(*routers)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
