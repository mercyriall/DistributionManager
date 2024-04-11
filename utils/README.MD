### check_link.py

---
```python
async def check_linked_soc_list(msg: Message):
    """функция для определения привязанных соц сетей"""
```
```python
async def check_for_buttons(msg: Message):
    """функция для выбора соц сетей для постинга"""
```
### cookie_format_change.py

---
```python
def cookie_to_base64(cookie_json):
    """принимает cookie в формате json
    возвращает cookie в формате base64"""
```
```python
def cookie_to_json(cookie_base64):
    """принимает cookie в формате base64
    возвращает cookie в формате json"""
```
### cookie_refactor_for_requests.py

---
```python
def vk_cookie_refactor(cookies_base64: str):
    """принимает куки в формате base64
    возвращает строку(куки)
    получает из вк куки пользователя только необходимые поля и
    формирует из них формат key=value;"""
```
```python
def twitter_cookie_refactor(cookies_base64):
    """принимает куки в формате base64
     возвращает две строки(куки, токен)
     получает из вк куки пользователя только необходимые поля и
    формирует из них формат key=value;"""
```
### create_request_parameters.py

---
```python
def vk_account_post_details(payload, account_id, post_text):
    """формирует payload данные для постинка в профиль в вк"""
```
```python
def vk_group_post_details(payload, group_id, post_text):
    """формирует payload данные для постинка в группу в вк"""
```
```python
def take_payload_data(payload_file_path):
    """открывает json файл (взвращает json)"""
```
### neuro_rework_text.py

---
```python
async def rework_post(title):
    """GigaChat возвращает текст с таким же смыслом, но другими словами"""
```
### post_functions.py

---
```python
async def post_tg(images_dict: dict, text_dict: dict, msg: Message, bot: Bot):
    """функция для постинга в телеграм"""
```
```python
async def post_tw(images_dict: dict, text_dict: dict, msg: Message, bot: Bot):
    """функция для постинга в твиттер"""
```
```python
async def post_vk(images_dict: dict, text_dict: dict, msg: Message, bot: Bot):
    """функция для постинга в вк"""
```