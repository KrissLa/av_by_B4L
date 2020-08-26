from data.config import admins
from loader import db, bot
from aiogram.dispatcher import FSMContext

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    print("Создаю таблицу пользователей")
    await db.create_table_av_users()
    print("Готово")
    print("Пытаюсь добавить админов")
    for user in admins:
        await db.add_user(user_id=int(user), name='admin', status=False, filter=None, ads_id_1=None, ads_id_2=None, ads_id_3=None, ads_id_4=None, ads_id_5=None)
    print("Готово")
    print(bot.get_current())

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    # from utils.restart_notifications import restart_notification
    # users_list = await db.select_all_user_id_with_status_1()
    # print(users_list)
    # for user in users_list:
    #     await restart_notification(db=db, bot=bot, user=user)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
