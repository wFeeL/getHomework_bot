import logging
import os
from copyreg import dispatch_table

from telegram_bot.database_methods import database_request

def check_environment_variables(logger: logging.Logger):
    for key, value in os.environ.items():
        if value == 'secret_value' or not value:
            logger.error(
                f"You're not specified {key} (environment variable)!\nPlease check Dockerfile and enter a value."
            )

def set_super_admin(logger: logging.Logger):
    telegram_id = os.environ['SUPER_ADMIN_TELEGRAM_ID']
    super_admins = list(map(lambda elem: elem[0], database_request.get_admins(super_admin=True)))
    if telegram_id and telegram_id not in super_admins:
        try:
            database_request.add_admin(telegram_id=telegram_id, value=True, super_admin=True)
            database_request.add_user(telegram_id=telegram_id)
            logger.info(f'Add next telegram_id {telegram_id} to the list of super admins and to the list of users.')
        except ValueError:
            logger.error("Something went wrong while setting super admin.")