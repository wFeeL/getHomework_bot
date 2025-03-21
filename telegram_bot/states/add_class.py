from aiogram import Router, F, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import *
from telegram_bot.keyboards import inline_markup, reply_markup


class AddClassForm(StatesGroup):
    number = State()
    letter = State()


router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


async def register_class(message: Message, state: FSMContext) -> None:
    await message.answer(text=text_message.CHOOSE_CLASS_NUMBER, reply_markup=reply_markup.get_choose_class_keyboard())
    await state.set_state(AddClassForm.number)


@router.message(AddClassForm.number)
async def process_class_number(message: Message, state: FSMContext) -> None:
    class_number = message.text
    CLASS_LEN = 11 # set as constant variable
    try:
        if int(class_number) not in range(1, CLASS_LEN + 1):
            raise ValueError
        await state.update_data(number=class_number)
        await message.answer(text=text_message.CHOOSE_CLASS_LETTER, reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddClassForm.letter)

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


@router.message(AddClassForm.letter)
async def process_class_letter(message: Message, state: FSMContext) -> None:
    class_letter = message.text
    try:
        if len(class_letter) > 2:
            raise ValueError
        await state.update_data(letter=class_letter)
        await send_class(message, state)

    except ValueError:
        await message.answer(text_message.WRONG_CLASS_LETTER, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()

async def send_class(message: Message, state: FSMContext) -> None:
    try:
        class_data = await state.get_data()
        number, letter = class_data.values()

        class_text = text_message.CLASS_DATA_TO_SEND.format(number=number, letter=letter)
        markup = inline_markup.get_send_class_keyboard()
        await message.answer(text=class_text, reply_markup=markup)

    except KeyError:
        await message.answer(text_message.TRY_AGAIN_ERROR,
                             reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()

@router.callback_query(F.data == 'send_class_data')
async def send_data(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        class_data = await state.get_data()
        number, letter = class_data.values()
        add_class_value(number, letter)

        await callback.message.answer(text_message.ADDING_CLASS_COMPLETE.format(number=number, letter=letter),
                                      reply_markup=inline_markup.get_admin_menu())
        await callback.message.delete()
        await state.clear()

    except KeyError:
        await callback.message.answer(text_message.INCORRECT_REQUEST,
                                      reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()
