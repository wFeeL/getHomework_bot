import logging
import datetime
from telegram_bot.database_methods.database_connection import create_connection


# Return database data from sql request
def create_request(sql_query: str, is_return: bool = True) -> list | None:
    """
    Return list of sql query's result. Create connection by config settings and execute sql query.
    :param sql_query: the sql query to execute with cursor.
    :param is_return: the bool type for returning value from request.
    :return: List of sql query result.
    """
    conn = create_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql_query)
                if is_return:
                    return cur.fetchall()
    except Exception as e:
        logging.error(f"Error fetching sql request data from database: {e}")
    return None


# Return condition for sql queries
def create_condition(args: dict, exception=None) -> str | None:
    """
    Create condition for sql query. Take column's args from table. 
    Use them to create 'WHERE' and 'AND' form for creating sql query.
    :param args: column's args from table.
    :param exception: list of exceptions which create request with '<@' element (not '=' element).
    :return: Stroke with condition
    """
    if exception is None:
        exception = []
    if not list(args.values()) == [None] * len(args):
        args_list = list(filter(lambda elem: args[elem] is not None, args))
        condition = 'WHERE ' + ' AND '.join(list(map(
            lambda elem: f"{elem} = '{args[elem]}'" if elem not in exception else "'{%s}' <@ %s" % (args[elem], elem),
            args_list))
        )
        return condition
    return ''


# Return data from users table
def get_users(telegram_id: int | str = None, class_id: int | str = None) -> list:
    """
    Return user's data from user's table from database. Take args for finding user in table.
    :param telegram_id: the user's telegram_id
    :param class_id: the user's class_id
    :return: List of row from database
    """
    condition = create_condition(locals())
    sql_query = f"SELECT telegram_id, class_id FROM users {condition} ORDER BY id"
    return create_request(sql_query)


# Return data from admins table
def get_admins(telegram_id: int | str = None, value: bool | str = None, super_admin: bool | str = None,
               class_id: int | str = None) -> list:
    """
    Return admin's data from admin's table from database. Take args for finding admin in table.
    :param telegram_id: the admin's telegram_id
    :param value: the bool type value of admin activity
    :param super_admin: the bool type value of super admin
    :param class_id: the admin's class_id
    :return: List of row from database
    """
    condition = create_condition(locals())
    sql_query = f"SELECT telegram_id, class_id, value, super_admin, class_id FROM admins {condition} ORDER BY id"
    return create_request(sql_query)


# Return data from homework table
def get_homework(id: int | str = None, subject_id: int | str = None, date: datetime.datetime | str = None,
                 class_id: int | str = None) -> list:
    """
    Return homework's data from homework's table from database. Take args for finding homework in table.
    :param id: the homework's id
    :param subject_id: the subject's id from homework
    :param date: the date of homework
    :param class_id: the class_id of homework
    :return: List of row from database
    """
    condition = create_condition(locals())
    sql_query = f"SELECT id, subject_id, date, description, file_id FROM homework {condition} ORDER by date"
    return create_request(sql_query)


# Return data from subject table
def get_subject(id: int | str = None, name: str = None, sticker: str = None,
                value: bool = None, class_ids: int | str = None) -> list:
    """
    Return subject's data from subject's table from database. Take args for finding subject in table.
    :param id: the id of subject
    :param name: the name of subject
    :param sticker: the sticker of subject 
    :param value: the bool type value of activity of subject
    :param class_ids: the list of class ids of subject
    :return: List of row from database
    """
    condition = create_condition(args=locals(), exception=['class_ids'])
    sql_query = f"SELECT id, name, sticker, value, class_ids FROM subject {condition} ORDER BY id"
    return create_request(sql_query)


# Return data from weekday table
def get_weekday(id: int | str = None, name: str = None, class_ids: int | str = None) -> list:
    """
    Return weekday's data from weekday's table from database. Take args for finding weekday in table.
    :param id: the id of weekday
    :param name: the name of weekday
    :param class_ids: the list of class ids of weekday
    :return: List of row from database
    """
    condition = create_condition(args=locals(), exception=['class_ids'])
    sql_query = f"SELECT id, name, class_ids FROM weekday {condition} ORDER BY id"
    return create_request(sql_query)


# Return data from class table
def get_class(id: int | str = None, letter: str = None, number: int | str = None, value: bool | str = None):
    """
    Return class's data from class's table from database. Take args for finding class in table.
    :param id: the id of class
    :param letter: the letter of class
    :param number: the number of class
    :param value: the bool type value of class activity
    :return: List of row from database
    """
    condition = create_condition(locals())
    sql_query = f"SELECT id, letter, number, value FROM class {condition} ORDER BY id"
    return create_request(sql_query)


# Return data from schedule table
def get_schedule(weekday: str, class_id: int | str) -> list:
    """
    Return schedule's data from schedule's table from database. Take args for finding schedule in table.
    :param weekday: the weekday of schedule
    :param class_id: the class id of schedule
    :return: List of row from database
    """
    weekday_id = get_weekday(name=weekday)[0][0]

    sql_query = ('SELECT s.name FROM schedule AS t LEFT JOIN subject AS s ON s.id = t.subject_id '
                 f'WHERE t.weekday_id = {weekday_id} AND class_id = {class_id} ORDER BY weight ASC')

    return create_request(sql_query)


# Return data from teachers table
def get_teachers(class_id: int | str) -> list:
    """
    Return teachers data from teachers table from database. Take args for finding teachers in table.
    :param class_id: the class id of teachers
    :return: List of row from database
    """
    sql_query = ("SELECT teachers.name, subject.name FROM teachers LEFT JOIN subject ON subject_id = subject.id "
                 "WHERE '{%s}' <@ teachers.class_ids ORDER BY subject.name" % class_id)
    return create_request(sql_query)


# Return data from timetable table
def get_timetable() -> list:
    """
    Return timetable's data from timetable's table from database. Take args for finding timetable in table.
    :return: List of row from database
    """
    sql_query = 'SELECT time FROM timetable'
    return create_request(sql_query)


# Return data from quotes table
def get_quotes(text: str = None, author: str = None, value: bool = None) -> list:
    """
    Return quotes data from quotes table from database. Take args for finding quotes in table.
    :param text: the text of quote
    :param author: the author of quote
    :param value: the bool type value activity of quote
    :return: List of row from database
    """
    condition = create_condition(locals())
    sql_query = f"SELECT text, author, value FROM quotes {condition} ORDER BY id"
    return create_request(sql_query)


# Add homework's value to database
def add_value(subject: str, date: str, description: str, file_id: str, class_id: int | str) -> None:
    """
    Insert value into homework's table.
    :param subject: the subject of homework
    :param date: the date of homework
    :param description: the description of homework
    :param file_id: the file id of homework
    :param class_id: the class id of homework
    """
    subject_id = get_subject(name=subject)[0][0]
    date = datetime.datetime.strptime(date, '%d.%m.%Y')
    sql_query = (f"INSERT INTO homework (subject_id, date, description, file_id, class_id) "
                 f"VALUES ({subject_id}, '{date}', '{description}', '{file_id}', {class_id})")
    create_request(sql_query, is_return=False)


# Add user's value to database
def add_user(telegram_id: int | str, class_id: int = 0) -> None:
    """
    Insert value into user's table.
    :param telegram_id: the telegram id of user
    :param class_id: the class id of user
    """
    sql_query = f"INSERT INTO users (telegram_id, class_id) VALUES ('{telegram_id}', {class_id})"
    create_request(sql_query, is_return=False)


# Add admin's value to database
def change_admin(telegram_id: int | str, value: bool = True, class_id: int | str = 0) -> None:
    """
    Insert and update value of admin's table. If admin is already in database use 'UPDATE' method.
    :param telegram_id: the telegram id of admin
    :param value: the bool type value of admin activity
    :param class_id: the class id of admin
    """
    if telegram_id not in list(map(lambda x: x[0], get_admins())) and value:
        sql_query = f"INSERT INTO admins (telegram_id, value, class_id) VALUES ('{telegram_id}', true, {class_id})"
    else:
        sql_query = f"UPDATE admins SET value = {value}, class_id = {class_id} WHERE telegram_id = '{telegram_id}'"
    create_request(sql_query, is_return=False)


# Update user's class to database
def update_user_class(telegram_id: int | str, class_id: int) -> None:
    """
    Update user's class.
    :param telegram_id: the telegram id of user
    :param class_id: the class id of user
    """
    sql_query = f"UPDATE users SET class_id = {class_id} WHERE telegram_id = '{telegram_id}'"
    create_request(sql_query, is_return=False)


# Update homework's value to database
def update_homework(homework_id: int | str, date: str, description: str, file_id: str) -> None:
    """
    Update date, description and file of homework.
    :param homework_id: the id of homework
    :param date: the date of homework
    :param description: the description of homework
    :param file_id: the file id of homework
    """
    date = datetime.datetime.strptime(date, '%d.%m.%Y')
    sql_query = (f"UPDATE homework SET date = '{date}', description = '{description}', file_id = '{file_id}' "
                 f"WHERE id = {homework_id}")
    create_request(sql_query, is_return=False)


# Delete homework's value from database
def delete_homework(homework_id: int | str) -> None:
    """
    Delete homework's data from table
    :param homework_id: the id of homework
    """
    sql_query = f"DELETE FROM homework WHERE id = {homework_id}"
    create_request(sql_query, is_return=False)
