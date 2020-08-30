import asyncio

from data.config import admins


async def get_ads(status, db, user_id, av_by, user_filter, bot, message, time_interval):
    """Рассылка новых объявлений"""
    try:
        while status:
            await asyncio.sleep(time_interval)
            status = await db.get_status(user_id)
            if not status:
                break
            ads_ids = []
            last_ads = await db.get_last_ads_id_list(user_id)
            new_ads = av_by.new_ads(user_filter, int(last_ads[0]))
            if new_ads:
                last_ads_links = av_by.get_new_ads_av(user_filter, last_ads)
                last_ads_links.reverse()
                print(last_ads_links)
                for ads in last_ads_links:
                    await bot.send_message(
                        message.from_user.id,
                        text=f'Новое объявление по Вашему фильтру:\n\n'
                             f'{ads["title"]}\n\n'
                             f'Цена: {ads["price"]}$\n'
                             f'Город: {ads["city"]}\n'
                             f'Год: {ads["year"]}\n'
                             f'Коробра передач: {ads["transmission"]}\n'
                             f'Объём двигателя: {ads["engine_capacity"]}\n'
                             f'Тип двигателя: {ads["engines_type"]}\n'
                             f'Тип кузова: {ads["body_type"]}\n'
                             f'Пробег: {ads["mileage"]}\n\n'
                             f'<a href="{ads["link"]}">Смотреть объявление на сайте</a>\n\n',
                        disable_web_page_preview=False
                    )
                    ads_ids.append(ads['id'])

                if len(ads_ids) == 1:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=last_ads[0],
                                         ads_id_3=last_ads[1], ads_id_4=last_ads[2], ads_id_5=last_ads[3])
                elif len(ads_ids) == 2:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=ads_ids[-2],
                                         ads_id_3=last_ads[0], ads_id_4=last_ads[1], ads_id_5=last_ads[2])
                elif len(ads_ids) == 3:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=ads_ids[-2],
                                         ads_id_3=ads_ids[-3], ads_id_4=last_ads[0], ads_id_5=last_ads[1])
                elif len(ads_ids) == 4:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=ads_ids[-2],
                                         ads_id_3=ads_ids[-3], ads_id_4=ads_ids[-4], ads_id_5=last_ads[0])
                elif len(ads_ids) >= 5:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=ads_ids[-2],
                                         ads_id_3=ads_ids[-3], ads_id_4=ads_ids[-4], ads_id_5=ads_ids[-5])
            else:
                print('Пока пусто, продолжаю следить')
            status = await db.get_status(user_id)
        await message.answer(f'Рассылка остановлена. Возможно в течении 20 секунд Вам придет объявление, '
                             f'которое уже находится в обработке')



    except:
        for user in admins:
            await bot.send_message(chat_id=user, text=f'У пользователя {user_id} что-то сломалось с парсером. Проверь')


async def get_ads_call(status, db, user_id, av_by, user_filter, bot, call, time_interval):
    """Рассылка новых объявлений после перезагрузки"""
    try:
        while status:
            await asyncio.sleep(time_interval)
            status = await db.get_status(user_id)
            if not status:
                break
            ads_ids = []
            last_ads = await db.get_last_ads_id_list(user_id)
            new_ads = av_by.new_ads(user_filter, int(last_ads[0]))
            if new_ads:
                last_ads_links = av_by.get_new_ads_av(user_filter, last_ads)
                last_ads_links.reverse()
                print(last_ads_links)
                for ads in last_ads_links:
                    await bot.send_message(
                        call.from_user.id,
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
                    ads_ids.append(ads['id'])

                if len(ads_ids) == 1:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=last_ads[0],
                                         ads_id_3=last_ads[1], ads_id_4=last_ads[2], ads_id_5=last_ads[3])
                elif len(ads_ids) == 2:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=ads_ids[-2],
                                         ads_id_3=last_ads[0], ads_id_4=last_ads[1], ads_id_5=last_ads[2])
                elif len(ads_ids) == 3:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=ads_ids[-2],
                                         ads_id_3=ads_ids[-3], ads_id_4=last_ads[0], ads_id_5=last_ads[1])
                elif len(ads_ids) == 4:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=ads_ids[-2],
                                         ads_id_3=ads_ids[-3], ads_id_4=ads_ids[-4], ads_id_5=last_ads[0])
                elif len(ads_ids) >= 5:
                    await db.set_ads_ids(user_id=user_id, ads_id_1=ads_ids[-1], ads_id_2=ads_ids[-2],
                                         ads_id_3=ads_ids[-3], ads_id_4=ads_ids[-4], ads_id_5=ads_ids[-5])
            else:
                print('Пока пусто, продолжаю следить')
            status = await db.get_status(user_id)

        await call.message.answer(f'Рассылка остановлена. Возможно в течении 20 секунд Вам придет объявление, '
                                  f'которое уже находится в обработке')



    except:
        for user in admins:
            await bot.send_message(chat_id=user, text=f'У пользователя {user_id} что-то сломалось с парсером. Проверь')
