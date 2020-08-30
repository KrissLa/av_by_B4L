import asyncio
import asyncpg
from datetime import datetime

from data import config

now = datetime.now()


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.PGUSER,
                database=config.PGDATABASE,
                password=config.PGPASSWORD,
                host=config.ip,
                port=config.PORT
            )
        )

    async def create_table_av_users(self):
        """Создаем таблицу пользователей"""
        sql = """
        CREATE TABLE IF NOT EXISTS av_users (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL UNIQUE ,
        name VARCHAR(255),
        status BOOL,
        filter TEXT,
        ads_id_1 bigint,
        ads_id_2 bigint,
        ads_id_3 bigint,
        ads_id_4 bigint,
        ads_id_5 bigint);
        """
        await self.pool.execute(sql)

    async def add_user(self, user_id: int, name: str, status: bool, filter: str, ads_id_1: int, ads_id_2: int,
                       ads_id_3: int, ads_id_4: int, ads_id_5: int):
        """Добавляем пользователя в бд"""
        try:
            sql = "INSERT INTO av_users (user_id, name, status, filter, ads_id_1, ads_id_2, ads_id_3, ads_id_4, ads_id_5) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)"
            await self.pool.execute(sql, user_id, name, status, filter, ads_id_1, ads_id_2, ads_id_3, ads_id_4,
                                    ads_id_5)
        except asyncpg.exceptions.UniqueViolationError:
            print('Пользователь с таким user_id уже существует')

    async def count_users(self):
        """Достаем количество пользователей"""
        return await self.pool.fetchval('SELECT COUNT(*) FROM av_users')

    async def count_users_with_status_1(self):
        """Достаем количество пользователей"""
        return await self.pool.fetchval('SELECT COUNT(*) FROM av_users WHERE status = true')

    async def change_filter(self, user_id, filter_value):
        """Устанавливаем фильтр"""
        await self.pool.execute(f"UPDATE av_users SET filter = '{filter_value}' WHERE user_id = {user_id}")

    async def get_filter(self, user_id):
        """Получаем фильтр"""
        return await self.pool.fetchval(f'SELECT filter FROM av_users WHERE user_id = {user_id}')

    async def change_status(self, user_id, status_value):
        """Устанавливаем status"""
        await self.pool.execute(f"UPDATE av_users SET status = {status_value} WHERE user_id = {user_id}")

    async def get_status(self, user_id):
        """Получаем статут рассылки"""
        return await self.pool.fetchval(f'SELECT status FROM av_users WHERE user_id = {user_id}')

    async def select_all_user_id(self):
        """Выбираем все id Пользователей"""
        all_users = await self.pool.fetch('SELECT user_id FROM av_users')
        all_users_id = [id['user_id'] for id in all_users]
        print(all_users_id)
        return all_users_id

    async def select_all_user_id_with_status_1(self):
        """Выбираем все id Пользователей"""
        all_users = await self.pool.fetch('SELECT user_id FROM av_users WHERE status = true')
        all_users_id = [id['user_id'] for id in all_users]
        return all_users_id

    async def select_all_user_id_with_status_0(self):
        """Выбираем все id Пользователей"""
        all_users = await self.pool.fetch('SELECT user_id FROM av_users WHERE status = false')
        all_users_id = [id['user_id'] for id in all_users]
        return all_users_id

    # async def change_ads_id_1(self, user_id, ads_id):
    #     """Устанавливаем id первого объявления на странице"""
    #     await self.pool.execute(f"UPDATE av_users SET ads_id_1 = {ads_id} WHERE user_id = {user_id}")
    #
    # async def change_ads_id_2(self, user_id, ads_id):
    #     """Устанавливаем id второго объявления на странице"""
    #     await self.pool.execute(f"UPDATE av_users SET ads_id_2 = {ads_id} WHERE user_id = {user_id}")
    #
    # async def change_ads_id_3(self, user_id, ads_id):
    #     """Устанавливаем id третьего объявления на странице"""
    #     await self.pool.execute(f"UPDATE av_users SET ads_id_3 = {ads_id} WHERE user_id = {user_id}")
    #
    # async def change_ads_id_4(self, user_id, ads_id):
    #     """Устанавливаем id четвертого объявления на странице"""
    #     await self.pool.execute(f"UPDATE av_users SET ads_id_4 = {ads_id} WHERE user_id = {user_id}")
    #
    # async def change_ads_id_5(self, user_id, ads_id):
    #     """Устанавливаем id пятого объявления на странице"""
    #     await self.pool.execute(f"UPDATE av_users SET ads_id_5 = {ads_id} WHERE user_id = {user_id}")

    async def set_ads_ids(self, user_id, ads_id_1, ads_id_2, ads_id_3, ads_id_4, ads_id_5):
        """Устанавливаем id первых 5-и объявлений на странице"""
        await self.pool.execute(
            f"UPDATE av_users SET ads_id_1 = {ads_id_1}, ads_id_2 = {ads_id_2}, ads_id_3 = {ads_id_3}, ads_id_4 = {ads_id_4}, ads_id_5 = {ads_id_5} WHERE user_id = {user_id}")

    async def get_last_ads_id_list(self, user_id):
        """Получаем список последних объявлений"""
        ads_ids = await self.pool.fetchrow(f'SELECT ads_id_1, ads_id_2, ads_id_3, ads_id_4, ads_id_5 FROM av_users WHERE user_id = {user_id}')
        return ads_ids

    # async def get_ads_id_1(self, user_id):
    #     """Получаем id первого объявления в списке"""
    #     return await self.pool.fetchval(f'SELECT ads_id_1 FROM av_users WHERE user_id = {user_id}')
    #
    # async def get_ads_id_2(self, user_id):
    #     """Получаем id второго объявления в списке"""
    #     return await self.pool.fetchval(f'SELECT ads_id_2 FROM av_users WHERE user_id = {user_id}')
    #
    # async def get_ads_id_3(self, user_id):
    #     """Получаем id третьего объявления в списке"""
    #     return await self.pool.fetchval(f'SELECT ads_id_3 FROM av_users WHERE user_id = {user_id}')
    #
    # async def get_ads_id_4(self, user_id):
    #     """Получаем id четвертого объявления в списке"""
    #     return await self.pool.fetchval(f'SELECT ads_id_4 FROM av_users WHERE user_id = {user_id}')
    #
    # async def get_ads_id_5(self, user_id):
    #     """Получаем id пятого объявления в списке"""
    #     return await self.pool.fetchval(f'SELECT ads_id_5 FROM av_users WHERE user_id = {user_id}')

    async def create_table_bug_reports(self):
        """Создаем таблицу с отчетами об ошибках"""
        sql = """
        CREATE TABLE IF NOT EXISTS bug_reports (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        name VARCHAR(255),
        status_report BOOL,
        report TEXT,
        date TIMESTAMP WITH TIME ZONE);
        """
        await self.pool.execute(sql)

    async def add_report(self, user_id: int, name: str, status_report: bool, report: str, date=now):
        """Добавляем отчет об ошибке в бд"""
        sql = "INSERT INTO bug_reports (user_id, name, status_report, report, date) VALUES ($1, $2, $3, $4, $5)"
        await self.pool.execute(sql, user_id, name, status_report, report, date)

    async def count_reports(self):
        """Достаем количество отчетов"""
        return await self.pool.fetchval('SELECT COUNT(*) FROM bug_reports')

    async def count_reports_with_status_0(self):
        """Достаем количество не исправленных отчетов"""
        return await self.pool.fetchval('SELECT COUNT(*) FROM bug_reports WHERE status = false')

    async def change_status_report(self, status_report, id):
        """Изменяем статус отчета"""
        await self.pool.execute(f"UPDATE bug_reports SET status_report = {status_report} WHERE id = {id}")

    async def select_all_reports(self):
        """Выбираем все отчеты"""
        sql = 'SELECT * FROM bug_reports'
        return await self.pool.fetch(sql)

    async def sellect_last_report_id(self):
        """Достаем id последнего отчета"""
        return await self.pool.fetchval(f'SELECT id FROM bug_reports ORDER BY id DESC LIMIT 1')

    async def select_all_reports_with_status(self, status_report):
        """Выбираем все отчеты"""
        sql = f'SELECT * FROM bug_reports WHERE status_report = {status_report}'
        return await self.pool.fetch(sql)
