from aiogram import Bot
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder
import os


from api.twitter.twitter_main import TwitterDistribution
from api.vk.vk_main import VkDistribution
from utils.neuro_rework_text import rework_post


from database.init_db import database as db


# функция для постинга в телеграм
async def post_tg(images_dict: dict, text_dict: dict, msg: Message, bot: Bot):
    tg_channel_id = (await db.get_tg_channel_id(msg.from_user.id))[24:-3]
    if len(images_dict) == 0:
        await bot.send_message(tg_channel_id, text_dict[msg.from_user.id])
    elif len(images_dict[msg.from_user.id]) == 1:
        await bot.send_photo(tg_channel_id,
                             photo=images_dict[msg.from_user.id][0],
                             caption=text_dict[msg.from_user.id])
    else:
        album_builder = MediaGroupBuilder(
            caption=text_dict[msg.from_user.id]
        )
        for photo in images_dict[msg.from_user.id]:
            album_builder.add_photo(
                media=photo
            )
        await bot.send_media_group(tg_channel_id,
                                   media=album_builder.build()
        )


# функция для постинга в твиттер
async def post_tw(text_dict: dict, msg: Message, neuro_flag: bool):
    path = f"database/images/{str(msg.from_user.id)}"
    photos = []
    twitter_manager = TwitterDistribution(str(msg.from_user.id),
                                          (await db.get_data_user(msg.from_user.id))['tw_cookie'])
    for paths, dirs, files in os.walk(path):
        for file in files:
            photos.append(path + "/" + file)
        break
    if neuro_flag is True:
        await twitter_manager.create_tweet(await rework_post(text_dict[msg.from_user.id]), photos)
    else:
        await twitter_manager.create_tweet(text_dict[msg.from_user.id], photos)


# функция для постинга в вконтакте
async def post_vk(text_dict: dict, msg: Message, neuro_flag: bool):
    path = f"database/images/{str(msg.from_user.id)}"
    photos = []
    vk_manager = VkDistribution(str(msg.from_user.id),
                                (await db.get_data_user(msg.from_user.id))['vk_cookie'],
                                (await db.get_data_user(msg.from_user.id))['vk_link'].split("/")[-1])
    for paths, dirs, files in os.walk(path):
        for file in files:
            photos.append(path + "/" + file)
        break
    if neuro_flag is True:
        await vk_manager.create_post(await rework_post(text_dict[msg.from_user.id]), photos)
    else:
        await vk_manager.create_post(text_dict[msg.from_user.id], photos)

