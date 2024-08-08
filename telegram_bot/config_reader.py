# Settings for telegram bot, database (postgres)cr and weather
class Settings:
    def __init__(self, bot_token, pg_dsn, weather_api):
        self.bot_token = bot_token
        self.pg_dsn = pg_dsn
        self.weather_API = weather_api


config = Settings(
    bot_token="6235035727:AAEeeliZcjeNobBAuEjAmXGexNjxkMJVMCo",
    pg_dsn="postgres://postgres:password@localhost:5432",
    weather_api="fc99a79328de8b7fa62cec28ebbb5a00"
)
