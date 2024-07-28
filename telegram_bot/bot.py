import asyncio
import logging
import locale

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from telegram_bot.states import edit_homework, admins, homework
from telegram_bot.handlers import bot_commands
from telegram_bot.config_reader import config

# Getting logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Bot starts polling...')

# Create a telegram_bot by token
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
dp = Dispatcher()


async def main() -> None:
    # Include all routers
    dp.include_router(edit_homework.router)
    dp.include_router(admins.router)
    dp.include_router(homework.router)
    dp.include_router(bot_commands.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
