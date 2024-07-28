from telegram_bot.database_methods.database_request import get_users
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


# Decorator for checking admin's of bot
def check_admin(func):
    async def wrapper_check_admin(message: Message, state: FSMContext) -> None:
        telegram_id = str(message.chat.id)
        admin_list = list(map(lambda x: x[0], get_users(is_admin=True)))

        if telegram_id in admin_list:
            await func(message, state)

    return wrapper_check_admin
