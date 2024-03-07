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

    async def _take_page_id(self, page_type="account"):
        request_url = f"https://vk.com/{self.get_nickname()}"
        try:
            response = requests.post(
                url=request_url,
                headers=self.get_headers()
            )

            if response.status_code == 200:
                with open('logging/app.log', 'a', encoding='UTF-8') as f:
                    f.write(f"(ВК) -FINE- {response.status_code} запрос на получение информации страницы\n")
                print(f"(ВК) -FINE- {response.status_code} запрос на получение информации страницы")

                if page_type == "account":
                    return response.text.split("user_id")[1][0:20].split(":")[1].split(".")[0]  # ))
                elif page_type == "group":
                    return response.text.split("data-group_id")[1][0:20].split("\"")[1]
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

    async def create_post(self, post_text: str, page_type="account"):
        if page_type == "account":
            payload = take_payload_data('api/vk/create_post_payload/homepage_payload.json')
            acc_id = await self._take_page_id(page_type)
            ref_payload = vk_account_post_details(payload, acc_id, post_text)

        elif page_type == "group":
            payload = take_payload_data('api/vk/create_post_payload/group_payload.json')
            group_id = await self._take_page_id(page_type)
            ref_payload = vk_group_post_details(payload, group_id, post_text)

        else:
            print('неправильный "page_type"')
            return None

        coded_body = urllib.parse.urlencode(ref_payload)

        try:
            response = requests.post(
                url=url_create_post,
                json=coded_body,
                headers=self.get_headers()
            )

            if response.status_code == 200:
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
                f.write("(ВК) -ЕRROR- запрос на создание поста\n" + traceback.format_exc() +  "\n")
            print("(ВК) -ЕRROR- запрос на создание поста\n", traceback.format_exc())

            return None
