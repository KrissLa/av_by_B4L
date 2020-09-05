import asyncio
import multiprocessing

import aiogram
from aiogram import executor
from aiogram.utils.exceptions import BotBlocked

import filters
import middlewares
from data.config import admins
from handlers import dp
from loader import db, bot
from utils.notify_admins import on_startup_notify
from utils.parsers.av_by import AvBySearch
from utils.set_bot_commands import set_default_commands


async def get_data():
    user_ids = await db.select_all_user_id_with_status_1()
    user_datas = []
    for user in user_ids:
        ids = await db.get_last_ads_id_list(user)
        user_filter = await db.get_filter(user)
        user_list = [int(ids[0]), int(ids[1]), int(ids[2]), int(ids[3]), int(ids[4])]
        # print(user_list)
        user_data = {
            'user_id': user,
            'filter': user_filter,
            'ads_id_1': ids[0],
            'last_ads_list': user_list
        }
        # print(user_data)
        user_datas.append(user_data)
    return user_datas


def handler(user_data):
    av = AvBySearch(user_data['last_ads_list'], user_data['filter'])
    print('создал класс парсерв')
    if av.new_ads(user_data['filter'], user_data['ads_id_1']):
        new_ads_list = av.get_new_ads_av(user_data['filter'], user_data['last_ads_list'])
        # print(result)
        # for res in result:
        #     print(res)
        #     await bot.send_message(chat_id=user_data['user_id'], text=f'{res["title"]}')
    else:
        new_ads_list = []

        # print('Пока пусто')
    result = {
        'user_id': user_data['user_id'],
        'new_ads_list': new_ads_list,
        'last_ads': user_data['last_ads_list']
    }
    # print(result)
    # print(result)

    return result


async def get_results():
    while True:
        # await asyncio.sleep(10)
        try:
            data = await get_data()
            # print(data)
            # print(data)
            with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
                parser_result = process.map(handler, data)
                print(parser_result)
                print('multi сделаль')
                for user in parser_result:
                    print('вошел в цикл')
                    if user['new_ads_list']:
                        print(user['user_id'])
                        user['new_ads_list'].reverse()
                        print('перевернул списсок')
                        for ads in user['new_ads_list']:
                            print('Вошел в цикл отправки сообщений')
                            try:
                                await bot.send_message(
                                    user['user_id'],
                                    text=f'Новое объявление по Вашему фильтру:\n\n'
                                         f'{ads["title"]}\n\n'
                                         f'Цена:  {ads["price"]}$\n'
                                         f'Город:  {ads["city"]}\n'
                                         f'Год:  {ads["year"]}\n'
                                         f'Коробра передач:  {ads["transmission"]}\n'
                                         f'Объём двигателя:  {ads["engine_capacity"]}\n'
                                         f'Тип двигателя:  {ads["engines_type"]}\n'
                                         f'Тип кузова:  {ads["body_type"]}\n'
                                         f'Пробег:  {ads["mileage"]}\n\n'
                                         f'<a href="{ads["link"]}">Смотреть объявление на сайте</a>\n\n',
                                    disable_web_page_preview=False
                                )
                            except BotBlocked:
                                await db.change_status(user_id=user['user_id'], status_value=False)
                                print(f'Не удалось отправить сообщение пользователю {user["user_id"]}')
                            print(f'Отправил сообщение пользователю {user["user_id"]}')
                        print('Пытаюсь добавить id в бд')

                        if len(user['new_ads_list']) == 1:
                            await db.set_ads_ids(user_id=user['user_id'],
                                                 ads_id_1=user['new_ads_list'][-1]['id'],
                                                 ads_id_2=user['last_ads'][0],
                                                 ads_id_3=user['last_ads'][1],
                                                 ads_id_4=user['last_ads'][2],
                                                 ads_id_5=user['last_ads'][3])
                        elif len(user['new_ads_list']) == 2:
                            await db.set_ads_ids(user_id=user['user_id'],
                                                 ads_id_1=user['new_ads_list'][-1]['id'],
                                                 ads_id_2=user['new_ads_list'][-2]['id'],
                                                 ads_id_3=user['last_ads'][0],
                                                 ads_id_4=user['last_ads'][1],
                                                 ads_id_5=user['last_ads'][2])
                        elif len(user['new_ads_list']) == 3:
                            await db.set_ads_ids(user_id=user['user_id'],
                                                 ads_id_1=user['new_ads_list'][-1]['id'],
                                                 ads_id_2=user['new_ads_list'][-2]['id'],
                                                 ads_id_3=user['new_ads_list'][-3]['id'],
                                                 ads_id_4=user['last_ads'][0],
                                                 ads_id_5=user['last_ads'][1])
                        elif len(user['new_ads_list']) == 4:
                            await db.set_ads_ids(user_id=user['user_id'],
                                                 ads_id_1=user['new_ads_list'][-1]['id'],
                                                 ads_id_2=user['new_ads_list'][-2]['id'],
                                                 ads_id_3=user['new_ads_list'][-3]['id'],
                                                 ads_id_4=user['new_ads_list'][-4]['id'],
                                                 ads_id_5=user['last_ads'][0])
                        elif len(user['new_ads_list']) >= 5:
                            await db.set_ads_ids(user_id=user['user_id'],
                                                 ads_id_1=user['new_ads_list'][-1]['id'],
                                                 ads_id_2=user['new_ads_list'][-2]['id'],
                                                 ads_id_3=user['new_ads_list'][-3]['id'],
                                                 ads_id_4=user['new_ads_list'][-4]['id'],
                                                 ads_id_5=user['new_ads_list'][-5]['id'])
                        print('закончил')
                        # print(user['user_id'])
                        # print(user['new_ads_list'])
                    else:
                        print('Новых объявлений нет')
        except:
            print('Error')

            # print(res_mult)
            # print(len(res_mult))
            # print(process.)


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
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_results())
    dp.loop.create_task(get_results())
    executor.start_polling(dp, on_startup=on_startup)
