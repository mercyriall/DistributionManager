import json

from aiogram.types import Message
from database.db_base import BaseDB
from utils.cookie_format_change import cookie_to_base64


class UsersDB(BaseDB):
    def __init__(self):
        super().__init__()

    async def check(self, login):
        """
        Проверка наличия пользователя в бд
        """

        query = f"""SELECT * FROM data_user WHERE tg_id='{login}'"""

        user = await self.fetch(query)
        return bool(len(user))

    async def check_link_vk(self, login):
        query = f"""SELECT vk_link FROM data_user WHERE tg_id='{login}'"""
        n = "None"
        user = await self.fetch(query)
        if n in str(user):
            return False
        else:
            return True

    async def check_link_tw(self, login):
        query = f"""SELECT tw_link FROM data_user WHERE tg_id='{login}'"""
        n = "None"
        user = await self.fetch(query)
        if n in str(user):
            return False
        else:
            return True

    async def get_tg_channel_id(self, login):
        query = f"""SELECT tg_channel_id FROM data_user WHERE tg_id='{login}'"""
        user = await self.fetch(query)
        return str(user)

    async def get_data_user(self, login):
        """
        Метод принимает логин пользователя бота и возвращает список cookies из бд
        Для получения конкретного cookie обращение происходит по ключам:
        Ссылка на группу: 'vk_link'
        Вконтакте:'vk_cookie',
        Twitter: 'tw_cookie'
        """

        if not (await self.check(login)):
            await self.insert_new_user(login)

        query = f"""SELECT vk_cookie, tw_cookie, tg_channel_id, vk_link FROM data_user WHERE tg_id='{login}'"""

        cookies = await self.fetch(query)
        return cookies[0]

    async def insert_link_vk(self, login: int, link: str):
        query = f"""UPDATE data_user
                   SET vk_link = '{link}'
                   WHERE tg_id = '{login}'"""
        await self.execute(query)

    async def delete_link_vk(self, login: int):
        query = f"""UPDATE data_user
                   SET vk_link = NULL
                   WHERE tg_id = '{login}'"""
        await self.execute(query)

    async def insert_tg_channel_id(self, login: int, chnl_id: str):
        query = f"""UPDATE data_user
                   SET tg_channel_id = '{chnl_id}'
                   WHERE tg_id = '{login}'"""
        await self.execute(query)

    async def delete_tg_channel_id(self, login: int):
        query = f"""UPDATE data_user
                   SET tg_channel_id = NULL
                   WHERE tg_id = '{login}'"""
        await self.execute(query)

    async def delete_tw_cookie(self, login: int):
        query = f"""UPDATE data_user
                   SET tw_cookie = NULL
                   WHERE tg_id = '{login}'"""
        await self.execute(query)

    async def delete_vk_cookie(self, login: int):
        query = f"""UPDATE data_user
                   SET vk_cookie = NULL
                   WHERE tg_id = '{login}'"""
        await self.execute(query)

    async def update_cookie(self, login: str, file: str = None):

        if not (await self.check(login)):
            await self.insert_new_user(login)

        if file is None:
            return 0

        cookie: str = self.get_cookies_on_file(login, file)

        query = f"""UPDATE data_user
                    SET {file.split('.')[0]} = '{cookie}'
                    WHERE tg_id = '{login}'"""

        await self.execute(query)

    async def insert_new_user(self, login):
        query = f"""INSERT INTO data_user (tg_id)
                    VALUES ('{login}')"""

        await self.execute(query)

    @staticmethod
    def get_cookies_on_file(login: str, file: str):
        path = f"database/uploaded_cookies/{login}"

        with open(f"{path}/{file}", "r") as f:
            cookie = f.read()
        json_cookie = json.loads(cookie)
        cookie_ready_for_using = cookie_to_base64(json_cookie)
        return cookie_ready_for_using
    