from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram_bot import callback_text, text_message
from telegram_bot.database_methods.database_request import get_subject, get_homework, get_weekday, get_class


# Inline keyboard button for common telegram user
def get_homework_menu_button(text='🔄 Главное меню', ) -> list[InlineKeyboardButton]:
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


def get_class_button(text='👤 Выбрать класс') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data=callback_text.CALLBACK['send_class'])]
    return button


def get_calendar_homework_button(text='🗓 Выбрать дату') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data=callback_text.CALLBACK['send_calendar_homework'])]
    return button


# Inline keyboard button for admin
def get_admin_menu_button() -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text='🔄 Главное меню',
                                   callback_data=callback_text.CALLBACK['send_admin_menu'])]
    return button


def get_add_homework_button() -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text='Добавить домашнее задание',
                                   callback_data=callback_text.CALLBACK['send_adding_states'])]
    return button


def get_delete_message_button(text='👀 Скрыть') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data='delete_message')]
    return button


def get_stop_state_button(text='👀 Скрыть') -> list[InlineKeyboardButton]:
    button = [InlineKeyboardButton(text=text, callback_data='stop_state')]
    return button


# def make_button(
#         text: str,
#         callback_data: str,
#         is_markup: bool = False
# ) -> list[InlineKeyboardButton] | InlineKeyboardMarkup:
#     button = [InlineKeyboardButton(text=text, callback_data=callback_data)]
#     return button if not is_markup else InlineKeyboardMarkup(inline_keyboard=[button])


# Inline markups for common telegram user
# Create a start keyboard for /start command
def get_start_keyboard(is_class: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if not is_class:
        builder.add(get_class_button()[0])
    else:
        builder.add(get_homework_menu_button('🔍 Открыть меню поиска')[0])

    builder.add(get_donate_button()[0], get_support_button('🔰 Разработчик')[0])
    builder.adjust(1, 2)
    return builder.as_markup()


# Create a help keyboard for /help command
def get_help_keyboard(is_class: bool = True) -> InlineKeyboardMarkup:
    keyboard = []
    if not is_class:
        keyboard.append(get_class_button())
    keyboard += [get_donate_button('💰Поддержать автора'), get_support_button()]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Create a homework_menu keyboard for /menu
def get_homework_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✍ Задания на завтра',
                                  callback_data=callback_text.CALLBACK['send_tomorrow_homework'])],
            get_calendar_homework_button(text='🗓️ Календарь заданий'),
            [InlineKeyboardButton(text='⚜ Все домашние задания',
                                  callback_data=callback_text.CALLBACK['send_all_homework'])]]
    )
    return markup


# Create an all homework keyboard for /homework
def get_all_homework_keyboard(class_id: int | str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    subjects = get_subject(class_ids=class_id)

    for i in range(len(subjects)):
        subject_id, subject_name, subject_sticker = subjects[i][0], subjects[i][1], subjects[i][2]
        data = get_homework(subject_id=subject_id, class_id=class_id)
        data_length = len(data)

        builder.row(InlineKeyboardButton(text=f'{subject_sticker} {subject_name}',
                                         callback_data="{\"subject_id\":\"" + str(subject_id) +
                                                       f"\",\"page\":\"{data_length}\",\"len\":"
                                                       + str(data_length) + "}"))
    builder.row(get_homework_menu_button()[0])
    return builder.as_markup()


# Create homework pagination keyboard for callback of /homework, also for /edit
def get_homework_pagination(length: int, page: int, subject_id: int | str,
                            class_id: int = None, is_admin: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    next_button = InlineKeyboardButton(text='Вперед ▶',
                                       callback_data="{\"subject_id\":\"" + str(subject_id) +
                                                     "\",\"page\":" + str(page + 1) + ",\"len\":"
                                                     + str(length) + "}")
    back_button = InlineKeyboardButton(text='◀ Назад',
                                       callback_data="{\"subject_id\":\"" + str(subject_id) + "\",\"page\":" +
                                                     str(page - 1) + ",\"len\":" + str(length) + "}")

    count_button = InlineKeyboardButton(text=f'{page}/{length}', callback_data='None')

    menu_button = InlineKeyboardButton(text='🔄 К выбору предметов',
                                       callback_data=callback_text.CALLBACK['send_all_homework'])
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
        # homework_id = int(get_homework_id_by_subject(subject_name, class_id)[page - 1][0])
        homework_id = int(get_homework(subject_id=subject_id, class_id=class_id)[page - 1][0])

        edit_button = InlineKeyboardButton(
            text='📝 Изменить домашнее задание', callback_data="{\"homework_id\":" + str(homework_id) +
                                                              ",\"edit\":\"True\"}")
        delete_button = InlineKeyboardButton(
            text='🗑️ Удалить домашнее задание', callback_data="{\"homework_id\":" + str(homework_id) +
                                                              ",\"delete\":\"True\"}")
        builder.row(edit_button)
        builder.row(delete_button)

    builder.row(menu_button)

    return builder.as_markup()


# Create schedule keyboard for /schedule
def get_schedule_keyboard(class_id: int | str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    weekend = get_weekday(class_ids=class_id)

    for i in range(len(weekend)):
        weekday_id = weekend[i][0]
        weekday_name = weekend[i][1]
        builder.row(InlineKeyboardButton(text=f'{text_message.SCHEDULE_DICTIONARY_RUS[weekday_name]}'.capitalize(),
                                         callback_data="{\"weekday_id\":\"" + f"{weekday_id}" + "\"}"))

    return builder.as_markup()


# Create class keyboard for /class
def get_class_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    classes = get_class()

    for elem in classes:
        class_id, letter, number = elem[0], elem[1], elem[2]
        builder.row(InlineKeyboardButton(text=f'{number} {letter}',
                                         callback_data="{\"class_id\":\"" + f"{class_id}" + "\"}"))
    return builder.as_markup()


# Create schedule's day for buttons of /schedule
def get_weekday_keyboard(weekday_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='◀ Назад', callback_data="{\"weekday_id\":\"" + f"{weekday_id - 1}" + "\"}"),
         InlineKeyboardButton(text='Вперед ▶', callback_data="{\"weekday_id\":\"" + f"{weekday_id + 1}" + "\"}")],
        [InlineKeyboardButton(text='🔄 Выбрать день', callback_data=callback_text.CALLBACK['send_schedule'])]
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
    next_date = datetime.strftime(selected_date + timedelta(days=1), '%Y-%m-%d')
    previous_date = datetime.strftime(selected_date - timedelta(days=1), '%Y-%m-%d')

    if media_group is None:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                get_calendar_homework_button(),
                get_homework_menu_button(),
                [InlineKeyboardButton(text='◀ Назад', callback_data="{\"date\":\"" + f"{previous_date}" + "\"}"),
                 InlineKeyboardButton(text='Вперед ▶', callback_data="{\"date\":\"" + f"{next_date}" + "\"}")]
            ])
    else:
        first_message_id = media_group[0]
        last_message_id = first_message_id + media_group[1]
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                get_calendar_homework_button(),
                get_homework_menu_button(),
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
        get_homework_menu_button('🔍 Поиск домашнего задания'), get_help_button(), get_support_button(),
        get_delete_message_button()
    ])
    return markup


# Create keyboard for deleting error's message and etc.
def get_delete_message_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[get_delete_message_button()])
    return markup


# Create search homework keyboard
def get_search_homework_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[get_homework_menu_button('🔍 Открыть меню поиска')])
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
    markup = InlineKeyboardMarkup(inline_keyboard=[get_add_homework_button(), get_admin_menu_button()])
    return markup


# Create send_homework keyboard for /add
def get_send_homework_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✅ Сохранить данные', callback_data='send_data')],
            [InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel_send_data')]
        ])
    return markup


# Create edit keyboard for /edit (editing menu for homework's data)
def get_edit_keyboard(is_file: bool = True, is_edited: bool = False) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(text='🗓️ Редактировать дату', callback_data='edit_date')],
                [InlineKeyboardButton(text='📝 Редактировать описание', callback_data='edit_description')],
                [InlineKeyboardButton(text='🖼️ Прикрепить изображение', callback_data='edit_file')]]
    if is_file:
        keyboard.append([InlineKeyboardButton(text='🗑️ Удалить изображение', callback_data='delete_file')])
    if is_edited:
        keyboard.append([InlineKeyboardButton(text='✅ Сохранить данные', callback_data='edit_data')])
        keyboard.append(get_stop_state_button())
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return markup


# Create skipping file keyboard for /add
def get_skip_file_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Пропустить выбор фото ⏩', callback_data='skip_file')]
        ])
    return markup


# Create user's keyboard for /users
def get_users_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[get_admin_menu_button()])
    return markup
