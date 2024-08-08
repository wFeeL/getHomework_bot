import requests
import json
import pymorphy3

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

from telegram_bot import text_message, callback_text
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import *
from telegram_bot.keyboards import inline_markup
from telegram_bot.decorators import check_admin
from telegram_bot.states import admins, edit_homework, homework

from aiogram_calendar import DialogCalendar, DialogCalendarCallback

router = Router()
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


# COMMANDS for common telegram user
# Command: /start
@router.message(Command('start'))
async def send_greetings(message: Message) -> None:
    user_telegram_id = str(message.from_user.id)
    user_telegram_username = message.from_user.username
    user_telegram_name = message.from_user.first_name

    if user_telegram_id not in list(map(lambda x: x[0], get_users())):
        register_user(telegram_id=user_telegram_id, telegram_username=user_telegram_username)
    await message.answer(text=text_message.GREETINGS.format(user=user_telegram_name),
                         reply_markup=inline_markup.get_start_keyboard())


# Command: /help
@router.message(Command('help'))
async def send_help(message: Message) -> None:
    await message.answer(text=text_message.HELP, reply_markup=inline_markup.get_help_keyboard())


# Command: /menu
@router.message(Command('menu'))
async def send_menu(message: Message) -> None:
    await message.answer(text=text_message.CHOOSE_CATEGORY, reply_markup=inline_markup.get_homework_menu())


# Command: /tomorrow
@router.message(Command('tomorrow'))
async def send_tomorrow_homework(message: Message) -> None:
    tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)
    await callback_text.send_date_homework(message, tomorrow_date)


# Command: /calendar
@router.message(Command('calendar'))
async def send_calendar_homework(message: Message) -> None:
    await message.answer(
        text=text_message.CHOOSE_DATE.format(date=''),
        reply_markup=await DialogCalendar().start_calendar(month=datetime.datetime.now().month)
    )


# Command: /homework
@router.message(Command('homework'))
async def send_all_homework(message: Message) -> None:
    await message.answer(text=text_message.CHOOSE_SUBJECT, reply_markup=inline_markup.get_all_homework_keyboard())


# Command: /schedule
@router.message(Command('schedule'))
async def send_schedule(message: Message) -> None:
    await message.answer(text=text_message.CHOOSE_WEEKDAY, reply_markup=inline_markup.get_schedule_keyboard())


# Command: /timetable
@router.message(Command('timetable'))
async def send_timetable(message: Message) -> None:
    # Create a timetable from database data
    timetable = '\n'.join(list(map(lambda elem: f'{elem[0] + 1}. <b>{elem[1][0]}</b>', enumerate(get_timetable()))))
    await message.answer(text=text_message.TIMETABLE.format(timetable=timetable))


# Command: /teachers
@router.message(Command('teachers'))
async def send_teachers(message: Message) -> None:
    # Create a teacher list from database data
    teachers_list = '\n'.join(
        list(map(lambda elem: f'{elem[0] + 1}. <b>{elem[1][1]}</b> - {elem[1][0]}', enumerate(get_teachers())))
    )
    await message.answer(text=text_message.TEACHERS.format(teachers_list=teachers_list))


# Command: /support
@router.message(Command('support'))
async def send_support(message: Message) -> None:
    await message.answer(text=text_message.SUPPORT, disable_web_page_preview=True)


# Command: /donate
@router.message(Command('donate'))
async def send_donate(message: Message) -> None:
    await message.answer(text=text_message.DONATE)


# Command: /site
@router.message(Command('site'))
async def send_site(message: Message) -> None:
    await message.answer(text=text_message.SITE, reply_markup=inline_markup.get_site_keyboard())


# Command: /weather
@router.message(Command('weather'))
async def send_weather(message: Message) -> None:
    request = requests.get(
        url='https://api.openweathermap.org/data/2.5/weather?q=Saint%20Petersburg&appid='
            f'{config.weather_API}&units=metric'
    )
    # Check if request is successful
    if request.status_code == 200:
        data = json.loads(request.text)

        # Take weather's data from json
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        wind_speed = data['wind']['speed']

        text_weather = text_message.TEXT_WEATHER.format(
            temperature=temperature, feels_like=feels_like, wind_speed=wind_speed
        )
        # Check for isolated cases of weather
        if 'clear sky' in weather:
            text_weather += text_message.CLEAR_SKY_WEATHER
        elif 'overcast clouds' in weather:
            text_weather += text_message.OVERCAST_CLOUDS_WEATHER
        elif 'rain' in weather:
            text_weather += text_message.RAIN_WEATHER
        elif 'few clouds' in weather:
            text_weather += text_message.FEW_CLOUDS_WEATHER
        elif weather == 'shower rain' or weather == 'thunderstorm':
            text_weather += text_message.SHOWER_RAIN_WEATHER
        elif 'snow' in weather:
            text_weather += text_message.SNOW_WEATHER
        else:
            text_weather += text_message.WEATHER

        await message.answer(text=text_weather)
    else:
        await message.answer(text=text_message.TEXT_ERROR)


# COMMANDS for telegram_bot's admin
# Command: /admin (admin_menu)
@router.message(Command('admin'))
@check_admin
async def send_admin_menu(message: Message, _state: FSMContext = None) -> None:
    await message.answer(text=text_message.ADMIN_GREETINGS)


# Command: /add
# Realize with FSMContext and State
@router.message(Command('add'))
@check_admin
async def send_adding_states(message: Message, state: FSMContext) -> None:
    await homework.register_homework(message, state)


# Command: /edit
@router.message(Command('edit'))
@check_admin
async def send_edit_menu(message: Message, _state: FSMContext = None) -> None:
    await send_all_homework(message)


# Command: /admins
@router.message(Command('admins'))
@check_admin
async def send_admins_menu(message: Message, _state: FSMContext = None) -> None:
    # Create admin_list from database data
    admins_list = ', '.join(list(map(lambda x: x[0], get_users(is_admin=True))))
    await message.answer(text=text_message.ADMINS_LIST.format(admins_list=admins_list),
                         reply_markup=inline_markup.get_admins_keyboard())


# Command: /users
@router.message(Command('users'))
@check_admin
async def send_users_list(message: Message, _state: FSMContext = None) -> None:
    # Create bot's user list from database data
    users_list = ', '.join(list(map(lambda x: x[0], get_users())))
    await message.answer(text=text_message.USERS_LIST.format(users_list=users_list),
                         reply_markup=inline_markup.get_users_keyboard())


# CALLBACKS
# Callback for aiogram_calendar and /calendar
@router.callback_query(DialogCalendarCallback.filter())
async def handle_dialog_calendar(callback: CallbackQuery, callback_data: CallbackData) -> None:
    selected, date = await DialogCalendar().process_selection(callback, callback_data)

    # Check availability of selected date
    if selected:
        await callback_text.send_date_homework(callback, date)


# Handle most of callback's (/menu, /tomorrow, /calendar, /homework etc.)
@router.callback_query(lambda call: call.data in list(callback_text.CALLBACK.values()))
async def handle_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback_text.call_function_from_callback(callback, state)


# Callback for sending date homework (/tomorrow and /calendar)
@router.callback_query(lambda call: 'date' in call.data and 'True' not in call.data)
async def handle_date_homework(callback: CallbackQuery) -> None:
    # Loading data from callback in json format
    date = json.loads(callback.data)['date']
    try:
        first_message = int(json.loads(callback.data)['first_msg'])
        last_message = int(json.loads(callback.data)['last_msg'])
        message_ids = list(range(first_message, last_message))

        await bot.delete_messages(chat_id=callback.message.chat.id, message_ids=message_ids)

    except KeyError:
        pass
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    await callback_text.send_date_homework(callback, date)


# Callback for /homework and subject's buttons
@router.callback_query(lambda call: 'subject' in call.data and 'len' in call.data)
async def handle_homework_pagination(callback: CallbackQuery) -> None:
    # Loading data from callback in json format
    callback_data = json.loads(callback.data)
    length, page, subject = callback_data['len'], int(callback_data['page']), callback_data['subject']

    subject_sticker = get_sticker_by_subject(subject)[0][0]  # Getting subject sticker from database (search by subject)
    homework_data = get_homework_by_subject(subject)  # Getting all subject's homework from database (search by subject)

    date, description, file_id = homework_data[page - 1][2], homework_data[page - 1][3], homework_data[page - 1][4]

    # Check availability of admin using database data
    is_admin = str(callback.message.chat.id) in list(map(lambda x: x[0], get_users(is_admin=True)))
    text = text_message.HOMEWORK_PAGINATION_TEXT.format(subject_sticker=subject_sticker, subject_name=subject,
                                                        date=date, description=description)
    markup = inline_markup.get_homework_pagination(length, page, subject, is_admin)
    await callback.message.delete()

    if file_id != 'None':
        await bot.send_photo(caption=text, reply_markup=markup, photo=file_id, chat_id=callback.message.chat.id)
    else:
        await callback.message.answer(text=text, reply_markup=markup)


# Callback for /schedule
@router.callback_query(lambda call: 'weekday_id' in call.data)
async def handle_schedule(callback: CallbackQuery) -> None:
    # Loading data from callback in json format
    callback_data = json.loads(callback.data)
    weekday_id = int(callback_data['weekday_id'][0])

    # Checking for next day after Saturday and for previous day before Monday
    new_weekday_id = 1 if weekday_id == 7 else 6 if weekday_id == 0 else weekday_id
    weekday_name = get_weekend(new_weekday_id)[0][0]
    weekday_name_rus = text_message.SCHEDULE_DICTIONARY_RUS[weekday_name]  # Translate weekday_name to Russian
    morph = pymorphy3.MorphAnalyzer()
    weekday_name_rus = morph.parse(weekday_name_rus)[0].inflect({'accs'}).word

    # Create schedule_text from database data
    schedule_text = '\n'.join(
        list(map(lambda elem: f'{elem[0] + 1}. {elem[1][0]}' if elem[1][0] is not None else f'{elem[0] + 1}. Нет урока',
                 enumerate(get_schedule(weekday_name))))
    )

    await callback.message.edit_text(
        text=text_message.SCHEDULE_TEXT.format(weekday_name=weekday_name_rus, schedule=schedule_text),
        reply_markup=inline_markup.get_weekday_keyboard(new_weekday_id)
    )


# Callback for /admins
@router.callback_query(lambda call: 'admin' in call.data)
async def handle_edit_admins(callback: CallbackQuery, state: FSMContext) -> None:
    # Checking availability of admin's active
    is_active = True if callback.data == 'add_admin' else False
    await admins.register_admins(callback.message, state, is_active)


# Callback for /edit, also for /homework
@router.callback_query(lambda call: 'edit' in call.data)
async def handle_edit_data(callback: CallbackQuery, state: FSMContext) -> None:
    # Loading data from callback in json format
    callback_data = json.loads(callback.data)
    homework_id = callback_data['id']
    await state.clear()
    await edit_homework.process_edit_homework(callback.message, state, homework_id)


# Callback for /delete
@router.callback_query(lambda call: 'delete' in call.data)
async def handle_delete_data(callback: CallbackQuery) -> None:
    try:
        # Loading data from callback in json format
        callback_data = json.loads(callback.data)
        delete_homework(callback_data['id'])
        await callback.message.delete()
        await callback.message.answer(text_message.DELETE_HOMEWORK)

    except KeyError:
        await callback.message.answer(text_message.INCORRECT_REQUEST)


# Handle all other text messages from telegram user
@router.message()
async def handle_text(message: Message) -> None:
    await message.answer(text=text_message.RANDOM_TEXT_FROM_USER, reply_markup=inline_markup.get_random_text_keyboard())
