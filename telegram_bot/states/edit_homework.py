from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.context import FSMContext

from telegram_bot.database_methods.database_request import *
from telegram_bot.keyboards import inline_markup
from telegram_bot.config_reader import config
from telegram_bot import text_message


# Form for editing homework
class Homework(StatesGroup):
    homework_id = State()
    subject = State()
    date = State()
    description = State()
    file_id = State()


router = Router()
bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))


# Start editing homework (take homework_id for load homework data)
async def process_edit_homework(message: Message, state: FSMContext, homework_id: int = None) -> None:
    try:
        # Take homework data from Homework (StatesGroup)
        data = await state.get_data()

        # Support the completion of homework
        homework_id = data['homework_id'] if homework_id is None else homework_id
        subject = get_homework_by_id(homework_id)[0][1] if 'subject' not in data.keys() else data['subject']
        date = get_homework_by_id(homework_id)[0][2] if 'date' not in data.keys() else data['date']
        description = get_homework_by_id(homework_id)[0][3] if 'description' not in data.keys() else data['description']
        file_id = get_homework_by_id(homework_id)[0][4] if 'file_id' not in data.keys() else data['file_id']

        # Update homework's data with new elements (date or description)
        await state.update_data(
            homework_id=homework_id, subject=subject, date=date, description=description, file_id=file_id
        )

        homework_text = text_message.EDIT_HOMEWORK.format(subject=subject, date=date, description=description)
        markup = inline_markup.get_edit_keyboard()

        if file_id != 'None':
            await bot.send_photo(caption=homework_text, reply_markup=markup, photo=file_id, chat_id=message.chat.id)
        else:
            await message.answer(homework_text, reply_markup=markup)

    except KeyError:
        await message.asnwer(text_message.TRY_AGAIN_ERROR)


# Process homework's date
@router.message(Homework.date)
async def process_date(message: Message, state: FSMContext) -> None:
    try:
        if message.text is not None:
            date = datetime.datetime.strftime(datetime.datetime.strptime(message.text, '%Y-%m-%d'), '%Y-%m-%d')
            await state.update_data(date=date)
        await process_edit_homework(message, state, homework_id=None)

    except ValueError:
        await message.answer(text_message.INCORRECT_REQUEST)


# Process homework's description
@router.message(Homework.description)
async def process_description(message: Message, state: FSMContext) -> None:
    if message.text is not None:
        await state.update_data(description=message.text)
    await process_edit_homework(message, state, homework_id=None)


# Process homework's file_id
@router.message(Homework.file_id)
async def process_description(message: Message, state: FSMContext) -> None:
    file = await bot.get_file(message.photo[0].file_id)
    await state.update_data(file_id=file.file_id)
    await process_edit_homework(message, state, homework_id=None)


# Edit homework's date
@router.callback_query(F.data == 'edit_date')
async def edit_date(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text_message.CHOOSE_DATE_FORMAT)
    await state.set_state(Homework.date)


# Edit homework's description
@router.callback_query(F.data == 'edit_description')
async def edit_description(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text_message.CHOOSE_DESCRIPTION)
    await state.set_state(Homework.description)


# Edit homework's file_id
@router.callback_query(F.data == 'edit_file')
async def edit_file(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.answer(text_message.CHOOSE_FILE)
    await state.set_state(Homework.file_id)


# Edit homework (create request to database)
@router.callback_query(F.data == 'edit_data')
async def edit_data(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        # Take homework data from Homework (StatesGroup)
        data = await state.get_data()
        homework_id, date, description, file_id = data['homework_id'], data['date'], data['description'], data[
            'file_id']
        edit_homework(homework_id, date, description, file_id)  # create editing request to database

        # Stop state (editing homework's data)
        await state.clear()
        await callback.message.delete()
        await callback.message.answer(text_message.EDIT_HOMEWORK_COMPLETE)

    except KeyError:
        await callback.message.answer(text_message.TRY_AGAIN_ERROR)
