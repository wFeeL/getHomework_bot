from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import CallbackQuery

from telegram_bot.handlers import bot_commands
from telegram_bot.config_reader import config

CALLBACK = {
    'send_menu': 'menu',
    'send_help': 'help',
    'send_all_homework': 'all_homework',
    'send_tomorrow_homework': 'tomorrow_homework',
    'send_calendar_homework': 'calendar_homework',
    'send_class': 'class',
    'send_choose_class': 'choose_class',
    'send_schedule': 'schedule_menu',
    'send_admin_menu': 'admin_menu',
    'send_adding_states': 'adding_states',
    'send_add_subject': 'adding_subject'
}

bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


# Call a function from callback data
async def call_function_from_callback(callback: CallbackQuery, **kwargs) -> None:
    """
    Call function from callback.
    Find name of function in const dict and call with all arguments.
    :param callback: Callback
    :param kwargs: Needed arguments.
    """
    for key in list(CALLBACK.keys()):
        if CALLBACK[key] == callback.data:
            func = getattr(bot_commands, key)
            await func(callback.message, **kwargs)
