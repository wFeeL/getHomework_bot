import logging
import datetime
from telegram_bot.database_methods.database_connection import create_connection


# Return database data from sql request
def create_request(sql_query: str, is_return: bool = True) -> list:
    conn = create_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql_query)
                if is_return:
                    return cur.fetchall()
    except Exception as e:
        logging.error(f"Error fetching sql request data from database: {e}")
    return []


# Return homework data for special date
def get_homework_by_date(date: datetime.datetime) -> list:
    sql_query = f"SELECT subject_id, description, file_id FROM homework WHERE date = '{date}' ORDER BY id"
    return create_request(sql_query)


# Return subject's data
def get_subjects(subject_id: int | str = None) -> list:
    sql_query = f'SELECT name FROM subject WHERE id = {subject_id}' if subject_id is not None else \
        "SELECT name FROM subject WHERE value = 'true' ORDER BY id"
    return create_request(sql_query)


# Return homework from subject's name
def get_homework_by_subject(subject_name: str) -> list:
    sql_query = "SELECT s.id, s.name, h.date, h.description, h.file_id FROM homework AS h LEFT JOIN subject AS s " \
                "ON h.subject_id = s.id " \
                f"WHERE name = '{subject_name}' " \
                "ORDER BY h.date"
    return create_request(sql_query)


def get_homework_by_id(homework_id: int | str) -> list:
    sql_query = "SELECT s.id, s.name, h.date, h.description, h.file_id FROM homework AS h LEFT JOIN subject AS s " \
                "ON h.subject_id = s.id " \
                f"WHERE h.id = {homework_id} " \
                "ORDER BY h.date"
    return create_request(sql_query)


# Return subject's sticker from subject's name
def get_sticker_by_subject(subject_name: str) -> list:
    sql_query = f"SELECT sticker FROM subject WHERE name = '{subject_name}'"
    return create_request(sql_query)


# Return weekday's data
def get_weekend(weekday_id: int | str = None) -> list:
    sql_query = f"SELECT name FROM weekday WHERE id = '{weekday_id}'" if weekday_id is not None else \
        'SELECT id, name FROM weekday ORDER BY id'
    return create_request(sql_query)


def get_weekday_id(weekday: str) -> list:
    sql_query = f"SELECT id FROM weekday WHERE name = '{weekday}'"
    return create_request(sql_query)


def get_schedule(weekday: str) -> list:
    weekday_id = get_weekday_id(weekday)[0][0]

    sql_query = ('SELECT s.name FROM schedule AS t LEFT JOIN subject AS s ON s.id = t.subject_id '
                 f'WHERE t.weekday_id = {weekday_id} ORDER BY weight ASC')

    return create_request(sql_query)


# Return a list of teachers
def get_teachers() -> list:
    sql_query = 'SELECT teachers.name, subject.name FROM teachers LEFT JOIN subject ON subject_id = subject.id ' \
                'ORDER BY subject.name'
    return create_request(sql_query)


# Return textbook's setting for user (/textbook)
def get_user_data(telegram_id: int | str) -> list:
    sql_query = (f"SELECT s.name, users.subject_path FROM users LEFT JOIN subject as s "
                 f"ON users.subject_id = s.id WHERE telegram_id = '{telegram_id}'")
    return create_request(sql_query)


def get_subject_path(subject: str) -> list:
    subject_id = get_subject_id(subject)[0][0]
    sql_query = f"SELECT path FROM textbook WHERE subject_id = {subject_id}"
    return create_request(sql_query)


def get_textbook_len(subject, subject_path) -> list:
    subject_id = get_subject_id(subject)[0][0]
    sql_query = f"SELECT PAGES FROM TEXTBOOK WHERE SUBJECT_ID = {subject_id} AND PATH = {subject_path}"
    return create_request(sql_query)


def get_search_by_numbers(subject: str, subject_path: int) -> list:
    subject_id = get_subject_id(subject)[0][0]
    sql_query = f"SELECT NUMBERS FROM TEXTBOOK WHERE SUBJECT_ID = {subject_id} AND PATH = {subject_path}"
    return create_request(sql_query)


def get_search_by_paragraph(subject: str, subject_path: int) -> list:
    subject_id = get_subject_id(subject)[0][0]
    sql_query = f"SELECT PARAGRAPHS FROM TEXTBOOK WHERE SUBJECT_ID = {subject_id} AND PATH = {subject_path}"
    return create_request(sql_query)


def get_textbook_subjects() -> list:
    sql_query = ('SELECT name FROM textbook as t LEFT JOIN subject as s ON t.subject_id = s.id WHERE t.value = true '
                 'ORDER BY t.id')
    return create_request(sql_query)


def set_textbook_subject(telegram_id: int | str, subject: str) -> None:
    subject_id = get_subject_id(subject)[0][0]
    sql_query = f"UPDATE users SET subject_id = {subject_id} WHERE telegram_id = '{telegram_id}'"
    create_request(sql_query, is_return=False)


# def get_textbook_data(subject: str, subject_path: int | str) -> list:
#     subject_id = get_subject_id(subject)[0][0]
#     sql_query = f"SELECT page, numbers"
#     return create_request(sql_query)


def get_page_by_paragraph(subject: str, subject_path: int, paragraph: int | str) -> list:
    subject_id = get_subject_id(subject)[0][0]
    sql_query = (f"SELECT PAGE FROM PAGES WHERE (PARAGRAPH like '%:{paragraph}' OR PARAGRAPH = '{paragraph}') "
                 f"AND SUBJECT_ID = {subject_id} AND PATH = {subject_path}")
    return create_request(sql_query)


def get_page_by_number(subject: str, subject_path: int, number: int | str, paragraph: int = None) -> list:
    subject_id = get_subject_id(subject)[0][0]
    if paragraph is None:
        sql_query = (f"SELECT PAGE FROM PAGES WHERE {number} <@ number AND SUBJECT_ID = {subject_id} "
                     f"AND PATH = {subject_path}")
    else:
        sql_query = (f"SELECT PAGE FROM PAGES WHERE {number} <@ number AND PARAGRAPH = '{paragraph}' "
                     f"AND SUBJECT_ID = {subject_id} AND PATH = {subject_path}")
        # and paragraph_request <@ paragraph (in database paragraph have int4range)
    return create_request(sql_query)


# Return a timetable
def get_timetable() -> list:
    sql_query = 'SELECT time FROM timetable'
    return create_request(sql_query)


def get_users(is_admin: bool = False) -> list:
    sql_query = "SELECT telegram_id FROM users WHERE admin = 'true'" if is_admin else 'SELECT telegram_id FROM users'
    return create_request(sql_query)


def get_subject_id(subject_name: str) -> list:
    sql_query = f"SELECT id FROM subject WHERE name = '{subject_name}' "
    return create_request(sql_query)


def get_homework_id_by_subject(subject_name: str) -> list:
    subject_id = get_subject_id(subject_name)[0][0]
    sql_query = f'SELECT id FROM homework WHERE subject_id = {subject_id} ORDER BY date'
    return create_request(sql_query)


def add_value(subject: str, date: str, description: str, file_id: str) -> None:
    subject_id = get_subject_id(subject)[0][0]
    date = datetime.datetime.strptime(date, '%d.%m.%Y')
    sql_query = (f"INSERT INTO homework (subject_id, date, description, file_id) "
                 f"VALUES ({subject_id}, '{date}', '{description}', '{file_id}')")
    create_request(sql_query, is_return=False)


def register_user(telegram_id: int | str, telegram_username: str) -> None:
    sql_query = f"INSERT INTO users (telegram_id, username) VALUES ('{telegram_id}', '{telegram_username}')"
    create_request(sql_query, is_return=False)


def change_admin(telegram_id: int | str, is_admin: bool) -> None:
    if telegram_id not in list(map(lambda x: x[0], get_users())):
        raise ValueError
    sql_query = f"UPDATE users SET admin = {is_admin} WHERE telegram_id = '{telegram_id}'"
    create_request(sql_query, is_return=False)


def edit_homework(homework_id: int | str, date: str | datetime.datetime, description: str, file_id: str) -> None:
    sql_query = (f"UPDATE homework SET date = '{date}', description = '{description}', file_id = '{file_id}' "
                 f"WHERE id = {homework_id}")
    create_request(sql_query, is_return=False)


def delete_homework(homework_id: int | str) -> None:
    sql_query = f"DELETE FROM homework WHERE id = {homework_id}"
    create_request(sql_query, is_return=False)
