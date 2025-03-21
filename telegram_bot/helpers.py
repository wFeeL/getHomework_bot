import logging
import os
import datetime

from telegram_bot.database_methods import database_request

def check_environment_variables(logger: logging.Logger):
    for key, value in os.environ.items():
        if value == 'secret_value' or not value:
            logger.error(
                f"You're not specified {key} (environment variable)!\nPlease check Dockerfile and enter a value."
            )

def set_super_admin(logger: logging.Logger):
    try:
        telegram_id = os.environ['SUPER_ADMIN_TELEGRAM_ID']
        super_admins = list(map(lambda elem: elem[0], database_request.get_admins(super_admin=True)))
        if telegram_id and telegram_id not in super_admins:
            database_request.add_admin(telegram_id=telegram_id, value=True, super_admin=True)
            database_request.add_user(telegram_id=telegram_id)
            logger.info(f'Add next telegram_id {telegram_id} to the list of super admins and to the list of users.')
    except TypeError:
        logger.error("There are no super admins in database or database don't activated.")
    except ValueError:
        logger.error("Something went wrong while setting super admin.")

def set_timetable(logger: logging.Logger):
    TIMETABLE_DICT = {
        1: {
            'start': datetime.time(hour=8, minute=30),
            'end': datetime.time(hour=9, minute=10)
        },
        2: {
            'start': datetime.time(hour=9, minute=20),
            'end': datetime.time(hour=10)
        },
        3: {
            'start': datetime.time(hour=10, minute=20),
            'end': datetime.time(hour=11)
        },
        4: {
            'start': datetime.time(hour=11, minute=20),
            'end': datetime.time(hour=12)
        },
        5: {
            'start': datetime.time(hour=12, minute=20),
            'end': datetime.time(hour=13)
        },
        6: {
            'start': datetime.time(hour=13, minute=20),
            'end': datetime.time(hour=14)
        },
        7: {
            'start': datetime.time(hour=14, minute=10),
            'end': datetime.time(hour=14, minute=50)
        },
        8: {
            'start': datetime.time(hour=15),
            'end': datetime.time(hour=15, minute=40)
        }
    }
