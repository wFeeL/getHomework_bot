import json
import random

import pymorphy3
import requests
from aiogram import Router, Bot, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram_dialog import DialogManager, setup_dialogs, StartMode

from telegram_bot import text_message, callback_text
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import *
from telegram_bot.decorators import check_admin, check_class
from telegram_bot.keyboards import inline_markup
from telegram_bot.states import edit_admins, edit_homework, add_homework, calendar

router = Router()  # Create a router for bot's commands
router.include_router(calendar.dialog)  # Include calendar router (dialog window from aiogram_dialog)
setup_dialogs(router)  # Setup router's dialog
bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


# COMMANDS for telegram user
# Command: /start
@router.message(Command('start'))
async def send_greetings(message: Message, **kwargs) -> None:
    """
    Send greetings.
    Register user if not exists and choose class.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    # Get user info
    user_telegram_id = message.chat.id
    user_telegram_name = message.chat.first_name

    # Check availability of user's registration
    if len(get_users()) == 0 or str(user_telegram_id) not in list(map(lambda x: x[0], get_users())):
        add_user(telegram_id=user_telegram_id)  # Register user to database

    # Check availability of user's class
    if get_users(telegram_id=user_telegram_id)[0][1] == 0:
        # Send message with choosing class
        markup = inline_markup.get_start_keyboard(is_class=False)
        text = text_message.GREETINGS.format(user=user_telegram_name, class_text=text_message.CLASS_NOT_CHOSEN)
    else:
        # Get class from database (user registration and choosing is success)
        class_id = get_users(telegram_id=user_telegram_id)[0][1]
        class_data = get_class(id=class_id)[0]
        letter, number = class_data[1], class_data[2]

        markup = inline_markup.get_start_keyboard()
        text = text_message.GREETINGS.format(user=user_telegram_name,
                                             class_text=text_message.CLASS_CHOSEN.format(number=number, letter=letter))

    await message.answer(text=text, reply_markup=markup)


# Command: /help
@router.message(Command('help'))
async def send_help(message: Message, **kwargs) -> None:
    """
        Send help text.
        Suggest to choose class.

        :param message: Message
        :param kwargs: Other message options (need for callback function)
    """
    # Check availability of user's class
    if get_users(telegram_id=message.chat.id)[0][1] == 0:
        markup = inline_markup.get_help_keyboard(is_class=False)
        text = text_message.HELP.format(class_text=text_message.CLASS_NOT_CHOSEN)
    else:
        # Get class from database (user registration and choosing is success)
        class_id = get_users(telegram_id=message.chat.id)[0][1]
        class_data = get_class(id=class_id)[0]
        letter, number = class_data[1], class_data[2]

        markup = inline_markup.get_help_keyboard()
        text = text_message.HELP.format(class_text=text_message.CLASS_CHOSEN.format(number=number, letter=letter))
    await message.answer(text=text, reply_markup=markup)


# Command: /menu
@router.message(Command('menu'))
@check_class
async def send_menu(message: Message, **kwargs) -> None:
    """
    Send homework search menu.

    Include /tomorrow, /calendar and /homework commands.
    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    await message.answer(text=text_message.CHOOSE_CATEGORY, reply_markup=inline_markup.get_homework_menu())


# Command: /tomorrow
@router.message(Command('tomorrow'))
@check_class
async def send_tomorrow_homework(message: Message, **kwargs) -> None:
    """
    Send tomorrow homework.
    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)
    await send_date_homework(message, tomorrow_date)


# Command: /homework
@router.message(Command('homework'))
@check_class
async def send_all_homework(message: Message, **kwargs) -> None:
    """
    Send list of subjects from database.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    class_id = get_users(telegram_id=message.chat.id)[0][1]

    await message.answer(text=text_message.CHOOSE_SUBJECT,
                         reply_markup=inline_markup.get_all_homework_keyboard(class_id))


# Command: /calendar
@router.message(Command('calendar'))
@check_class
async def send_calendar_homework(_message: Message, dialog_manager: DialogManager, **kwargs) -> None:
    """
    Send dated homework.

    :param _message: Need for callback function
    :param dialog_manager: Need for start the dialog
    :param kwargs: Other message options (need for callback function)
    """
    await dialog_manager.start(state=calendar.CalendarHomework.calendar, mode=StartMode.RESET_STACK)


# Command: /class
@router.message(Command('class'))
async def send_class(message: Message, **kwargs) -> None:
    """
    Send list of classes from database

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    if get_users(telegram_id=message.chat.id)[0][1] == 0:
        text = text_message.CHOOSE_CLASS
    else:
        class_id = get_users(telegram_id=message.chat.id)[0][1]
        class_len = len(get_users(class_id=class_id))
        class_data = get_class(id=class_id)[0]
        letter, number = class_data[1], class_data[2]

        text = text_message.CLASS.format(number=number, letter=letter, class_len=class_len)
    await message.answer(text=text, reply_markup=inline_markup.get_class_keyboard())


# Command: /schedule
@router.message(Command('schedule'))
@check_class
async def send_schedule(message: Message, **kwargs) -> None:
    """
    Send list of weekday's from database

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    class_id = get_users(telegram_id=message.chat.id)[0][1]
    await message.answer(text=text_message.CHOOSE_WEEKDAY, reply_markup=inline_markup.get_schedule_keyboard(class_id))


# Command: /timetable
@router.message(Command('timetable'))
async def send_timetable(message: Message, **kwargs) -> None:
    """
    Send timetable text.
     Created by database.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    # Create a timetable from database data
    timetable = '\n'.join(list(map(lambda elem: f'{elem[0] + 1}. <b>{elem[1][0]}</b>', enumerate(get_timetable()))))
    await message.answer(text=text_message.TIMETABLE.format(timetable=timetable))


# Command: /teachers
@router.message(Command('teachers'))
@check_class
async def send_teachers(message: Message, **kwargs) -> None:
    """
    Send list of teachers.
    Created by database.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    class_id = get_users(telegram_id=message.chat.id)[0][1]

    # Create a teacher list from database data
    teachers_list = '\n'.join(
        list(map(lambda elem: f'{elem[0] + 1}. <b>{elem[1][1]}</b> - {elem[1][0]}', enumerate(get_teachers(class_id))))
    )
    await message.answer(text=text_message.TEACHERS.format(teachers_list=teachers_list))


# Command: /support
@router.message(Command('support'))
async def send_support(message: Message, **kwargs) -> None:
    """
    Send support text.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    await message.answer(text=text_message.SUPPORT, disable_web_page_preview=True)


# Command: /donate
@router.message(Command('donate'))
async def send_donate(message: Message, **kwargs) -> None:
    """
    Send donate text.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    await message.answer(text=text_message.DONATE)


# Command: /site
@router.message(Command('site'))
async def send_site(message: Message, **kwargs) -> None:
    """
    Send site text.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    await message.answer(text=text_message.SITE, reply_markup=inline_markup.get_site_keyboard())


# Command: /weather
@router.message(Command('weather'))
async def send_weather(message: Message, **kwargs) -> None:
    """
    Send weather text.
    Use weather API to create GET-request and unparse data.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    request = requests.get(
        url=f'http://api.weatherapi.com/v1/current.json?key={config.weather_API}&q=Saint Petersburg&aqi=no&lang=ru'
    )
    # Check if request is successful
    if request.status_code == 200:
        data = json.loads(request.text)['current']
        temperature_c = data['temp_c']
        humidity = data['humidity']
        wind_speed = data['wind_mph']
        wind_dir = data['wind_dir']

        weather_icon = data['condition']['icon']
        weather_code = data['condition']['code']
        weather_icon_link = "cdn.weatherapi.com/weather/128x128/" + '/'.join(weather_icon.split('/')[-2:])

        text_weather = text_message.TEXT_WEATHER.format(
            temperature=temperature_c, wind_speed=wind_speed, humidity=humidity, wind_dir=wind_dir
        )

        # Check for isolated cases of weather
        if weather_code == 1000:
            text_weather += text_message.CLEAR_SKY_WEATHER

        elif weather_code in [1009, 1030, 1063]:
            text_weather += text_message.OVERCAST_CLOUDS_WEATHER

        elif weather_code in [1072, 1135, 1147, 1150, 1153, 1180, 1183, 1198, 1201, 1261]:
            text_weather += text_message.RAIN_WEATHER

        elif weather_code in [1003, 1006]:
            text_weather += text_message.FEW_CLOUDS_WEATHER

        elif weather_code in [1087, 1186, 1189, 1192, 1195, 1227, 1240, 1243, 1246, 1264, 1273, 1276]:
            text_weather += text_message.SHOWER_RAIN_WEATHER

        elif weather_code in [1066, 1069, 1114, 1117, 1168, 1171, 1204, 1207, 1210, 1213, 1216, 1219, 1222, 1225,
                              1249, 1252, 1255, 1258, 1279, 1282]:
            text_weather += text_message.SNOW_WEATHER

        else:
            text_weather += text_message.WEATHER

        await bot.send_photo(photo=weather_icon_link, caption=text_weather, chat_id=message.chat.id)
    else:
        await message.answer(text=text_message.TEXT_ERROR)


# COMMANDS for telegram_bot's admin
# Command: /admin
@router.message(Command('admin'))
@check_admin
async def send_admin_menu(message: Message, **kwargs) -> None:
    """
    Send admin text.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    class_id = get_admins(telegram_id=message.chat.id)[0][4]
    class_data = get_class(id=class_id)[0]
    letter, number = class_data[1], class_data[2]

    await message.answer(text=text_message.ADMIN_GREETINGS.format(
        class_text=text_message.CLASS_CHOSEN.format(number=number, letter=letter))
    )


# Command: /add
@router.message(Command('add'))
@check_admin
async def send_adding_states(message: Message, state: FSMContext, **kwargs) -> None:
    """
    Start adding homework.
    Use state for gather homework's data.

    :param message: Message
    :param state: FSMContext
    :param kwargs: Other message options (need for callback function)
    """
    await add_homework.register_homework(message, state)


# Command: /edit
@router.message(Command('edit'))
@check_admin
async def send_edit_menu(message: Message, **kwargs) -> None:
    """
    Send list of subject from database (call /homework)

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """

    class_id = get_admins(telegram_id=message.chat.id)[0][4]

    await message.answer(text=text_message.CHOOSE_SUBJECT,
                         reply_markup=inline_markup.get_all_homework_keyboard(class_id))


# Command: /admins
# Command is only for super admins (count: 1)
@router.message(Command('admins'))
@check_admin
async def send_admins_menu(message: Message, **kwargs) -> None:
    """
    Send list of admins.
    Only for super admins.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    # Create admin_list from database data
    admin_id = str(message.chat.id)
    if admin_id in list(map(lambda x: x[0], get_admins(value=True, super_admin=True))):
        admins_list = list(map(lambda x: x[0], get_admins(value=True)))
        text = text_message.ADMINS_LIST
        count = 0

        for admin in admins_list:
            try:
                user_chat = await bot.get_chat(chat_id=admin)
                if user_chat.username is not None:
                    count += 1
                    class_id = get_admins(telegram_id=admin)[0][1]
                    class_data = get_class(id=class_id)[0]
                    letter, number = class_data[1], class_data[2]
                    text += text_message.ADMIN_FORM.format(index=count, name=user_chat.first_name,
                                                           username=user_chat.username, letter=letter, number=number)
            except TelegramBadRequest:
                pass
        await message.answer(text=text, reply_markup=inline_markup.get_admins_keyboard())
    else:
        await handle_text(message, **kwargs)


# Command: /users
@router.message(Command('users'))
@check_admin
async def send_users_list(message: Message, **kwargs) -> None:
    """
    Send list of users.
    Created by database.

    :param message: Message
    :param kwargs: Other message options (need for callback function)
    """
    # Create bot's user list from database data
    users_list = list(map(lambda x: x[0], get_users()))
    text = text_message.USERS_LIST
    count = 0

    for user in users_list:
        try:
            user_chat = await bot.get_chat(chat_id=user)
            if user_chat.username is not None:
                count += 1
                is_admin = str(user) in list(map(lambda x: x[0], get_admins(value=True)))
                admin_text = '<b>Администратор</b>' if is_admin else ''
                text += text_message.USER_FORM.format(index=count, is_admin=admin_text, name=user_chat.first_name,
                                                      username=user_chat.username)
        except TelegramBadRequest:
            pass

    text += text_message.LEN_USERS.format(len_users_list=count)
    await message.answer(text=text, reply_markup=inline_markup.get_users_keyboard())


# CALLBACKS
# Handle most of callback's (/menu, /tomorrow, /calendar, /homework etc.)
@router.callback_query(lambda call: call.data in list(callback_text.CALLBACK.values()))
async def handle_callback(callback: CallbackQuery, **kwargs) -> None:
    """
    Handle callback to call function.

    :param callback: Callback
    :param kwargs: Other message options (need for callback function)
    """
    await callback.message.delete()
    await callback_text.call_function_from_callback(callback, **kwargs)


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
    await send_date_homework(callback, date)


# Callback for /homework and subject's buttons
@router.callback_query(lambda call: 'page' in call.data and 'len' in call.data)
async def handle_homework_pagination(callback: CallbackQuery) -> None:
    try:
        # Loading data from callback in json format
        callback_data = json.loads(callback.data)
        length, page, subject_id = int(callback_data['len']), int(callback_data['page']), callback_data['subject_id']

        class_id = get_users(telegram_id=callback.message.chat.id)[0][1]

        subject = get_subject(id=subject_id, class_ids=class_id)[0]
        subject_name = subject[1]
        subject_sticker = subject[2]
        # Getting all subject's homework from database (search by subject)
        homework_data = get_homework(subject_id=subject_id, class_id=class_id)

        date, description, file_id = homework_data[page - 1][2], homework_data[page - 1][3], homework_data[page - 1][4]
        date = date.strftime("%d.%m.%Y")
        # Check availability of admin using database data
        is_admin = str(callback.message.chat.id) in list(map(lambda x: x[0], get_admins(value=True, class_id=class_id)))
        text = text_message.HOMEWORK_PAGINATION_TEXT.format(subject_sticker=subject_sticker, subject_name=subject_name,
                                                            date=date, description=description)
        markup = inline_markup.get_homework_pagination(length=length, page=page,
                                                       subject_id=subject_id, is_admin=is_admin, class_id=class_id)
        await callback.message.delete()

        if file_id != 'None':
            await bot.send_photo(caption=text, reply_markup=markup, photo=file_id, chat_id=callback.message.chat.id)
        else:
            await callback.message.answer(text=text, reply_markup=markup)

    except IndexError:
        await callback.message.answer(text_message.TEXT_ERROR, reply_markup=inline_markup.get_delete_message_keyboard())


# Callback for /schedule
@router.callback_query(lambda call: 'weekday_id' in call.data)
async def handle_schedule(callback: CallbackQuery) -> None:
    # Loading data from callback in json format
    callback_data = json.loads(callback.data)
    weekday_id = int(callback_data['weekday_id'][0])

    class_id = get_users(telegram_id=callback.message.chat.id)[0][1]
    class_weekend = get_weekday(class_ids=class_id)
    min_weekday_id = class_weekend[0][0]
    max_weekday_id = len(class_weekend)

    if weekday_id == max_weekday_id + 1:
        weekday_id = min_weekday_id

    elif weekday_id == min_weekday_id - 1:
        weekday_id = max_weekday_id

    weekday_name = get_weekday(id=weekday_id, class_ids=class_id)[0][1]
    weekday_name_rus = text_message.SCHEDULE_DICTIONARY_RUS[weekday_name]  # Translate weekday_name to Russian
    morph = pymorphy3.MorphAnalyzer()
    weekday_name_rus = morph.parse(weekday_name_rus)[0].inflect({'accs'}).word

    # Create schedule_text from database data
    schedule_text = '\n'.join(
        list(map(lambda elem: f'{elem[0] + 1}. {elem[1][0]}' if elem[1][0] is not None else f'{elem[0] + 1}. Нет урока',
                 enumerate(get_schedule(weekday_name, class_id))))
    )

    await callback.message.edit_text(
        text=text_message.SCHEDULE_TEXT.format(weekday_name=weekday_name_rus, schedule=schedule_text),
        reply_markup=inline_markup.get_weekday_keyboard(weekday_id)
    )


# Callback for /class
@router.callback_query(lambda call: 'class_id' in call.data)
async def handle_class(callback: CallbackQuery) -> None:
    # Loading data from callback in json format
    callback_data = json.loads(callback.data)
    class_id = int(callback_data['class_id'][0])
    update_user_class(telegram_id=callback.message.chat.id, class_id=class_id)
    class_data = get_class(id=class_id)[0]
    letter, number = class_data[1], class_data[2]
    await callback.message.edit_text(text=text_message.UPDATE_CLASS_SUCCESSFUL.format(number=number, letter=letter),
                                     reply_markup=inline_markup.get_search_homework_keyboard())


# Callback for /admins
@router.callback_query(lambda call: 'admin' in call.data)
async def handle_edit_admins(callback: CallbackQuery, state: FSMContext) -> None:
    # Checking availability of admin's active
    is_active = True if callback.data == 'add_admin' else False
    await edit_admins.edit_admins(callback.message, state, is_active)


# Callback for /edit, also for /homework (edit homework -> date, description and file)
@router.callback_query(lambda call: 'homework_id' in call.data and 'edit' in call.data)
async def handle_edit_data(callback: CallbackQuery, state: FSMContext) -> None:
    # Loading data from callback in json format
    callback_data = json.loads(callback.data)
    homework_id = callback_data['homework_id']
    await state.clear()
    await callback.message.delete()
    await edit_homework.update_edit_data(callback.message, state, homework_id)


# Callback for /edit (delete homework)
@router.callback_query(lambda call: 'homework_id' in call.data and 'delete' in call.data)
async def handle_delete_data(callback: CallbackQuery) -> None:
    try:
        # Loading data from callback in json format
        callback_data = json.loads(callback.data)
        delete_homework(callback_data['homework_id'])
        await callback.message.delete()
        await callback.message.answer(text_message.DELETE_HOMEWORK)

    except KeyError:
        await callback.message.answer(text_message.INCORRECT_REQUEST,
                                      reply_markup=inline_markup.get_delete_message_keyboard())


# Delete message
@router.callback_query(F.data == 'delete_message')
async def delete_message(callback: CallbackQuery) -> None:
    await callback.message.delete()


# Handle all other text messages from telegram user
@router.message()
async def handle_text(message: Message, **kwargs) -> None:
    await message.answer(text=text_message.RANDOM_TEXT_FROM_USER, reply_markup=inline_markup.get_random_text_keyboard())


# Send a date homework from callback data (take data and return homework data). Commands: /calendar and /tomorrow
async def send_date_homework(message: Message | CallbackQuery, date: datetime, **kwargs) -> None:
    if type(message) is CallbackQuery:
        message = message.message
        await message.delete()

    class_id = get_users(telegram_id=message.chat.id)[0][1]

    # homework_data = get_homework_by_date(date, class_id)
    homework_data = get_homework(date=date, class_id=class_id)
    markup = inline_markup.get_calendar_keyboard(date, None)

    morph = pymorphy3.MorphAnalyzer()
    weekday_name = morph.parse(date.strftime('%A'))[0].inflect({'accs'}).word
    date_text = date.strftime("%d.%m.%Y")

    if len(homework_data) > 0:

        homework_text = text_message.HOMEWORK_TO_SELECTED_DATE.format(f'{weekday_name} {date_text}')

        for i in range(len(homework_data)):
            subject_name = get_subject(id=homework_data[i][1], class_ids=class_id)[0][1]
            subject_description = str(homework_data[i][3])

            homework_text += text_message.HOMEWORK_TEXT.format(
                sequence_number=i + 1, subject_name=subject_name,
                subject_description=subject_description
            )
        photos = list(map(lambda elem: elem[4], filter(lambda elem: elem[4] != 'None', homework_data)))

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
        quote_data = get_quotes(value=True)
        index = random.randint(0, len(quote_data) - 1)
        quote_data = quote_data[index]
        quote, author = quote_data[0], quote_data[1]
        text = text_message.HOMEWORK_IS_NULL.format(date=f'{weekday_name} {date_text}', quote=quote, author=author)
        await message.answer(text=text, reply_markup=markup)
