import os
import asyncpg
from dotenv import load_dotenv
class BaseDB:
    _instance = None
    def __init__(self):
        self.pool = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    async def init_pool(self):
        load_dotenv()

        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv("DB_PASSWORD")

        self.pool = await asyncpg.create_pool(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    async def execute(self, query):
        async with self.pool.acquire() as connection:
            return await connection.execute(query)

    async def fetch(self, query):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query)
