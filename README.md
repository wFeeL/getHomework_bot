
# getHomework_bot

getHomework_bot - это телеграмм бот, написанный на библиотеке [aiogram](https://aiogram.dev/) с использованием [Postgresql](https://www.postgresql.org/) базы данных. 

Бот может сохранять, изменять, удалять и записывать данные о домашнем задании в базу.
Для работы бота необходимо создать таблицы в базе данных, используя [homework.sql](https://github.com/wFeeL/getHomework_bot/blob/main/database/homework.sql), в котором уже прописаны все таблицы.

В боте преобладает несколько видов пользователей:
1. Супер-администратор - создатель данного бота, у него есть доступ к всему функционалу.
2. Администратор - может добавлять, удалять и изменять домашние задания, а также просматривать всех пользователей бота.
3. Ученик (пользователь, выбравший класс) - может просматривать домашние задания для своего класса.
4. Обычный пользователь - доступен маленький функционал, для повышения необходимо выбрать любой класс.



## Run Locally

Создать бота с помощью @BotFather и получить токен

Clone the project and run it locally

```bash
git clone https://github.com/wFeeL/getHomework_bot.git
cd getHomework_bot
pip install -r requirements.txt
python -m telegram_bot.bot
```



## Run via Docker (recommended)

Clone the project, build an image and run the project in [Docker](https://www.docker.com/)
```bash
git clone https://github.com/wFeeL/getHomework_bot.git
cd getHomework_bot
touch .env
docker build -f Dockefile -t homework_bot .
docker volume create --name=db_data
docker-compose up
```

    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`BOT_TOKEN`

`WEATHER_API`

`SUPER_ADMIN_TELEGRAM_ID`
