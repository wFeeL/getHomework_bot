from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot.handlers.bot_commands import *
from telegram_bot.database_methods.database_request import *


# Inline keyboard button for common telegram user
def get_menu_button(text='🔄 Главное меню') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data='menu')]
    return button


def get_help_button(text='❓ Помощь') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data='help')]
    return button


def get_support_button(text='🔰 Поддержка') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, url='https://t.me/wfeels')]
    return button


def get_donate_button(text='💰 Донат') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, url='https://www.tinkoff.ru/rm/saburov.daniil23/TTzup21621')]
    return button


# Inline keyboard button for admin
def get_admin_menu_button() -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text='🔄 Главное меню',
                                   callback_data=callback_text.CALLBACK['send_admin_menu'])]
    return button


# Inline markups for common telegram user
# Create a start keyboard for /start command
def get_start_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[get_menu_button('🔍 Открыть меню поиска'), get_donate_button(),
                         get_support_button('🔰 Разработчик')]
    )
    return markup


# Create a help keyboard for /help command
def get_help_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[get_donate_button('💰Поддержать автора'), get_support_button()])
    return markup


# Create a homework_menu keyboard for /menu
def get_homework_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✍ Задания на завтра',
                                  callback_data=callback_text.CALLBACK[send_tomorrow_homework.__name__])],
            [InlineKeyboardButton(text='📅 Календарь заданий',
                                  callback_data=callback_text.CALLBACK[send_calendar_homework.__name__])],
            [InlineKeyboardButton(text='⚜ Все домашние задания',
                                  callback_data=callback_text.CALLBACK[send_all_homework.__name__])]]
    )
    return markup


# Create an all homework keyboard for /homework
def get_all_homework_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    subjects = get_subjects()

    for i in range(len(subjects)):
        data = get_homework_by_subject(subjects[i][0])
        subject_name = subjects[i][0]
        subject_sticker = get_sticker_by_subject(subject_name)[0][0]
        data_length = len(data)

        builder.row(InlineKeyboardButton(text=f'{subject_sticker} {subjects[i][0]}',
                                         callback_data="{\"subject\":\"" + str(subject_name) +
                                                       f"\",\"page\":\"{data_length}\",\"len\":"
                                                       + str(data_length) + "}"))
    builder.row(get_menu_button()[0])
    return builder.as_markup()


# Create homework pagination keyboard for callback of /homework, also for /edit
def get_homework_pagination(length, page, subject_name, is_admin=False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    next_button = InlineKeyboardButton(text='Вперед ▶',
                                       callback_data="{\"subject\":\"" + str(subject_name) +
                                                     "\",\"page\":" + str(page + 1) + ",\"len\":"
                                                     + str(length) + "}")
    back_button = InlineKeyboardButton(text='◀ Назад',
                                       callback_data="{\"subject\":\"" + str(subject_name) + "\",\"page\":" +
                                                     str(page - 1) + ",\"len\":" + str(length) + "}")

    count_button = InlineKeyboardButton(text=f'{page}/{length}', callback_data='None')

    menu_button = InlineKeyboardButton(text='🔄 К выбору предметов',
                                       callback_data=callback_text.CALLBACK[send_all_homework.__name__])

    if page == 1 and length == 1:
        builder.add(count_button)

    elif page == 1:
        builder.add(count_button, next_button)

    elif page == length:
        builder.add(back_button, count_button)

    else:
        builder.add(back_button, count_button, next_button)

    builder.adjust(3, 1)
    if is_admin:
        homework_id = int(get_homework_id_by_subject(subject_name)[page - 1][0])

        edit_button = InlineKeyboardButton(
            text='📝 Изменить домашнее задание', callback_data="{\"id\":" + str(homework_id) + ",\"edit\":\"True\"}")
        delete_button = InlineKeyboardButton(
            text='🗑️ Удалить домашнее задание', callback_data="{\"id\":" + str(homework_id) + ",\"delete\":\"True\"}")
        builder.row(edit_button)
        builder.row(delete_button)

    builder.row(menu_button)

    return builder.as_markup()


# Create schedule keyboard for /schedule
def get_schedule_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    weekend = get_weekend()

    for i in range(len(weekend)):
        weekday_name = weekend[i][1]
        weekday_id = i + 1
        builder.row(InlineKeyboardButton(text=f'{text_message.SCHEDULE_DICTIONARY_RUS[weekday_name]}'.capitalize(),
                                         callback_data="{\"weekday_id\":\"" + f"{weekday_id}" + "\"}"))

    return builder.as_markup()


# Create schedule's day for buttons of /schedule
def get_weekday_keyboard(weekday_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='◀ Назад', callback_data="{\"weekday_id\":\"" + f"{weekday_id - 1}" + "\"}"),
         InlineKeyboardButton(text='Вперед ▶', callback_data="{\"weekday_id\":\"" + f"{weekday_id + 1}" + "\"}")],
        [InlineKeyboardButton(text='🔄 Главное меню', callback_data=callback_text.CALLBACK[send_schedule.__name__])]
    ])
    return markup


# Create site keyboard for /site
def get_site_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Перейти по ссылке', url='https://petersburgedu.ru/')]]
    )
    return markup


# Create calendar keyboard for callback of /calendar
def get_calendar_keyboard(selected_date, media_group: tuple[int, int] = None) -> InlineKeyboardMarkup:
    next_date = datetime.datetime.strftime(selected_date + datetime.timedelta(days=1), '%Y-%m-%d')
    previous_date = datetime.datetime.strftime(selected_date - datetime.timedelta(days=1), '%Y-%m-%d')

    if media_group is None:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                get_menu_button(),
                [InlineKeyboardButton(text='◀ Назад', callback_data="{\"date\":\"" + f"{previous_date}" + "\"}"),
                 InlineKeyboardButton(text='Вперед ▶', callback_data="{\"date\":\"" + f"{next_date}" + "\"}")]
            ])
    else:
        first_message_id = media_group[0]
        last_message_id = first_message_id + media_group[1]
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                get_menu_button(),
                [InlineKeyboardButton(
                    text='◀ Назад',
                    callback_data="{" + f"\"date\":\"{previous_date}\",\"first_msg\":\"{first_message_id}\","
                                        f"\"last_msg\":\"{last_message_id}\"" + "}"),
                    InlineKeyboardButton(
                        text='Вперед ▶',
                        callback_data="{" + f"\"date\":\"{next_date}\",\"first_msg\":\"{first_message_id}\","
                                            f"\"last_msg\":\"{last_message_id}\"" + "}")],
            ])
    return markup


def get_random_text_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        get_menu_button(), get_help_button(), get_support_button()
    ])
    return markup


# Inline markup for admin
# Create admins_keyboard for /admins (admin function)
def get_admins_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Добавить администратора', callback_data='add_admin')],
            [InlineKeyboardButton(text='Удалить администратора', callback_data='delete_admin')],
            get_admin_menu_button()
        ])
    return markup


def get_admin_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[get_admin_menu_button()])
    return markup


# Create send_homework keyboard for /add
def get_send_hw_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✅ Отправить данные', callback_data='send_data')],
            [InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_send_data')]
        ])
    return markup


# Create cancel keyboard for /edit
def get_cancel_keyboard(data: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🚫 Отмена', callback_data=f'cancel_{data}')]
        ])
    return markup


# Create edit keyboard for /edit (editing menu for homework's data)
def get_edit_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Редактировать дату', callback_data='edit_date')],
            [InlineKeyboardButton(text='Изменить описание', callback_data='edit_description')],
            [InlineKeyboardButton(text='Прикрепить изображение', callback_data='edit_file')],
            [InlineKeyboardButton(text='Обновить данные', callback_data='edit_data')]
        ])
    return markup


def get_skip_file_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Пропустить выбор фото', callback_data='skip_file')]
        ])
    return markup


def get_users_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[get_admin_menu_button()])
    return markup
