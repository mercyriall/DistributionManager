import asyncio
import os
import random

from dotenv import load_dotenv
from api.vk.vk_main import VkDistribution

load_dotenv()

cookie = os.getenv('COOKIE')
acc_url = os.getenv('PAGE_URL')

post_text = "dada"
images_name = ['tyan.jpg', '5a8f918ceb6d5f875adb5c86804473f1.jpg']

async def main():
    tg_user_id = random.randint(0, 1000)
    account_url = acc_url.split("/")[-1]

    vk_manager = VkDistribution(str(tg_user_id), cookie, account_url)

    # можно ничего не передавать, дефолт значения '' и без картинки (пустой список)
    await vk_manager.create_post(post_text, images_name)


if __name__ == '__main__':
    asyncio.run(main())
