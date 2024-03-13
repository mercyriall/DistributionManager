from db_base import BaseDB
import asyncio
import re

class DB_Users(BaseDB):
    def __init__(self):
        super().__init__()


    async def check(self, login):
        """Проверка наличия пользователя в бд"""
        query = f"""SELECT * FROM users WHERE username='{login}'"""

        user = await self.fetch(query)
        return bool(len(user))

    async def get_cookies(self, login):
        """Метод принимает логин пользователя бота и возвращает список cookies из бд
           Для получения конкретного cookie обращение происходит по ключам:
           Вконтакте:'cookie_vk',
           Instagram:'cookie_insta'
           Telegram: 'cookie_tg'"""

        query = f"""SELECT cookie_vk, cookie_insta, cookie_tg FROM users WHERE username='{login}'"""

        cookies = await self.fetch(query)
        return cookies[0]
    async def insert_cookie(self, login, cookies: dict):
        pass

    @staticmethod
    def get_cookies_on_file(files: list):
        cookies_dict = {}
        for file in files:
            with open(file, 'r') as f:
                cookies_dict[file.split('.')[0]] = f.readline()
        return cookies_dict


async def main():
    db = DB_Users()
    db2 = DB_Users()
    print(id(db), id(db2))

    await db.init_pool()
    flag = await db2.check('kjs')
    print(flag)
    cookies = db.get_cookies_on_file(['insta.txt', 'tg.txt', 'vk.txt'])
    print(cookies)
asyncio.run(main())