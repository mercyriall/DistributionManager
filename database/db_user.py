from db_base import BaseDB
from utils.cookie_format_change import cookie_to_base64

class DB_Users(BaseDB):
    def __init__(self):
        super().__init__()

    async def check(self, login):
        """
            Проверка наличия пользователя в бд
        """
        query = f"""SELECT * FROM users WHERE username='{login}'"""

        user = await self.fetch(query)
        return bool(len(user))

    async def get_cookies(self, login):
        """
            Метод принимает логин пользователя бота и возвращает список cookies из бд
            Для получения конкретного cookie обращение происходит по ключам:
            Вконтакте: 'cookie_vk',
            Instagram: 'cookie_insta'
            Telegram: 'cookie_tg'
        """

        query = f"""SELECT cookie_vk, cookie_insta, cookie_tg FROM users WHERE username='{login}'"""

        cookies = await self.fetch(query)
        return cookies[0]

    async def update_cookie(self, login, files: list):
        update_params = ''

        if not (await self.check(login)):
            await self.insert_new_user(login)

        cookie_dict: dict = self.get_cookies_on_files(files)

        for key, value in cookie_dict.items():
            value = cookie_to_base64(value)
            update_params += ', '.join(f"{key} = '{value}'")

        query = f"""UPDATE users
                    SET {update_params}
                    WHERE username = '{login}'"""
        await self.execute(query)

    async def insert_new_user(self, login):
        query = f"""INSERT INTO users (username)
                    VALUES ('{login}')"""

        await self.execute(query)

    @staticmethod
    def get_cookies_on_files(files: list):
        cookies_dict = {}
        for file in files:
            with open(file, 'r') as f:
                cookies_dict[file.split('.')[0]] = f.readline()
        return cookies_dict
