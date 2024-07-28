import datetime
import pymorphy3

from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from telegram_bot.handlers import bot_commands
from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods import database_request
from telegram_bot.keyboards import inline_markup

# Dict for callbacks. 'function_name': 'callback_name'

CALLBACK = {
    'send_menu': 'menu',
    'send_help': 'help',
    'send_all_homework': 'all_homework',
    'send_tomorrow_homework': 'tomorrow_homework',
    'send_calendar_homework': 'calendar_homework',
    'send_schedule': 'schedule_menu',
    'send_admin_menu': 'admin_menu',
    'send_adding_states': 'add_homework'
}

bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))


# Call a function from callback data
async def call_function_from_callback(callback: CallbackQuery, state: FSMContext) -> None:
    for key in list(CALLBACK.keys()):
        if CALLBACK[key] == callback.data:
            func = getattr(bot_commands, key)
            try:
                await func(callback.message)
            except TypeError:
                await func(callback.message, state)


# Send a date homework from callback data (take data and return homework data). Commands: /calendar and /tomorrow
async def send_date_homework(message: Message | CallbackQuery, date: datetime) -> None:
    homework_data = database_request.get_homework_by_date(date)
    markup = inline_markup.get_calendar_keyboard(date, None)

    morph = pymorphy3.MorphAnalyzer()
    weekday_name = morph.parse(date.strftime('%A'))[0].inflect({'accs'}).word
    date_text = date.strftime("%d.%m.%Y")

    if type(message) is CallbackQuery:
        message = message.message
        await message.delete()

    if len(homework_data) > 0:

        homework_text = text_message.HOMEWORK_TO_SELECTED_DATE.format(f'{weekday_name} {date_text}')

        for i in range(len(homework_data)):
            subject_name = database_request.get_subjects(subject_id=homework_data[i][0])[0][0]
            subject_description = str(homework_data[i][1])

            homework_text += text_message.HOMEWORK_TEXT.format(
                sequence_number=i + 1, subject_name=subject_name,
                subject_description=subject_description
            )
        photos = list(map(lambda elem: elem[2], filter(lambda elem: elem[2] != 'None', homework_data)))

        if len(photos) == 1:
            await bot.send_photo(chat_id=message.chat.id, photo=photos[-1], caption=homework_text, reply_markup=markup)

        elif len(photos) > 1:
            first_photo = [InputMediaPhoto(media=photos[0], caption=homework_text)]
            media_group = first_photo + list(map(lambda elem: InputMediaPhoto(media=elem), photos[1:]))
            media_group = await bot.send_media_group(chat_id=message.chat.id, media=media_group)
            media_group_id, media_group_len = media_group[0].message_id, len(media_group)

            markup = inline_markup.get_calendar_keyboard(date, (media_group_id, media_group_len))
            await message.answer(text=text_message.CHOOSE_ACTION, reply_markup=markup)

        else:
            await message.answer(text=homework_text, reply_markup=markup)

    else:
        text = text_message.HOMEWORK_IS_NULL.format(f'{weekday_name} {date_text}')
        await message.answer(text=text, reply_markup=markup)
