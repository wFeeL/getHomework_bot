from datetime import date
from typing import Dict

from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Calendar, CalendarScope, )
from aiogram_dialog.widgets.kbd import CalendarConfig
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView, CalendarMonthView, CalendarScopeView, CalendarYearsView,
)
from aiogram_dialog.widgets.text import Const, Format, Text
from babel.dates import get_month_names

from telegram_bot import text_message, config_reader
from telegram_bot.handlers import bot_commands


# Handle date selected from dialog with calendar and call function to send date's homework
async def homework_calendar_date_selected(callback: CallbackQuery, widget,
                                          dialog_manager: DialogManager, selected_date: date) -> None:
    await bot_commands.send_date_homework(callback, selected_date)
    await dialog_manager.done()


# CalendarHomework state (only for calendar widget)
class CalendarHomework(StatesGroup):
    calendar = State()


# Custom month for calendar
class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_month_names(
            'wide', context='stand-alone', locale=locale,
        )[selected_date.month].title()


# Configurate custom calendar (create range and buttons)
class CustomCalendar(Calendar):
    def _init_views(self) -> Dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data, self.config,
                header_text='🗓 ' + Month() + Format(' {date:%Y}'),
                next_month_text=Month() + " ▶",
                prev_month_text="◀ " + Month(),
                today_text=Format("> {date:%d} <")
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data, self.config,
                month_text=Month(),
                this_month_text='> ' + Month() + ' <',
                next_year_text=Format("{date:%Y}") + " ▶",
                prev_year_text="◀ " + Format("{date:%Y}"),
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data, self.config,
                this_year_text=Format("> {date:%Y} <"),
                next_page_text=Format("{date:%Y}") + " ▶",
                prev_page_text="◀ " + Format("{date:%Y}"),
            ),
        }


config = config_reader.config  # Get config with date settings
min_date, max_date = config.min_date, config.max_date
# Create calendar config with date ranges
calendar_config = CalendarConfig(
    min_date=date(min_date.year, min_date.month, min_date.day),
    max_date=date(max_date.year, max_date.month, max_date.day),
    years_columns=1, years_per_page=1, month_columns=1
)

# Create dialog with calendar widget
dialog = Dialog(
    Window(
        Const(text_message.CHOOSE_DATE.format(date='')),
        CustomCalendar(id='homework_calendar', on_click=homework_calendar_date_selected, config=calendar_config),
        state=CalendarHomework.calendar,
    )
)
