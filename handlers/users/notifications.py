import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default.menu_keyboards import stopped_notification_menu, running_notification_menu, menu, cancel_menu
from keyboards.inline.inline_keyboards import cancel_markup
from loader import dp, db, bot
from states.menu_states import NewFilters, Notifications
from utils.parsers.av_by import get_last_auto_from_av, AvBySearch


@dp.message_handler(Text(endswith='Включить рассылку'), state=Notifications.WaitNotificationStatus)
async def start_notification(message: types.Message, state: FSMContext):
    """Нажатие на кнопку Включить рассылку"""
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    await Notifications.NotificationsOn.set()
    await message.answer('Рассылка включена. Я отправлю Вам новые объявления как только они появятся.',
                         reply_markup=running_notification_menu)
    await db.change_status(user_id, True)
    print(await state.get_state())
    state_name = await state.get_state()
    user_filter = await db.get_filter(user_id)
    av_by = AvBySearch(await db.get_last_ads_id_list(user_id), user_filter)
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
        await message.answer('Что-то сломалось. \n'
                             'Попробуйте меня перезагрузить /restart и проверьте фильтр.\n'
                             'Если не помогло, пожалуйста, сообщите об ошибке')


@dp.message_handler(Text(endswith='Остановить рассылку'), state=Notifications.NotificationsOn)
async def stop_notification(message: types.Message):
    """Нажатие на кнопку Остановить рассылку"""
    await message.answer('Вы нажали Остановить рассылку',
                         reply_markup=stopped_notification_menu)
    await Notifications.WaitNotificationStatus.set()


@dp.message_handler(Text(endswith='Главное меню'),
                    state=Notifications.WaitNotificationStatus)
async def back_to_menu(message: types.Message, state: FSMContext):
    """Нажатие на кнопку Главное меню"""
    await message.answer('Вы нажали Главное меню',
                         reply_markup=menu)
    await state.finish()

# Закинуть user_id  в state и попробовать запустить отдельную функцию по кругу
