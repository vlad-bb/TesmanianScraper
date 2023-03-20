import os
import json
import asyncio
import aioschedule
from aiogram import Bot, Dispatcher, executor, types
from main import Scrapper

sc = Scrapper()
sc.login()

"""Settings"""
TOKEN = '6140119080:AAEbu6Xs9anI1czP_TGRUDZxWjibJMjXHqY'
bot = Bot(TOKEN)
dp = Dispatcher(bot)

users_storage = 'data/users_storage.json'


def add_user(user_id, fullname_name):
    """Функція додавання користувачів до бота"""
    if not os.path.exists(users_storage):
        with open(users_storage, 'w', encoding='utf-8') as fd:
            json.dump({}, fd, ensure_ascii=False, indent=4)
    with open(users_storage, 'r+', encoding='utf-8') as file:
        users = json.load(file)
        if users.get(user_id) is None:
            print(f'New user {fullname_name} was appended')
            users.update({user_id: fullname_name})
            file.seek(0)
            json.dump(dict(users), file, ensure_ascii=False, indent=4)
            file.truncate()


def get_users() -> list:
    """Функція отримання усіх користувачів"""
    with open(users_storage, 'r', encoding='utf-8') as file:
        users: dict = json.load(file)
        return [k for k in users.keys()]


@dp.message_handler(commands=['start'], )
async def start_command(message: types.Message, ):
    """Функція виклику меню"""
    fullname_name = message.from_user.full_name
    user_id = message.from_user.id
    add_user(user_id, fullname_name)
    info = f'Hello {fullname_name}!\n' \
           f'This is Tesmanian News Chanel'
    await message.answer(info)


async def send_fresh_news():
    """Функція відправки свіжих новин"""
    users = get_users()
    news = sc.check_news()
    if news:
        for article in news:
            for user in users:
                info = f'{list(article.values())[0]}\n' \
                       f'{list(article.keys())[0]}'
                print(f'News was sent to {user}')
                await bot.send_message(user, text=info)


async def scheduler():
    """Планувальник задач"""
    try:
        aioschedule.every(15).seconds.do(send_fresh_news)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(5)
    except Exception as error:
        print(f'Error: {error}')


async def on_startup(_):
    """Запуск планувальника задач при старті бота"""
    asyncio.create_task(scheduler())
    print('TelegramBot running...')


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except Exception as err:
        print(f'Error: {err}')
