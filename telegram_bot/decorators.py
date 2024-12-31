from aiogram.types import Message

from telegram_bot.database_methods.database_request import get_admins, get_users
from telegram_bot.handlers import bot_commands


# Decorator for checking admins of bot
def check_admin(func):
    async def wrapper_check_admin(message: Message, **kwargs) -> None:
        admin = get_admins(telegram_id=message.chat.id)
        if admin != [] and (admin[0][2] or admin[0][3]):
            await func(message, **kwargs)
        else:
            await bot_commands.handle_text(message, **kwargs)
    return wrapper_check_admin


# Decorator for checking admins of bot
def check_super_admin(func):
    async def wrapper_check_super_admin(message: Message, **kwargs) -> None:
        admin = get_admins(telegram_id=message.chat.id)
        if admin != [] and admin[0][3]:
            await func(message, **kwargs)
        else:
            await bot_commands.handle_text(message, **kwargs)
    return wrapper_check_super_admin


# Decorator for checking class of users
def check_class(func):
    async def wrapper_check_class(message: Message, **kwargs) -> None:
        if get_users(telegram_id=message.chat.id)[0][1] == 0:
            await bot_commands.send_class(message, **kwargs)
        else:
            await func(message, **kwargs)

    return wrapper_check_class


# def check_condition(func, condition1: bool = False, condition2: bool = False, check_super_admin: bool = False):
#     async def wrapper_check_condition(message: Message, **kwargs) -> None:
#         print(condition1, condition2, check_super_admin)
#         await func(message, **kwargs)
#     return wrapper_check_condition