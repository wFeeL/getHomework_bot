import datetime
import os

class Settings:
    def __init__(self, bot_token, pg_dsn, weather_api, min_date, max_date):
        self.bot_token: str = bot_token
        self.pg_dsn: str = pg_dsn
        self.weather_API: str = weather_api
        self.min_date: datetime.datetime = min_date
        self.max_date: datetime.datetime = max_date

# Settings for telegram bot, database (postgres) and weather
config = Settings(
    bot_token=os.environ['BOT_TOKEN'],
    pg_dsn="postgres://postgres:password@localhost:5432",
    weather_api=os.environ['WEATHER_API'],
    min_date=datetime.datetime(year=2024, month=9, day=1),
    max_date=datetime.datetime(year=2025, month=5, day=31)
)
