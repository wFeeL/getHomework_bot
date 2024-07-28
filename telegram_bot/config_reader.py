from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PostgresDsn


# Settings for telegram bot, database (postgres and weather
class Settings(BaseSettings):
    bot_token: SecretStr
    pg_dsn: PostgresDsn
    weather_API: SecretStr
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


config = Settings(
    bot_token="6235035727:AAEeeliZcjeNobBAuEjAmXGexNjxkMJVMCo",  # Telegram bot API TOKEN
    pg_dsn="postgres://postgres:password@postgres:5432",
    weather_API="fc99a79328de8b7fa62cec28ebbb5a00"
)
