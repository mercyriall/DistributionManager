import asyncio
import os
import random

from dotenv import load_dotenv
from api.vk.vk_main import VkDistribution

load_dotenv()

cookie = os.getenv('COOKIE')
acc_url = os.getenv('PAGE_URL')

post_text = "helyep"

async def main():
    tg_user_id = random.randint(0, 1000)
    account_url = acc_url.split("/")[-1]

    await VkDistribution(str(tg_user_id), cookie, account_url).create_post(post_text, "group")


if __name__ == '__main__':
    asyncio.run(main())
