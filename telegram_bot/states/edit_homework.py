from datetime import datetime, date

from aiogram import Router, F, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
from aiogram_calendar.schemas import highlight, DialogCalAct

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import get_users, get_homework, get_subject, update_homework
from telegram_bot.keyboards import inline_markup


# Form for editing homework
class Homework(StatesGroup):
    homework_id = State()
    subject_id = State()
    date = State()
    description = State()
    file_id = State()

class CustomDialogCalendar(DialogCalendar):
    async def start_calendar(
            self,
            year: int = datetime.now().year,
            month: int = None
    ) -> InlineKeyboardMarkup:
        today = datetime.now()
        now_year = today.year

        if month:
            return await self._get_days_kb(year, month)
        kb = []
        # inline_kb = InlineKeyboardMarkup(row_width=5)
        # first row - years
        years_row = []
        for value in range(year - 2, year + 3):
            if self.min_date.year <= value <= self.max_date.year:
                years_row.append(InlineKeyboardButton(
                    text=str(value) if value != now_year else highlight(value),
                    callback_data=DialogCalendarCallback(act=DialogCalAct.set_y, year=value, month=-1, day=-1).pack()
                ))
        kb.append(years_row)
        # nav buttons
        nav_row = []
        if self.min_date.year <= year - 2 <= self.max_date.year:
            nav_row.append(InlineKeyboardButton(
                text='<<',
                callback_data=DialogCalendarCallback(act=DialogCalAct.prev_y, year=year, month=-1, day=-1).pack()
            ))
        nav_row.append(InlineKeyboardButton(
            text=self._labels.cancel_caption,
            callback_data=DialogCalendarCallback(act=DialogCalAct.cancel, year=year, month=1, day=1).pack()
        ))
        if self.min_date.year <= year + 3 <= self.max_date.year:
            nav_row.append(InlineKeyboardButton(
                text='>>',
                callback_data=DialogCalendarCallback(act=DialogCalAct.next_y, year=year, month=1, day=1).pack()
            ))
        kb.append(nav_row)
        return InlineKeyboardMarkup(row_width=5, inline_keyboard=kb)

    async def _get_month_kb(self, year: int):
        """Creates an inline keyboard with months for specified year"""

        today = datetime.now()
        now_month, now_year = today.month, today.year
        now_year = today.year

        kb = []
        # first row with year button
        years_row = [InlineKeyboardButton(
            text=self._labels.cancel_caption,
            callback_data=DialogCalendarCallback(act=DialogCalAct.cancel, year=year, month=1, day=1).pack()
        ), InlineKeyboardButton(
            text=str(year) if year != today.year else highlight(year),
            callback_data=DialogCalendarCallback(act=DialogCalAct.start, year=year, month=-1, day=-1).pack()
        ), InlineKeyboardButton(text=" ", callback_data=self.ignore_callback)]
        kb.append(years_row)
        # two rows with 6 months buttons
        month6_row = []

        def highlight_month():
            month_str = self._labels.months[month - 1]
            if now_month == month and now_year == year:
                return highlight(month_str)
            return month_str

        def is_available_month(year: int, month: int) -> bool:
            return self.min_date <= datetime(year, month, 1) <= self.max_date

        for month in range(1, 7):
            if is_available_month(year, month):
                month6_row.append(InlineKeyboardButton(
                    text=highlight_month(),
                    callback_data=DialogCalendarCallback(
                        act=DialogCalAct.set_m, year=year, month=month, day=-1
                    ).pack()
                ))
        month12_row = []

        for month in range(7, 13):
            if is_available_month(year, month):
                month12_row.append(InlineKeyboardButton(
                    text=highlight_month(),
                    callback_data=DialogCalendarCallback(
                        act=DialogCalAct.set_m, year=year, month=month, day=-1
                    ).pack()
                ))

        kb.append(month6_row)
        kb.append(month12_row)
        return InlineKeyboardMarkup(row_width=6, inline_keyboard=kb)

router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


# Get homework data and update state's data
async def update_edit_data(message: Message, state: FSMContext, homework_id: int) -> None:
    class_id = get_users(telegram_id=message.chat.id)[0][1]
    homework_data = get_homework(id=homework_id, class_id=class_id)[0]
    subject_id, date, description, file_id = homework_data[1], homework_data[2], homework_data[3], homework_data[4]
    # subject = get_subject(id=subject_id)[0][1]
    if type(date) is not str:
        date = date.strftime("%d.%m.%Y")
    data = {
        'homework_id': homework_id,
        'subject_id': subject_id,
        'date': date,
        'description': description,
        'file_id': file_id
    }

    await state.update_data(data)
    await process_edit_homework(message, state, is_edited=False)


# Main editing menu with choose action
async def process_edit_homework(message: Message, state: FSMContext, is_edited: bool = True) -> None:
    try:
        # Take homework data from Homework (StatesGroup)
        data = await state.get_data()
        homework_id, subject_id, date, description, file_id = data.values()
        subject = get_subject(id=subject_id)[0][1]

        homework_text = text_message.EDIT_HOMEWORK.format(subject=subject, date=date, description=description)

        if file_id != 'None':
            markup = inline_markup.get_edit_homework_keyboard(is_edited=is_edited)
            await bot.send_photo(caption=homework_text, reply_markup=markup, photo=file_id, chat_id=message.chat.id)
        else:
            markup = inline_markup.get_edit_homework_keyboard(is_file=False, is_edited=is_edited)
            await message.answer(homework_text, reply_markup=markup)

    except KeyError:
        await message.answer(text_message.TRY_AGAIN_ERROR,
                             reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


# Process homework's description
@router.message(Homework.description)
async def process_description(message: Message, state: FSMContext) -> None:
    try:
        if message.text is None:
            raise TypeError
        await state.update_data(description=message.text)
    except TypeError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
    finally:
        await state.set_state(Homework.subject_id)
        await process_edit_homework(message, state)


# Process homework's file_id
@router.message(Homework.file_id)
async def process_file_id(message: Message, state: FSMContext) -> None:
    try:
        file = await bot.get_file(message.photo[0].file_id)
        await state.update_data(file_id=file.file_id)
    except TypeError:
        await message.answer(text_message.INCORRECT_REQUEST, reply_markup=inline_markup.get_delete_message_keyboard())
    finally:
        await process_edit_homework(message, state)
        await state.set_state(Homework.subject_id)


# Edit homework's date
@router.callback_query(F.data == 'edit_date')
async def edit_date(callback: CallbackQuery) -> None:
    await callback.message.delete()
    today = date.today()
    await callback.message.answer(
        text=text_message.CHOOSE_DATE.format(date=''),
        reply_markup=await CustomDialogCalendar().start_calendar(
            year=today.year, month=today.month)
    )


# Edit homework's description
@router.callback_query(F.data == 'edit_description')
async def edit_description(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(text_message.CHOOSE_DESCRIPTION)
    await state.set_state(Homework.description)


# Edit homework's file_id
@router.callback_query(F.data == 'edit_file')
async def edit_file(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(text_message.CHOOSE_FILE)
    await state.set_state(Homework.file_id)


# Delete homework's file_id
@router.callback_query(F.data == 'delete_file')
async def delete_file(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await state.update_data(file_id='None')
    await process_edit_homework(callback.message, state)


# Edit homework (create request to database)
@router.callback_query(F.data == 'edit_data')
async def edit_data(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        # Take homework data from Homework (StatesGroup)
        data = await state.get_data()
        update_homework(**data)  # create editing request to database

        # Stop state (editing homework's data)
        await state.clear()
        await callback.message.delete()
        await callback.message.answer(text_message.EDIT_HOMEWORK_COMPLETE,
                                      reply_markup=inline_markup.get_users_keyboard())

    except KeyError:
        await callback.message.answer(text_message.TRY_AGAIN_ERROR,
                                      reply_markup=inline_markup.get_delete_message_keyboard())
        await state.clear()


# Stop state
@router.callback_query(F.data == 'stop_state')
async def stop_state(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await state.clear()


# Callback for dialog calendar (aiogram_calendar)
@router.callback_query(DialogCalendarCallback.filter())
async def handle_dialog_calendar(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext) -> None:
    calendar = CustomDialogCalendar()
    calendar.set_dates_range(min_date=config.min_date, max_date=config.max_date)
    selected, date = await calendar.process_selection(callback, callback_data)

    # Check availability of selected date
    if selected:
        await callback.message.delete()
        await state.update_data(date=date.strftime("%d.%m.%Y"))
        await process_edit_homework(callback.message, state)
        await state.set_state(Homework.subject_id)
