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


# Form for homework data
class HomeworkForm(StatesGroup):
    subject = State()
    date = State()
    description = State()
    file_id = State()
    none_state = State()


router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


# Start registering a homework
async def register_homework(message: Message, state: FSMContext) -> None:
    class_id = get_users(telegram_id=message.chat.id)[0][1]

    await message.answer(text=text_message.CHOOSE_SUBJECT, reply_markup=reply_markup.get_subjects_keyboard(class_id))
    await state.set_state(HomeworkForm.subject)


# Process subject
@router.message(HomeworkForm.subject)
async def process_subject(message: Message, state: FSMContext) -> None:
    class_id = get_users(telegram_id=message.chat.id)[0][1]
    try:
        # Check availability of subject in database
        if message.text not in list(map(lambda x: x[1], get_subject(class_ids=class_id))):
            raise ValueError

        await state.update_data(subject=message.text)

        # Remove a reply keyboard markup
        _message = await message.answer(text='Ignore.', reply_markup=ReplyKeyboardRemove())
        await _message.delete()

        calendar = SimpleCalendar()
        calendar.set_dates_range(min_date=config.min_date, max_date=config.max_date)
        today = datetime.datetime.today()
        await message.answer(
            text=text_message.CHOOSE_DATE.format(date=''),
            reply_markup=await calendar.start_calendar(
                year=today.year, month=today.month, day=today.day)
        )

    except ValueError:
        await message.answer(text_message.WRONG_SELECTION, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


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
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


# Process file_id
@router.message(HomeworkForm.file_id)
async def process_file(message: Message, state: FSMContext) -> None:
    try:
        file = await bot.get_file(message.photo[0].file_id)
        await state.update_data(file_id=file.file_id)
        await send_homework(message, state)
        await state.set_state(HomeworkForm.none_state)
    except TypeError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


# Callback for simple calendar (aiogram_calendar)
@router.callback_query(SimpleCalendarCallback.filter())
async def handle_simple_calendar(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext) -> None:
    calendar = SimpleCalendar()
    calendar.set_dates_range(min_date=config.min_date, max_date=config.max_date)
    selected, date = await calendar.process_selection(callback, callback_data)
    data = await state.get_data()
    try:
        if selected and data['subject']:
            date = date.strftime('%d.%m.%Y')
            await state.update_data(date=date)

            await callback.message.edit_text(text=text_message.CHOOSE_DATE.format(date=date))

            await callback.message.answer(text_message.CHOOSE_DESCRIPTION)
            await state.set_state(HomeworkForm.description)
    except KeyError:
        await callback.message.delete()


# Skip selecting file
@router.callback_query(F.data == 'skip_file')
async def skip_sending_file(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(file_id='None')
    await callback.message.delete()
    await send_homework(callback.message, state)


# Confirm sending homework to database
@router.callback_query(F.data == 'send_data')
async def send_data(callback: CallbackQuery, state: FSMContext) -> None:
    class_id = get_admins(telegram_id=callback.message.chat.id)[0][1]

    try:
        homework_data = await state.get_data()
        subject, date, description, file_id = (homework_data['subject'], homework_data['date'],
                                               homework_data['description'], homework_data['file_id'])
        add_value(subject, date, description, file_id, class_id)

        await callback.message.answer(text_message.ADDING_HOMEWORK_COMPLETE,
                                      reply_markup=inline_markup.get_admin_menu())
        await callback.message.delete()
        await state.clear()

    except KeyError:
        await callback.message.answer(text_message.INCORRECT_REQUEST,
                                      reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


# Cancel sending homework data to database and clear state
@router.callback_query(F.data == 'cancel_send_data')
async def cancel_send_data(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text_message.CANCEL_ACTION, reply_markup=inline_markup.get_admin_menu())


# Send homework data to database
async def send_homework(message: Message, state: FSMContext) -> None:
    try:
        homework_data = await state.get_data()
        subject, date, description, file_id = (homework_data['subject'], homework_data['date'],
                                               homework_data['description'], homework_data['file_id'])
        await state.set_state(HomeworkForm.none_state)
        homework_text = text_message.DATA_TO_SEND.format(subject=subject, date=date, description=description)
        markup = inline_markup.get_send_homework_keyboard()
        if file_id != 'None':
            await bot.send_photo(caption=homework_text, reply_markup=markup, photo=file_id, chat_id=message.chat.id)
        else:
            await message.answer(text=homework_text, reply_markup=markup)

    except KeyError:
        await message.answer(text_message.TRY_AGAIN_ERROR,
                             reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()
