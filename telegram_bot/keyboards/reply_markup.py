from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram_bot.database_methods.database_request import *


# Create subject's reply keyboard for /add
def get_subjects_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for elem in get_subjects():
        builder.row(KeyboardButton(text=elem[0]))

    return builder.as_markup()
