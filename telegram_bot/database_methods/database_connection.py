import psycopg2
import logging
from telegram_bot import config_reader

logging.basicConfig(level=logging.INFO)


# Create connection to database by pg_dsn
def create_connection():
    try:
        connection = psycopg2.connect(str(config_reader.config.pg_dsn))
        return connection

    except psycopg2.Error as error:
        logging.error(f'Error with connection to database {error}')
        return None


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