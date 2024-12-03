import logging
import os

from telegram_bot.database_methods import database_request

def check_environment_variables(logger: logging.Logger):
    for key, value in os.environ.items():
        if value == 'secret_value' or not value:
            logger.error(
                f"You're not specified {key} (environment variable)!\nPlease check Dockerfile and enter a value."
            )

def set_super_admin(logger: logging.Logger):
    telegram_id = os.environ['SUPER_ADMIN_TELEGRAM_ID']
    if telegram_id:
        try:
            logger.info(f'Add next telegram_id {telegram_id} to the list of super admins')
            database_request.add_admin(telegram_id=os.environ['SUPER_ADMIN_TELEGRAM_ID'], value=True, super_admin=True)
        except ValueError:
            logger.error("Something went wrong while setting super admin.")