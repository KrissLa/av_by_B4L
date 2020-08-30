from aiogram import executor

import filters
import middlewares
from data.config import admins
from handlers import dp
from loader import db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    filters.setup(dp)
    middlewares.setup(dp)
    print("Создаю таблицу пользователей")
    await db.create_table_av_users()
    print("Готово")
    print("Пытаюсь добавить админов")
    for user in admins:
        await db.add_user(user_id=int(user), name='admin', status=False, filter=None, ads_id_1=None, ads_id_2=None,
                          ads_id_3=None, ads_id_4=None, ads_id_5=None)


    print("Готово")

    await db.create_table_bug_reports()
    await set_default_commands(dp)
    await on_startup_notify(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
