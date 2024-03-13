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
                    except: return None

                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -FINE- {response.status_code} запрос на получение информации страницы\n")
                print(f"(ВК) -FINE- {response.status_code} запрос на получение информации страницы")

                return link_type, received_id
            else:
                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -ЕRROR- {response.status_code} запрос на получение информации страницы\n")
                print(f"(ВК) -ЕRROR- {response.status_code} запрос на получение информации страницы")

                return None

        except Exception:
            with open('logging/app.log', 'a', encoding='UTF-8') as f:
                f.write("(ВК) -ЕRROR- запрос на получение информации страницы\n" + traceback.format_exc() + "\n")
            print("(ВК) -ЕRROR- запрос на получение информации страницы\n", traceback.format_exc())

            return None
    async def _take_images_id(self, images: list):
        pass

    async def _insert_image_payload(self):
        pass

    async def create_post(self, post_text: str = 'hellyep', images: list = []):
        teg, acc_id = await self._take_page_id()
        if images != []: images_id = await self._take_images_id(images)

        if teg == 'user':
            payload = take_payload_data('api/vk/create_post_payload/homepage_payload.json')
            if images_id != None:
                await self._insert_image_payload()
            ref_payload = vk_account_post_details(payload, acc_id, post_text)

        elif teg == 'group':
            payload = take_payload_data('api/vk/create_post_payload/group_payload.json')
            if images_id != None:
                await self._insert_image_payload()
            ref_payload = vk_group_post_details(payload, acc_id, post_text)

        else:
            print('что то не так с ссылкой на аккаунт (не получается получить id профиля)')
            return None

        body = urllib.parse.urlencode(ref_payload)

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
                    f.write(f"(ВК) -ЕRROR- {response.status_code} запрос на создание поста\n")
                print(f"(ВК) -ЕRROR- {response.status_code} запрос на создание поста")

                return None
        except Exception:
            with open('logging/app.log', 'a', encoding='UTF-8') as f:
                f.write("(ВК) -ЕRROR- запрос на создание поста\n" + traceback.format_exc() + "\n")
            print("(ВК) -ЕRROR- запрос на создание поста\n", traceback.format_exc())

            return None
