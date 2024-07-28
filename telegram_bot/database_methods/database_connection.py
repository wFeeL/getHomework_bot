import psycopg2
import logging
from telegram_bot.config_reader import config

logging.basicConfig(level=logging.INFO)


# Create connection to database by pg_dsn
def create_connection():
    try:
        connection = psycopg2.connect(str(config.pg_dsn))
        return connection

    except psycopg2.Error as error:
        logging.error(f'Error with connection to database {error}')
        return None
