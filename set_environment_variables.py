import argparse
import os

parser = argparse.ArgumentParser()

default_arg_value = 'secret_value'

parser.add_argument('--bot_token', default=default_arg_value)
parser.add_argument('--weather_api', default=default_arg_value)
parser.add_argument('--super_admin_telegram_id', default=default_arg_value)

args = parser.parse_args()

for key, value in args.__dict__.items():
    if value != default_arg_value:
        os.environ[key.upper()] = value
