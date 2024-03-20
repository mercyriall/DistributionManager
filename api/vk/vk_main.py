import json
import random
import string
import traceback
import urllib
import os

import aiohttp
from dotenv import load_dotenv

from logs.logging_main import Logging
from utils.cookie_format_change import cookie_to_base64
from utils.cookie_refactor_for_requests import vk_cookie_refactor
from utils.create_request_parameters import take_payload_data, vk_account_post_details, vk_group_post_details


load_dotenv()

_proxy_token = os.getenv('PROXY_TOKEN')
_proxy_geo = os.getenv('GEO_CODE')
_user_agent = 'Mozilla/5.0'


class VkTemplate:
    def __init__(self, telegram_user_id: str, cookie: str, nickname: str):
        self._telegram_user_id = telegram_user_id
        self._proxy = (f'http://{_proxy_token}:'
                       f'sessionId={telegram_user_id}&render=false&super=true&regionalGeoCode={_proxy_geo}'
                       f'@proxy.scrape.do:8080')
        self._nickname = nickname
        self._headers = self._request_headers_create(cookie)
        self.logging = Logging()

    @staticmethod
    def _request_headers_create(cookie_base64: str):
        cookies_dictionary = vk_cookie_refactor(cookie_base64)

        return {
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': cookies_dictionary,
            'user-agent': _user_agent
        }

    def get_id(self):
        return self._telegram_user_id

    def get_proxy(self):
        return self._proxy

    def get_nickname(self):
        return self._nickname

    def get_headers(self):
        return self._headers

    def set_headers(self, cookie_base64):
        self._request_headers_create(cookie_base64)


class VkDistribution(VkTemplate):
    """
    telegram_user_id - unique
    !cookie format - base64 (decode/encode in /utils/cookie_format_change)
    nickname - only nickname, not a full link
    """

    __text_length_limit = 10000
    __images_count_limit = 10

    def __init__(self, telegram_user_id: str, cookie: str, nickname: str):
        super().__init__(telegram_user_id, cookie, nickname)

    def get_text_limit(self):
        return self.__text_length_limit

    def get_images_limit(self):
        return self.__images_count_limit

    async def create_post(self, post_text: str = '', images: list = []):
        """
        Ограничения:
            длина текста:39020(профиль), 75776(группа) с картинками хз меняется ли что - то
            лучше бы ставить ограниение сильно меньше (что я и сделал)
            количество картинок: 10 (как будто бы тоже можно поменьше выставить, но поставил 10)
        Принимает: строку + массив картинок
            можно только картинки или только текст
            Также можно ничего не передавать
        Возвращает: True/False + log
            False + "Вы не заполнили пост"
            False + "Превысили лимит длины текста/кол-во изображений"
            False + "Простите, временные неполадки в работе" (ошибка не зависит от пользователя)
            False + "Неудачная попытка, статус ошибки <status>" (ошибка в запросе, с аварийным кодом,
            проблема с куки/ссылкой или в самой программе)
            False + "Куки плохие" (ошибка в запросе, но код 200(успешный), значит плохие куки 90%
             поэтому сообщение вернется про них)
            True + "Пост создан"
        """

        url_create_post = 'https://vk.com/al_wall.php?act=post'

        if post_text == '' and images == []: return False, "Вы не заполнили пост"
        if len(post_text) > self.__text_length_limit\
            or len(images) > self.__images_count_limit: return False, "Превысили лимит длины текста/кол-во изображений"

        body = await self._create_post_preparation(post_text, images)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=url_create_post,
                        # proxy=self.get_proxy(),
                        # ssl=False,
                        json=body,
                        headers=self.get_headers()
                ) as response:
                    if response.status == 200:

                        # проверка действительно ли запрос успешный
                        try:
                            check_wrk = (await response.text()).split('statsMeta')[0][200]
                        except:
                            self.logging.warning(f"ID={self.get_id()} (VK)"
                                                 f" плохие куки, запрос на создание поста")
                            return False, "Куки плохие"

                        self.logging.info(f"ID={self.get_id()} (VK)"
                                          f" STATUS={response.status} запрос на создание поста")

                    else:
                        self.logging.warning(f"ID={self.get_id()} (VK)"
                                             f" STATUS={response.status} запрос на создание поста")
                        return False, f"Неудачная попытка, статус ошибки: {response.status}"

        except:
            self.logging.error(f"ID={self.get_id()}"
                               f" (VK) запрос на создание поста\n {traceback.format_exc()}")
            return False, "Простите, временные неполадки в работе"

        return True, "Пост создан"

    async def check_cookie_and_link(self):
        tmp1, tmp2 = await self._take_page_id()
        if tmp1 is None and tmp2 is None:
            return False
        return True

    async def _take_page_id(self):
        request_url = f"https://vk.com/{self.get_nickname()}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=request_url,
                        # proxy=self.get_proxy(),
                        # ssl=False,
                        headers=self.get_headers()
                ) as response:
                    if response.status == 200:
                        try:
                            # профиль id
                            received_id = (await response.text()).split("user_id")[1][0:20].split(":")[1].split(".")[0]
                            link_type = "user"
                        except:
                            # группа id
                            try:
                                received_id = (await response.text()).split("data-group_id")[1][0:20].split("\"")[1]
                                link_type = "group"
                            except:
                                self.logging.warning(f"ID={self.get_id()} (VK) неправильная ссылка {request_url}")
                                return None, None

                        self.logging.info(f"ID={self.get_id()} (VK)"
                                          f" запрос на получение информации страницы STATUS={response.status}")
                    else:
                        self.logging.warning(f"ID={self.get_id()} (VK)"
                                             f" запрос на получение информации страницы STATUS={response.status}")
                        return None, None

        except:
            self.logging.error(f"ID={self.get_id()} (VK)"
                               f" запрос на получение информации страницы\n {traceback.format_exc()}")
            return None, None

        return link_type, received_id

    async def _take_images_token(self, teg: str, acc_id: str):
        url_get_token = 'https://vk.com/al_photos.php?act=choose_photo'

        if teg == 'user':
            payload = take_payload_data('api/vk/create_post_payload/user_act=choose_photo.json')
            payload['to_id'] = f"{acc_id}"

        else:
            payload = take_payload_data('api/vk/create_post_payload/user_act=choose_photo.json')
            payload['_ads_group_id'] = f"{acc_id}"
            payload['to_id'] = f"-{acc_id}"

        # слайчайный набор букв и цифр длиной 10 символов
        payload['boxhash'] = ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(10)])
        body = urllib.parse.urlencode(payload)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=url_get_token,
                        # proxy=self.get_proxy(),
                        # ssl=False,
                        headers=self.get_headers(),
                        json=body
                ) as response:
                    if response.status == 200:
                        token = (await response.text()).split('token=')[1][0:411].split("'")[0]
                        self.logging.info(f"ID={self.get_id()} (VK) получение токена"
                                          f" ACC={acc_id} STATUS={response.status}")
                    else:
                        self.logging.warning(f"ID={self.get_id()} (VK) получение токена"
                                             f" ACC={acc_id} STATUS={response.status}")

        except:
            self.logging.error(f"ID={self.get_id()} (VK) получение токена ACC={acc_id}")
            return None

        return token

    async def _take_images_hash(self, images: list, teg: str, acc_id: str):
        token = await self._take_images_token(teg, acc_id)
        url_get_hash = f'https://pu.vk.com/gu/photo/v2/bulk_upload?token={token}'
        images_hash = []
        for file_name in images:
            try:
                files = aiohttp.FormData()
                files.add_field('file1',
                                open(f"database/images/{file_name}", 'rb'),
                                content_type='multipart/form-data',
                                filename=f"{file_name}"
                                )
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                            url=url_get_hash,
                            # proxy=self.get_proxy(),
                            # ssl=False,
                            data=files
                    ) as response:
                        if response.status == 200:
                            # проверка правильно ли прошел запрос
                            check_wrk = (await response.text()).split('kid')[1]
                            images_hash.append(json.loads(await response.text()))
                            self.logging.info(f"ID={self.get_id()} (VK) хеширования картинки "
                                              f"IMG={file_name} STATUS={response.status}")
                        else:
                            self.logging.warning(f"ID={self.get_id()} (VK) хеширование картинки"
                                                 f" IMG={file_name} STATUS={response.status}")

            except:
                self.logging.error(f"ID={self.get_id()} (VK) хеширование картинки"
                                   f" FILE={file_name}\n {traceback.format_exc()}")

        return images_hash

    async def _take_images_id(self, images: list, teg: str, acc_id: str):
        url_images_id = 'https://vk.com/al_photos.php?act=choose_uploaded'
        images_hash = await self._take_images_hash(images, teg, acc_id)

        if teg == 'user':
            payload = take_payload_data('api/vk/create_post_payload/user_act=choose_uploaded.json')
            payload['mid'] = acc_id
        else:
            payload = take_payload_data('api/vk/create_post_payload/group_act=choose_uploaded.json')
            payload['_ads_group_id'] = acc_id

        images_id = []
        for image_hash in images_hash:
            try:
                payload['photos'] = image_hash
                if teg == 'group': payload['mid'] = image_hash['user_id']

                # view source + url-encode + реплейсами убираем пробелы и ' переводим в "
                body = urllib.parse.urlencode(payload).replace("+", "").replace("%27", "%22")

                async with (aiohttp.ClientSession() as session):
                    async with session.post(
                            url=url_images_id,
                            # proxy=self.get_proxy(),
                            # ssl=False,
                            json=body,
                            headers=self.get_headers()
                    ) as response:
                        if response.status == 200:
                            image_id = str(payload['mid']) +\
                                       (await response.text()).split(str(payload['mid']))[1].split('"')[0]

                            images_id.append(image_id)
                            self.logging.info(f"ID={self.get_id()} (VK) получение id картинки"
                                              f" IMG_ID={image_id} TEG={teg} STATUS={response.status}")
                        else:
                            self.logging.warning(f"ID={self.get_id()} (VK) получение id картинки"
                                                 f" TEG={teg} STATUS={response.status}")

            except:
                self.logging.error(f"ID={self.get_id()} (VK) получение id картинки"
                                   f" TEG={teg}\n {traceback.format_exc()}")

        return images_id

    async def _insert_image_payload(self, payload: dict, images_id: list, teg: str):
        if teg == "user": payload['hash'] = '9f40df1c00c16002f5'
        else: payload['hash'] = '6dedfe9d7064041f35'

        for i in range(len(images_id)):
            payload.update({f'attach{i+1}_type': 'photo'})
            payload.update({f'attach{i+1}': images_id[i]})
        return payload

    async def _create_post_preparation(self, post_text: str, images: list): # формируем тело запроса
        images_id = []
        teg, acc_id = await self._take_page_id()

        if teg == 'user':
            payload = take_payload_data('api/vk/create_post_payload/user_act=post.json')
            ref_payload = vk_account_post_details(payload, acc_id, post_text)

        elif teg == 'group':
            payload = take_payload_data('api/vk/create_post_payload/group_act=post.json')
            ref_payload = vk_group_post_details(payload, acc_id, post_text)

        else:
            self.logging.warning(f'ID={self.get_id()}'
                                 f' (VK) что то не так с ссылкой на аккаунт ( не получается получить id профиля )')
            return None

        if images != []: images_id = await self._take_images_id(images, teg, acc_id)
        if images_id != []: await self._insert_image_payload(ref_payload, images_id, teg)
        
        body = urllib.parse.urlencode(ref_payload)
        return body
