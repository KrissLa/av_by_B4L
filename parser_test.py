import asyncio

import requests
import multiprocessing

from loader import db
from utils.parsers.av_by import AvBySearch

#user_data = {'user_id': 111111, 'filter': "", 'ads_id_1': 1, 'last_ads_list': [1, 2, 3, 4, 5]}


def handler(user_data):
    av = AvBySearch(user_data['last_ads_list'], user_data['filter'])
    if av.new_ads(user_data['filter'], user_data['ads_id_1']):
        result = av.get_new_ads_av(user_data['filter'], user_data['last_ads_list'])
        print(result)


async def get_data():
    user_ids = await db.select_all_user_id_with_status_1()
    user_datas = []
    for user in user_ids:
        ids = await db.get_last_ads_id_list(user)
        user_filter = await db.get_filter(user)
        user_list = [int(ids[0]), int(ids[1]), int(ids[2]), int(ids[3]), int(ids[4])]
        print(user_list)
        user_data = {
            'user_id': user,
            'filter': user_filter,
            'ads_id_1': ids[0],
            'last_ads_list':  user_list
        }
        user_datas.append(user_data)
    return user_datas

async def get_results():
    data = await get_data()
    with multiprocessing.Pool(multiprocessing.cpu_count()) as process:
        process.map(handler, data)

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(get_results())




