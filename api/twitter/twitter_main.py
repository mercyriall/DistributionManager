import json
import os
import random
import string
import traceback

import aiohttp
from dotenv import load_dotenv

from logs.logging_main import Logging
from utils.cookie_refactor_for_requests import twitter_cookie_refactor
from utils.create_request_parameters import take_payload_data

load_dotenv()

_proxy_token = os.getenv('PROXY_TOKEN')
_proxy_geo = os.getenv('GEO_CODE')
_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
_bearer = os.getenv('TWITTER_BEARER')
_tweet_key = os.getenv('TWITTER_TWEET_KEY')


class TwitterTemplate():
    def __init__(self, id: str, cookie: str):
        self._id = id
        self._proxy = f'http://{_proxy_token}:sessionId={id}&render=false&super=true&regionalGeoCode={_proxy_geo}@proxy.scrape.do:8080'
        self._headers = self._request_headers_create(cookie)
        self.logging = Logging()

    @staticmethod
    def _request_headers_create(cookie: str):
        cookies_dictionary, csrf_token = twitter_cookie_refactor(cookie)

        return {
            'content-type': 'application/json',
            'authorization': f'Bearer {_bearer}',
            'cookie': cookies_dictionary,
            'user-agent': _user_agent,
            'x-csrf-token': csrf_token
        }

    def get_id(self):
        return self._id

    def get_proxy(self):
        return self._proxy

    def get_headers(self):
        return self._headers


class TwitterDistribution(TwitterTemplate):
    def __init__(self, id: str, cookie: str):
        super().__init__(id, cookie)

    def update_cookie(self):
        #запрос на получение куки
        #cookie_base64 = cookie_to_base64(cookie_json)
        #self.set_headers(cookie_base64)
        #return cookie_base64
        pass

    async def check_cookie(self):
        # слайчайный набор букв и цифр длиной 10 символов
        random_tweet = ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(10)])
        tweet_id = await self.create_tweet(random_tweet)

        if tweet_id is False:
            return False
        else:
            if not await self._delete_tweet(tweet_id):
                self.logging.error(f"ID={self.get_id()}"
                                    f" (TWITTER) удаление поста")
            self.logging.info(f"ID={self.get_id()}"
                                    f" (TWITTER) проверка куки")
            return True

    async def _delete_tweet(self, tweet_id: str):
        query_id = "VaenaVgh5q5ih7kvyVjgtg"
        url_delete_tweet = f"https://twitter.com/i/api/graphql/{query_id}/DeleteTweet"

        payload = {
            "variables": {
                "tweet_id": f"{tweet_id}",
                "dark_request": False
            },
            "queryId": f"{query_id}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=url_delete_tweet,
                    # proxy=self.get_proxy(),
                    # ssl=False,
                    json=payload,
                    headers=self.get_headers()
            ) as response:
                if response.status == 200:
                    return True
                else:
                    return False

    async def create_tweet(self, tweet_text: str = '', images: list = []):
        url_create_tweet = f'https://twitter.com/i/api/graphql/{_tweet_key}/CreateTweet'
        if tweet_text == '' and images == []: return False
        template_payload = take_payload_data('api/twitter/CreateTweet.json')
        payload = await self._prepare_payload(template_payload, tweet_text, images)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=url_create_tweet,
                        # proxy=self.get_proxy(),
                        # ssl=False,
                        json=payload,
                        headers=self.get_headers()
                ) as response:
                    if response.status == 200:
                        data_dict = json.loads(await response.text())
                        tweet_id = data_dict['data']['create_tweet']['tweet_results']['result']['rest_id'] # для удаления при проверке
                        self.logging.info(f"ID={self.get_id()}"
                                           f" (TWITTER) создание поста")
                    else:
                        self.logging.warning(f"ID={self.get_id()} STATUS={response.status}"
                                   f" (TWITTER) создание поста")
                        return False

        except:
            self.logging.error(f"ID={self.get_id()}"
                                   f" (TWITTER) создание поста\n {traceback.format_exc()}")
            return False

        return tweet_id

    async def _prepare_payload(self, payload: dict, tweet_text: str, images: list):
        if tweet_text != '':
            payload['variables']['tweet_text'] = tweet_text
        payload['queryId'] = _tweet_key

        images_id = await self._get_images_id(images)

        json_image_id = []
        for image_id in images_id:
            json_image_id.append({"media_id": f"{image_id}", "tagged_users": []})
        payload['variables']['media']['media_entities'] = json_image_id

        return payload

    async def _command_INIT(self, images: list):
        images_total_bytes = []
        images_id = []
        headers = self.get_headers()
        headers.update({"referer": "https://twitter.com/"})
        headers.pop("content-type", None)

        for image in images:
            file_path = f'database/images/{image}'
            images_total_bytes.append(os.path.getsize(file_path))

        for image_total_bytes in images_total_bytes:
            url_init = (f'https://upload.twitter.com/i/media/upload.json?'
                        f'command=INIT&total_bytes={image_total_bytes}&media_type=image%2Fjpeg&media_category=tweet_image')
            try:

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                            url=url_init,
                            # proxy=self.get_proxy(),
                            # ssl=False,
                            headers=headers
                    ) as response:
                        if response.status == 200 or response.status == 202:
                            json_data = json.loads(await response.text())
                            images_id.append(json_data['media_id_string'])

                            self.logging.info(f"ID={self.get_id()} TOTAL_BYTES={image_total_bytes} (TWITTER)"
                                              f" STATUS={response.status} INIT STAGE")
                        else:
                            self.logging.warning(f"ID={self.get_id()} TOTAL_BYTES={image_total_bytes} (TWITTER)"
                                                 f" STATUS={response.status} INIT STAGE")

            except:
                self.logging.error(f"ID={self.get_id()} TOTAL_BYTES={image_total_bytes}"
                                   f" (TWITTER) INIT STAGE\n {traceback.format_exc()}")
        return images_id

    async def _command_APPEND(self, images: list, images_id: list):
        activate_id = []
        headers = self.get_headers()
        headers.update({"origin": "https://twitter.com"})
        headers.pop("content-type", None)
        for i in range(len(images_id)):
            url_append = f'https://upload.twitter.com/i/media/upload.json?command=APPEND&media_id={images_id[i]}&segment_index=0'
            files = aiohttp.FormData()
            files.add_field('media',
                            open(f"database/images/{images[i]}", 'rb'),
                            content_type='multipart/form-data; boundary=----WebKitFormBoundaryQykHaFZ7kqbjoaVF',
                            filename=f"{images[i]}"
                            )
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                            url=url_append,
                            headers=headers,
                            # proxy=self.get_proxy(),
                            # ssl=False,
                            data=files
                    ) as response:
                        if response.status == 200 or response.status == 204:
                            activate_id.append(images_id[i])

                            self.logging.info(f"ID={self.get_id()} (TWITTER)"
                                                     f" STATUS={response.status} APPEND STAGE")
                        else:
                            self.logging.warning(f"ID={self.get_id()} (TWITTER)"
                                                     f" STATUS={response.status} APPEND STAGE")

            except:
                self.logging.error(f"ID={self.get_id()}"
                                   f" (TWITTER) APPEND STAGE\n {traceback.format_exc()}")
        return activate_id

    async def _command_FINALIZE(self, images_id: list):
        original_md5 = '1e0ddfe203fb440506cf5dd9c34e3e4c'

        headers = self.get_headers()
        headers.update({"referer": "https://twitter.com/"})
        headers.pop("content-type", None)

        for i in range(len(images_id)):
            url_finalize = f'https://upload.twitter.com/i/media/upload.json?command=FINALIZE&media_id={images_id[i]}&original_md5={original_md5}'

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                            url=url_finalize,
                            # proxy=self.get_proxy(),
                            # ssl=False,
                            headers=headers
                    ) as response:
                        if response.status == 200 or response.status == 201:
                            json_data = json.loads(await response.text())
                            images_id.append(json_data['media_id_string'])

                            self.logging.info(f"ID={self.get_id()} (TWITTER)"
                                              f" STATUS={response.status} FINALIZE STAGE")
                        else:
                            self.logging.warning(f"ID={self.get_id()} (TWITTER)"
                                                 f" STATUS={response.status} FINALIZE STAGE")

            except:
                self.logging.error(f"ID={self.get_id()}"
                                   f" (TWITTER) FINALIZE STAGE\n {traceback.format_exc()}")

    async def _get_images_id(self, images: list):
        images_id = await self._command_INIT(images)
        activate_id = await self._command_APPEND(images, images_id)
        finalize = await self._command_FINALIZE(images_id)
        return activate_id
