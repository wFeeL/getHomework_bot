import calendar
from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram_calendar.schemas import highlight, SimpleCalAct, superscript

from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import get_users, get_admins, get_subject, add_homework_value
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

class CustomSimpleCalendar(SimpleCalendar):
    async def start_calendar(
            self,
            year: int = datetime.now().year,
            month: int = datetime.now().month,
            day: int = datetime.now().day
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided year and month
        :param int day: Day to use in the calendar, if None the current day is used.
        :param int year: Year to use in the calendar, if None the current year is used.
        :param int month: Month to use in the calendar, if None the current month is used.
        :return: Returns InlineKeyboardMarkup object with the calendar.
        """

        today = datetime.now()
        now_weekday = self._labels.days_of_week[today.weekday()]
        now_month, now_year, now_day = today.month, today.year, today.day

        def highlight_month():
            month_str = self._labels.months[month - 1]
            if now_month == month and now_year == year:
                return highlight(month_str)
            return month_str

        def highlight_weekday():
            if now_month == month and now_year == year and now_weekday == weekday:
                return highlight(weekday)
            return weekday

        def format_day_string():
            date_to_check = datetime(year, month, day)
            if self.min_date and date_to_check < self.min_date:
                return superscript(str(day))
            elif self.max_date and date_to_check > self.max_date:
                return superscript(str(day))
            return str(day)

        def highlight_day():
            day_string = format_day_string()
            if now_month == month and now_year == year and now_day == day:
                return highlight(day_string)
            return day_string

        # building a calendar keyboard
        kb = []

        # inline_kb = InlineKeyboardMarkup(row_width=7)
        # First row - Year
        years_row = []
        date_to_check = datetime(year, month, day)
        if self.min_date and date_to_check.year - 1 >= self.min_date.year:
            years_row.append(InlineKeyboardButton(
                text="<<",
                callback_data=SimpleCalendarCallback(act=SimpleCalAct.prev_y, year=year, month=month, day=1).pack()
            ))

        years_row.append(InlineKeyboardButton(
            text=str(year) if year != now_year else highlight(year),
            callback_data=self.ignore_callback
        ))
        if self.max_date and date_to_check.year + 1 <= self.max_date.year:
            years_row.append(InlineKeyboardButton(
                text=">>",
                callback_data=SimpleCalendarCallback(act=SimpleCalAct.next_y, year=year, month=month, day=1).pack()
            ))
        kb.append(years_row)

        # Month nav Buttons
        month_row = []
        if self.min_date and date_to_check - timedelta(days=31) >= self.min_date:
            month_row.append(InlineKeyboardButton(
                text="<",
                callback_data=SimpleCalendarCallback(act=SimpleCalAct.prev_m, year=year, month=month, day=1).pack()
            ))

        month_row.append(InlineKeyboardButton(
            text=highlight_month(),
            callback_data=self.ignore_callback
        ))
        if self.max_date and date_to_check + timedelta(days=31) <= self.max_date:
            month_row.append(InlineKeyboardButton(
                text=">",
                callback_data=SimpleCalendarCallback(act=SimpleCalAct.next_m, year=year, month=month, day=1).pack()
            ))
        kb.append(month_row)

        # Week Days
        week_days_labels_row = []
        for weekday in self._labels.days_of_week:
            week_days_labels_row.append(
                InlineKeyboardButton(text=highlight_weekday(), callback_data=self.ignore_callback)
            )
        kb.append(week_days_labels_row)

        # Calendar rows - Days of month
        month_calendar = calendar.monthcalendar(year, month)

        for week in month_calendar:
            days_row = []
            for day in week:
                if day == 0:
                    days_row.append(InlineKeyboardButton(text=" ", callback_data=self.ignore_callback))
                    continue
                days_row.append(InlineKeyboardButton(
                    text=highlight_day(),
                    callback_data=SimpleCalendarCallback(act=SimpleCalAct.day, year=year, month=month, day=day).pack()
                ))
            kb.append(days_row)

        # nav today & cancel button
        cancel_row = [InlineKeyboardButton(
            text=self._labels.cancel_caption,
            callback_data=SimpleCalendarCallback(act=SimpleCalAct.cancel, year=year, month=month, day=day).pack()
        ), InlineKeyboardButton(text=" ", callback_data=self.ignore_callback), InlineKeyboardButton(
            text=self._labels.today_caption,
            callback_data=SimpleCalendarCallback(act=SimpleCalAct.today, year=year, month=month, day=day).pack()
        )]
        kb.append(cancel_row)
        return InlineKeyboardMarkup(row_width=7, inline_keyboard=kb)

    async def process_selection(self, query: CallbackQuery, data: SimpleCalendarCallback) -> tuple:
        """
        Process the callback_query. This method generates a new calendar if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by calendar_callback
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """
        return_data = (False, None)

        # processing empty buttons, answering with no action
        if data.act == SimpleCalAct.ignore:
            await query.answer(cache_time=60)
            return return_data

        temp_date = datetime(int(data.year), int(data.month), 1)

        # user picked a day button, return date
        if data.act == SimpleCalAct.day:
            return await self.process_day_select(data, query)

        # user navigates to previous year, editing message with new calendar
        if data.act == SimpleCalAct.prev_y:
            prev_date = datetime(int(data.year) - 1, self.min_date.month, 1)
            await self._update_calendar(query, prev_date)
        # user navigates to next year, editing message with new calendar
        if data.act == SimpleCalAct.next_y:
            next_date = datetime(int(data.year) + 1, 1, 1)
            await self._update_calendar(query, next_date)
        # user navigates to previous month, editing message with new calendar
        if data.act == SimpleCalAct.prev_m:
            prev_date = temp_date - timedelta(days=1)
            await self._update_calendar(query, prev_date)
        # user navigates to next month, editing message with new calendar
        if data.act == SimpleCalAct.next_m:
            next_date = temp_date + timedelta(days=31)
            await self._update_calendar(query, next_date)
        if data.act == SimpleCalAct.today:
            next_date = datetime.now()
            if next_date.year != int(data.year) or next_date.month != int(data.month):
                await self._update_calendar(query, datetime.now())
            else:
                await query.answer(cache_time=60)
        if data.act == SimpleCalAct.cancel:
            await query.message.delete_reply_markup()
        # at some point user clicks DAY button, returning date
        return return_data



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

        simple_calendar = CustomSimpleCalendar()
        simple_calendar.set_dates_range(min_date=config.min_date, max_date=config.max_date)
        today = datetime.today()
        await message.answer(
            text=text_message.CHOOSE_DATE.format(date=''),
            reply_markup=await simple_calendar.start_calendar(
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
    simple_calendar = CustomSimpleCalendar()
    simple_calendar.set_dates_range(min_date=config.min_date, max_date=config.max_date)
    selected, date = await simple_calendar.process_selection(callback, callback_data)
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
        subject, date, description, file_id = homework_data.values()
        add_homework_value(subject, date, description, file_id, class_id)

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
        subject, date, description, file_id = homework_data.values()
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
