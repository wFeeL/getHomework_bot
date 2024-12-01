FROM python:3.11.2-slim
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
ENV BOT_TOKEN secret_value
ENV WEATHER_API secret_value
ENV SUPER_ADMIN_TELEGRAM_ID secret_value
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./telegram_bot /app/telegram_bot
COPY set_environment_variables.py .

WORKDIR /app

CMD ["python", "-m", "telegram_bot.bot"]