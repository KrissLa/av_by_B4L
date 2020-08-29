import asyncio


async def get_ads(state_name, db, user_id, av_by, user_filter, bot, message, time_interval, state):
    """Рассылка новых объявлений"""
    try:
        while state_name=='Notifications:NotificationsOn':
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
            await asyncio.sleep(time_interval)
            state_name = await state.get_state()
        await message.answer('Рассылка остановлена')



    except:
        await message.answer('Что-то сломалось. \n'
                             'Попробуйте меня перезагрузить /restart и проверьте фильтр.\n'
                             'Если не помогло, пожалуйста, сообщите об ошибке')



async def get_ads_call(state_name, db, user_id, av_by, user_filter, bot, call, time_interval, state):
    """Рассылка новых объявлений после перезагрузки"""
    try:
        while state_name == 'Notifications:NotificationsOn':
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
            await asyncio.sleep(time_interval)
            state_name = await state.get_state()
        await call.message.answer('Рассылка остановлена')



    except:
        await call.message.answer('Что-то сломалось. \n'
                             'Попробуйте меня перезагрузить /restart и проверьте фильтр.\n'
                             'Если не помогло, пожалуйста, сообщите об ошибке')