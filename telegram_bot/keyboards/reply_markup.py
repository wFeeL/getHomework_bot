from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram_bot.database_methods.database_request import *


# Create subject's reply keyboard for /add
def get_subjects_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for elem in get_subjects():
        builder.row(KeyboardButton(text=elem[0]))

    return builder.as_markup()


def get_pdf_page_keyboard(page: int | str) -> ReplyKeyboardMarkup:
    if page.isdigit():
        markup = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=f'{page - 1}'), KeyboardButton(text=f'{page + 1}')]]
        )
    else:
        page = page.split('.')
        paragraph, number = int(page[0]), int(page[1])
        markup = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=f'{paragraph}.{number - 1}'),
                       KeyboardButton(text=f'{paragraph}.{number + 1}')]]
        )
    return markup
