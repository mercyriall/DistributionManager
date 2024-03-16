from db_base import BaseDB
import asyncio
import re
from utils.cookie_format_change import cookie_to_base64
class DB_Users(BaseDB):
    def __init__(self):
        super().__init__()


    async def check(self, login):
        """Проверка наличия пользователя в бд"""
        query = f"""SELECT * FROM data_user WHERE tg_id='{login}'"""

        user = await self.fetch(query)
        return bool(len(user))

    async def get_data_user(self, login):
        """Метод принимает логин пользователя бота и возвращает список cookies из бд
                   Для получения конкретного cookie обращение происходит по ключам:
                   Ссылка на группу: 'link_vk'
                   Вконтакте:'cookie_vk',
                   Twitter: 'cookie_tw' """
        if not(await self.check(login)):
            await self.insert_new_user(login)


        query = f"""SELECT link_vk, cookie_vk, cookie_tw FROM data_user WHERE tg_id='{login}'"""

        cookies = await self.fetch(query)
        return cookies[0]

    async def insert_link_vk(self, login: str, link: str):
        query = f"""UPDATE data_user
                   SET link_vk = '{link}
                   WHERE tg_id = '{login}''"""
        await self.execute(query)

    async def update_cookie(self, login, files: list = None, cookie_dict: dict = None):

        if not(await self.check(login)):
            await self.insert_new_user(login)
        if cookie_dict is None and files is not None:
            cookie_dict: dict = self.get_cookies_on_file(files)

        update_params = ', '.join([f"{key} = '{cookie_to_base64(value)}'" for key, value in cookie_dict.items()])

        query = f"""UPDATE data_user
                    SET {update_params}
                    WHERE tg_id = '{login}'"""
        await self.execute(query)

    async def insert_new_user(self, login):
        query = f"""INSERT INTO data_user (tg_id)
                    VALUES ('{login}')"""

        await self.execute(query)
    @staticmethod
    def get_cookies_on_file(files: list):
        cookies_dict = {}
        for file in files:
            with open(file, 'r') as f:
                cookies_dict[file.split('.')[0]] = f.readline()
        return cookies_dict

