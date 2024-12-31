from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram_bot.database_methods.database_request import get_subject, get_class


# Create subject's reply keyboard for /add
def get_subjects_keyboard(class_id: int | str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for elem in get_subject(class_ids=class_id):
        builder.row(KeyboardButton(text=elem[1]))

    return builder.as_markup()


# Create class reply keyboard for /class
def get_class_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    classes = get_class()

    for elem in classes:
        class_id, letter, number = elem[0], elem[1], elem[2]
        builder.row(KeyboardButton(text=f'{number} {letter}'))
    return builder.as_markup()

# Create choose class keyboard for /add_class
def get_choose_class_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    CLASS_LEN = 11 # set as constant variable
    for i in range(1, CLASS_LEN + 1):
        builder.add(KeyboardButton(text=str(i)))
    return builder.as_markup()
