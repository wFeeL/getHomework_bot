from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import *
from telegram_bot.keyboards import inline_markup, reply_markup

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale


# Form for homework data
class HomeworkForm(StatesGroup):
    subject = State()
    date = State()
    description = State()
    file_id = State()


router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


# Start registering a homework
async def register_homework(message: Message, state: FSMContext) -> None:
    await message.answer(text=text_message.CHOOSE_SUBJECT, reply_markup=reply_markup.get_subjects_keyboard())
    await state.set_state(HomeworkForm.subject)


# Process subject
@router.message(HomeworkForm.subject)
async def process_subject(message: Message, state: FSMContext) -> None:
    try:
        # Check availability of subject in database
        if message.text not in list(map(lambda x: x[0], get_subjects())):
            raise ValueError

        await state.update_data(subject=message.text)

        # Remove a reply keyboard markup
        _message = await message.answer(text='Ignore.', reply_markup=ReplyKeyboardRemove())
        await _message.delete()

        await message.answer(
            text=text_message.CHOOSE_DATE.format(date=''),
            reply_markup=await SimpleCalendar(
                locale=await get_user_locale(message.from_user)).start_calendar())

    except ValueError:
        await state.clear()
        await message.answer(text_message.WRONG_SELECTION)


# Process description
@router.message(HomeworkForm.description)
async def process_description(message: Message, state: FSMContext) -> None:
    try:
        # Check the correctness of the description
        if message.text is None:
            raise ValueError

        await state.update_data(description=message.text)
        await message.answer(text_message.CHOOSE_FILE, reply_markup=inline_markup.get_skip_file_keyboard())
        await state.set_state(HomeworkForm.file_id)
    except ValueError:
        await state.clear()
        await message.answer(text_message.WRONG_SELECTION)


# Process file_id
@router.message(HomeworkForm.file_id)
async def process_file(message: Message, state: FSMContext) -> None:
    try:
        file = await bot.get_file(message.photo[0].file_id)
        await state.update_data(file_id=file.file_id)
        await send_homework(message, state)
    except TypeError:
        await state.clear()
        await message.answer(text_message.INCORRECT_REQUEST)


async def send_homework(message: Message, state: FSMContext) -> None:
    try:
        homework_data = await state.get_data()
        subject, date, description, file_id = (homework_data['subject'], homework_data['date'],
                                               homework_data['description'], homework_data['file_id'])

        homework_text = text_message.DATA_TO_SEND.format(subject=subject, date=date, description=description)
        markup = inline_markup.get_send_hw_keyboard()
        if file_id != 'None':
            await bot.send_photo(caption=homework_text, reply_markup=markup, photo=file_id, chat_id=message.chat.id)
        else:
            await message.answer(text=homework_text, reply_markup=markup)

    except KeyError:
        await state.clear()
        await message.answer(text_message.TRY_AGAIN_ERROR)


# CALLBACKS
# Callback for simple calendar (aiogram_calendar)
@router.callback_query(SimpleCalendarCallback.filter())
async def handle_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext) -> None:
    selected, date = await SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user)
    ).process_selection(callback_query, callback_data)

    if selected:
        date = date.strftime('%d.%m.%Y')
        await state.update_data(date=date)

        await callback_query.message.edit_text(text=text_message.CHOOSE_DATE.format(date=date))

        await callback_query.message.answer(text_message.CHOOSE_DESCRIPTION)
        await state.set_state(HomeworkForm.description)

    else:
        await state.clear()


# Skip selecting file
@router.callback_query(F.data == 'skip_file')
async def skip_sending_file(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(file_id='None')
    await callback.message.delete()
    await send_homework(callback.message, state)


# Send homework data to database
@router.callback_query(F.data == 'send_data')
async def send_data(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        homework_data = await state.get_data()
        subject, date, description, file_id = (homework_data['subject'], homework_data['date'],
                                               homework_data['description'], homework_data['file_id'])
        add_value(subject, date, description, file_id)

        await callback.message.answer(text_message.GREAT_JOB, reply_markup=inline_markup.get_admin_menu())
        await callback.message.delete()
        await state.clear()

    except KeyError:
        await state.clear()
        await callback.message.answer(text_message.INCORRECT_REQUEST)


# Cancel sending homework data to database and clear state
@router.callback_query(F.data == 'cancel_send_data')
async def cancel_send_data(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text_message.CANCEL_ACTION, reply_markup=inline_markup.get_admin_menu())
