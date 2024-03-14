import json
import random
import string
import traceback
import urllib
from abc import ABC
import os

import requests
from dotenv import load_dotenv
from utils.cookie_refactor_for_requests import vk_cookie_refactor
from utils.create_request_parameters import take_payload_data, vk_account_post_details, vk_group_post_details


load_dotenv()

proxy_url = os.getenv('PROXY_TOKEN')
proxy_geo = os.getenv('GEO_CODE')
user_agent = os.getenv('USER_AGENT')

url_create_post = 'https://vk.com/al_wall.php?act=post'

class VkTemplate(ABC):
    def __init__(self, id: str, cookie: str, nickname: str):
        self._id = id
        self._proxy = f'http://{proxy_url}:sessionId={id}&render=false&super=true&regionalGeoCode={proxy_geo}@proxy.scrape.do:8080'
        self._nickname = nickname
        self._headers = self._request_headers_create(cookie)

    def _request_headers_create(self, cookie: str):
        cookies_dictionary = vk_cookie_refactor(cookie)

        return {
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': cookies_dictionary,
            'user-agent': user_agent
        }

    def get_id(self):
        return self._id

    def get_proxy(self):

        return self._proxy
    def get_nickname(self):
        return self._nickname

    def get_headers(self):
        return self._headers

class VkDistribution(VkTemplate):
    def __init__(self, id: str, cookie: str, nickname: str):
        super().__init__(id, cookie, nickname)

    async def _take_page_id(self):
        request_url = f"https://vk.com/{self.get_nickname()}"
        try:
            response = requests.post(
                url=request_url,
                headers=self.get_headers()
            )

            if response.status_code == 200:
                try:
                    # профиль
                    received_id = response.text.split("user_id")[1][0:20].split(":")[1].split(".")[0]  # ))
                    link_type = "user"
                except:
                    # группа
                    try:
                        received_id = response.text.split("data-group_id")[1][0:20].split("\"")[1]
                        link_type = "group"
                    except: return None, None

                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -FINE- {response.status_code} запрос на получение информации страницы\n")
                print(f"(ВК) -FINE- {response.status_code} запрос на получение информации страницы")

                return link_type, received_id
            else:
                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -ЕRROR- {response.status_code} запрос на получение информации страницы\n")
                print(f"(ВК) -ЕRROR- {response.status_code} запрос на получение информации страницы")

                return None, None

        except Exception:
            with open('logging/app.log', 'a', encoding='UTF-8') as f:
                f.write("(ВК) -ЕRROR- запрос на получение информации страницы\n" + traceback.format_exc() + "\n")
            print("(ВК) -ЕRROR- запрос на получение информации страницы\n", traceback.format_exc())

            return None, None


    async def _take_images_token(self, teg: str, acc_id: str):
        url_get_token = 'https://vk.com/al_photos.php?act=choose_photo'

        if teg == 'user':
            payload = take_payload_data('api/vk/create_post_payload/user_act=choose_photo.json')
            payload['to_id'] = f"{acc_id}"
            # слайчайный набор букв и цифр длиной 10 символов
            payload['boxhash'] = [random.choice(string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase) for i in range(10)]
        else:
            payload = take_payload_data('api/vk/create_post_payload/user_act=choose_photo.json')
            payload['_ads_group_id'] = f"{acc_id}"
            payload['to_id'] = f"-{acc_id}"
            # слайчайный набор букв и цифр длиной 10 символов
            payload['boxhash'] = [random.choice(string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase) for i in range(10)]

        body = urllib.parse.urlencode(payload)
        try:
            response = requests.post(
                url=url_get_token,
                headers=self.get_headers(),
                json=body
            )
            #print(f"(ВК) -FINE- получение токена {response.text.split('token=')[1][0:411]}")
            return response.text.split('token=')[1][0:411]
        except:
            with open('logging/app.log', 'a', encoding='UTF-8') as f:
                f.write(f"(ВК) -ERROR- ошибка получения токена {acc_id}\n")
            print(f"(ВК) -ERROR- ошибка получения токена {acc_id}")
            return None

    async def _take_images_hash(self, images: list, teg: str, acc_id: str):
        token = await self._take_images_token(teg, acc_id)
        url_get_hash = f'https://pu.vk.com/gu/photo/v2/bulk_upload?token={token}'
        images_hash = []
        for file_name in images:
            try:
                response = requests.post(
                    url=url_get_hash,
                    files={
                        'file1': (
                            f"database/images/{file_name}",
                            open(f"database/images/{file_name}", 'rb'),
                            'multipart/form-data',
                        )
                    }
                )
                response.text.split('kid')[1] # проверка правильно ли прошел запрос
                images_hash.append(json.loads(response.text))
            except:
                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -ERROR- ошибка хеширования картинки {file_name}\n" + traceback.format_exc() + "\n")
                print(f"(ВК) -ERROR- ошибка хеширования картинки {file_name}\n" + traceback.format_exc() + "\n")

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

                response = requests.post(
                    url=url_images_id,
                    headers=self.get_headers(),
                    json=body
                )
                images_id.append(str(payload['mid']) + response.text.split(str(payload['mid']))[1].split('"')[0])
            except:
                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -ERROR- ошибка получения id картинки {teg}\n" + traceback.format_exc() + "\n")
                print(f"(ВК) -ERROR- ошибка получения id картинки {teg}" + traceback.format_exc() + "\n")

        return images_id

    async def _insert_image_payload(self, payload: json, images_id: list):
        payload['primary_attachments_mode'] = 'grid'
        payload['hash'] = '6dedfe9d7064041f35'
        for i in range(len(images_id)):
            payload.update({f'attach{i+1}_type': 'photo'})
            payload.update({f'attach{i+1}': images_id[i]})
        return payload


    async def _create_post_preparation(self, post_text: str, images: list): # формируем тело запроса
        images_id = None
        teg, acc_id = await self._take_page_id()

        if teg == 'user':
            payload = take_payload_data('api/vk/create_post_payload/user_act=post.json')
            ref_payload = vk_account_post_details(payload, acc_id, post_text)

        elif teg == 'group':
            payload = take_payload_data('api/vk/create_post_payload/group_act=post.json')
            ref_payload = vk_group_post_details(payload, acc_id, post_text)

        else:
            print('что то не так с ссылкой на аккаунт (не получается получить id профиля)')
            return None

        if images != []: images_id = await self._take_images_id(images, teg, acc_id)
        if images_id != []: await self._insert_image_payload(ref_payload, images_id)

        body = urllib.parse.urlencode(ref_payload)

        return body

    async def create_post(self, post_text: str = '', images: list = []):
        body = await self._create_post_preparation(post_text, images)

        try:
            response = requests.post(
                url=url_create_post,
                json=body,
                headers=self.get_headers()
            )

            if response.status_code == 200:
                response.text.split('statsMeta')[0][200] # проверка действительно ли запрос успешный

                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -FINE- {response.status_code} запрос на создание поста\n")
                print(f"(ВК) -FINE- {response.status_code} запрос на создание поста")

            else:
                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -ERROR- {response.status_code} запрос на создание поста\n")
                print(f"(ВК) -ERROR- {response.status_code} запрос на создание поста")

                return None
        except Exception:
            with open('logging/app.log', 'a', encoding='UTF-8') as f:
                f.write("(ВК) -ERROR- запрос на создание поста\n" + traceback.format_exc() + "\n")
            print("(ВК) -ERROR- запрос на создание поста\n", traceback.format_exc())

            return None
