import asyncio

from aiogram import types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
storage = RedisStorage2()


from utils.parsers.av_by import AvBySearch


async def restart_notification(db, bot, user, storage=storage):
    """"""

    print(await storage.get_state(chat=user))
    state_name = await storage.get_state(chat=user)
    data = await storage.get_data(chat=user)
    print(data)
    user_id = data.get('user_id')
    print(user_id)
    print(await storage.get_state(chat=user))
    if state_name == 'Notifications:NotificationsOn':
        user_filter = await db.get_filter(user_id)
        av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
        try:
            while state_name == 'Notifications:NotificationsOn':
                print(user_id)
                ads_ids = []
                last_ads = await db.get_last_ads_id_list(user_id)
                new_ads = av_by.new_ads(user_filter, int(last_ads[0]))
                if new_ads:
                    last_ads_links = av_by.get_new_ads_av(user_filter, last_ads)
                    last_ads_links.reverse()
                    print(last_ads_links)
                    for ads in last_ads_links:
                        await bot.send_message(
                            user_id,
                            text=f'=====AV.BY:\n \n {ads["title"]}\n  {ads["price"]}$\n {ads["link"]}',
                        )
                        ads_ids.append(ads['id'])

                    if len(ads_ids) == 1:
                        await db.change_ads_id_5(user_id, last_ads[3])
                        await db.change_ads_id_4(user_id, last_ads[2])
                        await db.change_ads_id_3(user_id, last_ads[1])
                        await db.change_ads_id_2(user_id, last_ads[0])
                        await db.change_ads_id_1(user_id, ads_ids[-1])
                    elif len(ads_ids) == 2:
                        await db.change_ads_id_5(user_id, last_ads[2])
                        await db.change_ads_id_4(user_id, last_ads[1])
                        await db.change_ads_id_3(user_id, last_ads[0])
                        await db.change_ads_id_2(user_id, ads_ids[-2])
                        await db.change_ads_id_1(user_id, ads_ids[-1])
                    elif len(ads_ids) == 3:
                        await db.change_ads_id_5(user_id, last_ads[1])
                        await db.change_ads_id_4(user_id, last_ads[0])
                        await db.change_ads_id_3(user_id, ads_ids[-3])
                        await db.change_ads_id_2(user_id, ads_ids[-2])
                        await db.change_ads_id_1(user_id, ads_ids[-1])
                    elif len(ads_ids) == 4:
                        await db.change_ads_id_5(user_id, last_ads[0])
                        await db.change_ads_id_4(user_id, ads_ids[-4])
                        await db.change_ads_id_3(user_id, ads_ids[-3])
                        await db.change_ads_id_2(user_id, ads_ids[-2])
                        await db.change_ads_id_1(user_id, ads_ids[-1])
                    elif len(ads_ids) >= 5:
                        await db.change_ads_id_5(user_id, ads_ids[-5])
                        await db.change_ads_id_4(user_id, ads_ids[-4])
                        await db.change_ads_id_3(user_id, ads_ids[-3])
                        await db.change_ads_id_2(user_id, ads_ids[-2])
                        await db.change_ads_id_1(user_id, ads_ids[-1])
                else:
                    print('Пока пусто, продолжаю следить')
                await asyncio.sleep(15)


        except:
            await bot.send_message(chat_id=user_id, text='Что-то сломалось. \n'
                                 'Попробуйте меня перезагрузить /restart и проверьте фильтр.\n'
                                 'Если не помогло, пожалуйста, сообщите об ошибке')