import pymorphy3

from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

from telegram_bot.handlers import bot_commands
from telegram_bot import text_message
from telegram_bot.config_reader import config
from telegram_bot.database_methods.database_request import *
from telegram_bot.keyboards import inline_markup

from PyPDF2 import PdfReader, PdfWriter

# Dict for callbacks. 'function_name': 'callback_name'

CALLBACK = {
    'send_menu': 'menu',
    'send_help': 'help',
    'send_all_homework': 'all_homework',
    'send_tomorrow_homework': 'tomorrow_homework',
    'send_calendar_homework': 'calendar_homework',
    'send_schedule': 'schedule_menu',
    'send_admin_menu': 'admin_menu',
    'send_adding_states': 'add_homework',
    'send_textbook': 'textbook'
}

bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))


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
    homework_data = get_homework_by_date(date)
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
            subject_name = get_subjects(subject_id=homework_data[i][0])[0][0]
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


async def create_pdf_by_page(page_number: int, subject: str, subject_path: int, filename: str):
    try:
        with open(f'././textbook/{subject} {subject_path}.pdf', 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            pdf_writer = PdfWriter()
            with open(f'././textbook/{filename}.pdf', 'wb') as result:
                pdf_writer.add_page(pdf_reader.pages[page_number - 1])
                pdf_writer.write(result)
        return not None
    except IndexError:
        return None


async def get_textbook_page(subject: str, subject_path: int | str, request: str, path: str):
    try:
        page = int(request)
        if page > get_textbook_len(subject, subject_path)[0][0]:
            raise IndexError

        await create_pdf_by_page(page, subject, subject_path, filename='page')
        file = FSInputFile(path.format(name='page'), filename=f'страница {page}.pdf')

        return file

    except IndexError:
        print('too looong!')

    except ValueError:
        print('Handle a ValueError')


async def get_textbook_number(subject: str, subject_path: int | str, request: str, path: str):
    try:
        if not get_search_by_numbers(subject, subject_path)[0][0]:
            raise IndexError

        paragraph = None

        if subject == 'Алгебра':
            request = request.split('.')
            paragraph, number = int(request[0]), int(request[1])

        else:
            number = int(request)

        page = get_page_by_number(subject=subject, subject_path=subject_path,
                                  number=number, paragraph=paragraph)[0][0]
        await create_pdf_by_page(page, subject, subject_path, filename='number')
        file = FSInputFile(path.format(name='number'), filename=f'номер {number}.pdf')

        return file

    except IndexError:
        print('no numbers')

    except ValueError:
        print('it is algebra, but wrong number')


async def get_textbook_paragraph(subject: str, subject_path: int | str, request: str, path: str):
    try:
        if not get_search_by_paragraph(subject, subject_path)[0][0]:
            raise IndexError

        paragraph = int(request)

        page = get_page_by_paragraph(subject=subject, subject_path=subject_path, paragraph=paragraph)[0][0]
        await create_pdf_by_page(page, subject, subject_path, filename='paragraph')

        file = FSInputFile(path.format(name='paragraph'), filename=f'параграф {paragraph}.pdf')
        return file

    except IndexError:
        print('no paragraphs')

    except ValueError:
        print('Handle a ValueError')
