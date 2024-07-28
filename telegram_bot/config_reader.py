from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PostgresDsn


# Settings for telegram bot, database (postgres) and weather
class Settings(BaseSettings):
    bot_token: SecretStr = "6235035727:AAEeeliZcjeNobBAuEjAmXGexNjxkMJVMCo"
    pg_dsn: PostgresDsn = "postgres://postgres:password@postgres:5432"
    weather_API: SecretStr = "fc99a79328de8b7fa62cec28ebbb5a00"
    model_config = SettingsConfigDict(env_prefix='_')
