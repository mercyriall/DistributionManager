# Directory: twitter

---
 - CreateTweet.json - payload file for create post

---
### twitter_main.py
```python
    class TwitterTemplate:
    """
    базовый класс содержащий headers запроса и 
    неизменяемые поля привязанные к пользователю
    """
```
---

```python
    class TwitterDistribution(TwitterTemplate):
    """
    класс для создания поста в твитере
    наследует поля для аутентификации пользователя
    """
```
 ```python
    def get_text_limit(self):
    """
    возвращает ограничение на длину текста для твитера
    """
```
```python
    def get_images_limit(self):
    """
    возвращает ограничение на количество изображений для твитера
    """
```
```python
    async def create_tweet(self, tweet_text: str = '', images: list = []):
    """
        Ограничения:
            длина текста: 280
            количество картинок: 4
        Принимает: строку + массив картинок
            можно только картинки или только текст
            Также можно ничего не передавать
        Возвращает: tweet_id/False + log
            False + "Вы не заполнили пост"
            False + "Превысили лимит длины текста/кол-во изображений"
            False + "Простите, временные неполадки в работе" (ошибка не зависит от пользователя)
            False + "Неудачная попытка, статус ошибки: <status>" (ошибка в запросе, с аварийным кодом,
            проблема с куки/ссылкой или в самой программе)
            False + "Куки плохие" (ошибка в запросе, но код 200(успешный), значит плохие куки 90%
             поэтому сообщение вернется про них)
            tweet_id + "Пост создан"
    """
```
```python
    async def check_cookie(self):
    """
    проверка работоспособности куки, сразу можно выдать
    пользователю фидбек правильно ли он импортировал куки
    """
```
```python
    async def _delete_tweet(self, tweet_id: str):
    """
    удаление поста (применяется при проверке на качество куки) 
    """
```
```python
    async def _prepare_payload(self, payload: dict, tweet_text: str, images: list):
    """
    формируем payload файл для определенного юзера;текста;изображений
    """
```
```python
    async def _command_INIT(self, images: list):
    """
    этап вставки картинки(1/3)
    запрос на инициализацию изображения в твитере
    """
```
```python
    async def _command_APPEND(self, images: list, images_id: list):
    """
    этап вставки картинки(2/3)
    запрос с передачей файла (изображения)
    """
```
```python
    async def _command_FINALIZE(self, images_id: list):
    """
    этап вставки картинки(3/3)
    финальный запрос на импорт картинки в твитер
    """
```
```python
    async def _get_images_id(self, images: list):
    """
    получаем присвоенный id нашей картинке 
    (выдается по размеру изображения)
    """
```

# Directory: vk

---
## Directory create_post_payload

 - group_act=choose_photo.json - payload file for create post with image in group
 - group_act=choose_uploaded.json - payload file for create image hash in group
 - group_act=post.json - payload file for create post without image in group
 - user_act=choose_photo.json - payload file for create post with image in profile
 - user_act=choose_uploaded.json - payload file for create image hash in profile
 - user_act=post.json - payload file for create post without image in profile

---
### vk_main.py
```python
    class VkTemplate:
    """
    базовый класс содержащий headers запроса и 
    неизменяемые поля привязанные к пользователю
    """
```
---

```python
    class VkDistribution(VkTemplate):
    """
    класс для создания поста в вк
    наследует поля для аутентификации пользователя
    """
```
 ```python
    def get_text_limit(self):
    """
    возвращает ограничение на длину текста для вк
    """
```
```python
    def get_images_limit(self):
    """
    возвращает ограничение на количество изображений для вк
    """
```
```python
    async def create_post(self, tweet_text: str = '', images: list = []):
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
```
```python
    async def check_cookie_and_link(self):
    """
    проверка работоспособности куки и правильность ссылки,
     сразу можно выдать
    пользователю фидбек правильно ли он импортировал куки и
    правильную ли ссылку указал
    """
```
```python
    async def _take_page_id(self):
    """
    получаем id привязанное к аккаунту юзера (соц сети, а не тг)
    """
```
```python
    async def _take_images_token(self, teg: str, acc_id: str):
    """
    получаем token привязанный к изображения
    """
```
```python
    async def _take_images_id(self, images: list, teg: str, acc_id: str):
    """
    получаем id изображения
    """
```
```python
    async def _insert_image_payload(self, payload: dict, images_id: list, teg: str):
    """
    импортируем полученные данные изображения в 
    payload файл
    """
```
```python
    async def _create_post_preparation(self, post_text: str, images: list):
    """
    формируем payload файл проверяя есть ли
    переданные изображения и куда постим (группа, профиль)
    """
```