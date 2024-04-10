# File: db_base.py
____
## Class: <i>BaseDB

    Базовый класс, содержащий подключение
    к базе данных на удаленном сервере и 
    базовые методы для выполнения SQL-запросов

```python
    async def init_pool(self):
    """Метод для инициализации подключения"""

    async def execute(self, query):
    """Метод для выполнения запросов"""

    async def fetch(self, query):
    """Метод для получения данных из базы данных"""
```
___
# File: db_user.py
___
## Class: <i>UsersDB
    Класс для выполнения запросов к 
    таблице с данными пользователей
```python
    async def check(self, login):
    """Метод проверки на наличие пользователя в БД"""

    async def check_link_vk(self, login):
    """Метод проверки на наличие ссылки от сервиса ВК"""

    async def check_link_tw(self, login):
    """Метод проверки на наличие ссылки от сервиса Twitter"""

    async def get_tg_channel_id(self, login):
    """Метод для получения id канала в Telegram"""

    async def get_data_user(self, login):
    """Метод для получение данных пользователя"""

    async def insert_link_vk(self, login: int, link: str):
    """Метод для вставки в БД ссылки ВК"""

    async def delete_link_vk(self, login: int):
    """Метод для удаления ссылки ВК из БД"""

    async def insert_tg_channel_id(self, login: int, chnl_id: str):
    """Метод для вставки id канала Telegram в БД"""

    async def delete_tg_channel_id(self, login: int):
    """Метод для удаления id канала Telegram из БД"""

    async def delete_tw_cookie(self, login: int):
    """Метод для удаления cookie Twitter"""

    async def delete_vk_cookie(self, login: int):
    """Метод для удаления cookie VK"""

    async def update_cookie(self, login: str, file: str = None):
    """Метод для обновления cookie в БД"""

    async def insert_new_user(self, login):
    """Метод для вставки нового пользователя в БД"""

    @staticmethod
    def get_cookies_on_file(login: str, file: str):
    """Метод для получения cookie из файла""" 
```


