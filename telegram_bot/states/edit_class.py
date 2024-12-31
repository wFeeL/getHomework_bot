import datetime

from aiogram import Router, F, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram_calendar import DialogCalendar, DialogCalendarCallback

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import get_class, update_class
from telegram_bot.keyboards import inline_markup, reply_markup


class Class(StatesGroup):
    class_id = State()
    number = State()
    letter = State()


router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


async def update_edit_data(message: Message, state: FSMContext, class_id: int) -> None:
    class_data = get_class(id=class_id)[0]
    print(class_data, class_id)
    letter, number = class_data[1], class_data[2]
    data = {
        'class_id': class_id,
        'letter': letter,
        'number': number
    }

    await state.update_data(data)
    await process_edit_class(message, state, is_edited=False)


# Main editing menu with choose action
async def process_edit_class(message: Message, state: FSMContext, is_edited: bool = True) -> None:
    try:
        # Take homework data from Homework (StatesGroup)
        data = await state.get_data()

        letter, number = data['letter'], data['number']

        class_text = text_message.EDIT_CLASS.format(number=number, letter=letter)
        await message.answer(class_text, reply_markup=inline_markup.get_edit_class_keyboard(is_edited=is_edited))

    except KeyError:
        await message.answer(text_message.TRY_AGAIN_ERROR,
                             reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


@router.message(Class.number)
async def process_number(message: Message, state: FSMContext) -> None:
    try:
        class_number = message.text
        CLASS_LEN = 11
        if int(class_number) not in range(1, CLASS_LEN + 1):
            raise ValueError
        await state.update_data(number=class_number)
    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
    finally:
        await process_edit_class(message, state)
        await state.set_state(Class.class_id)


@router.message(Class.letter)
async def process_letter(message: Message, state: FSMContext) -> None:
    try:
        if message.text is None or len(message.text) > 2:
            # not integer
            raise TypeError
        await state.update_data(letter=message.text)
    except TypeError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
    finally:
        await state.set_state(Class.class_id)
        await process_edit_class(message, state)


@router.callback_query(F.data == 'edit_number')
async def edit_number(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(text_message.CHOOSE_CLASS_NUMBER,
                                  reply_markup=reply_markup.get_choose_class_keyboard())
    await state.set_state(Class.number)


@router.callback_query(F.data == 'edit_letter')
async def edit_letter(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(text_message.CHOOSE_CLASS_LETTER,
                                  reply_markup=ReplyKeyboardRemove())
    await state.set_state(Class.letter)



# Edit homework (create request to database)
@router.callback_query(F.data == 'edit_class_data')
async def edit_class_data(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        # Take homework data from Homework (StatesGroup)
        data = await state.get_data()
        class_id, number, letter = data['class_id'], data['number'], data['letter']
        update_class(class_id, number, letter)  # create editing request to database

        # Stop state (editing homework's data)
        await state.clear()
        await callback.message.delete()
        await callback.message.answer(text_message.EDIT_CLASS_COMPLETE,
                                      reply_markup=inline_markup.get_users_keyboard())

    except KeyError:
        await callback.message.answer(text_message.TRY_AGAIN_ERROR,
                                      reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()
