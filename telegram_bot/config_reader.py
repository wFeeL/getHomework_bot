from pydantic_settings import BaseSettings
from pydantic import SecretStr, PostgresDsn

# Database connection config
DB_CONFIG = {
    'host': 'postgres',
    'user': 'postgres',
    'password': 'password',
    'port': 5432
}


class Settings(BaseSettings):
    bot_token: SecretStr
    pg_dsn: PostgresDsn
    weather_API: SecretStr


# Settings for telegram bot, postgres and weather
config = Settings(
    bot_token="",  # Telegram bot API TOKEN
    pg_dsn=f"postgres://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}",
    weather_API='fc99a79328de8b7fa62cec28ebbb5a00'
)
