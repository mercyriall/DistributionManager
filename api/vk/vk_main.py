from abc import ABC, abstractmethod
import os

from dotenv import load_dotenv
from utils.cookie_refactor_for_requests import vk_cookie_refactor


load_dotenv()

proxy_url = os.getenv('PROXY_TOKEN')
proxy_geo = os.getenv('GEO_CODE')
user_agent = os.getenv('USER_AGENT')

class VkTemplate(ABC):
    def __init__(self, id: str, cookie: str):
        self._id = id
        self._proxy = f'http://{proxy_url}:sessionId={id}&render=false&super=true&regionalGeoCode={proxy_geo}@proxy.scrape.do:8080'
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

    def get_headers(self):
        return self._headers

class VkDistribution(VkTemplate):
    def __init__(self, id: str, cookie: str):
        super().__init__(id, cookie)

    async def start_vk_distribution(self):
        await self._create_post()

    async def _create_post(self):
        pass
