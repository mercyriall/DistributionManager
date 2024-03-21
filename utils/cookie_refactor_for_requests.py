from utils.cookie_format_change import cookie_to_json


vk_necessary_cookies_for_reply = ['remixdt', 'remixlang', 'remixstlid', 'remixstid',
                               'remixlgck', 'remixscreen_dpr', 'remixscreen_depth',
                               'remixscreen_orient', 'remixcolor_scheme_mode', 'tmr_lvid',
                               'tmr_lvidTS', 'remixuas', 'remixnttpid', 'remixsuc', 'remixdmgr',
                               'remixuacck', 'remixdark_color_scheme', 'remixrefkey', 'remixscreen_width',
                               'remixscreen_height', 'remixua', 'remixnp', 'remixgp', 'remixcurr_audio',
                               'remixscreen_winzoom', 'remixpuad', 'remixnsid', 'remixsid', 'tmr_detect']

#vk_necessary_cookies_for_reply = ['remixnsid', 'remixsid']

twitter_necessary_cookies_for_reply = ["personalization_id", "att", "twid", "ct0", "auth_token", "guest_id", "g_state",
                     "guest_id_marketing", "_ga", "kdt", "lang", "gt", "_gid", "guest_id_ads"]


def vk_cookie_refactor(cookies_base64: str):
    """
    переводим base64 формат в json и перерабатываем нужные куки в словарь
    """

    full_cookie = ''
    cookies = cookie_to_json(cookies_base64)
    if cookies is None: return full_cookie

    for cookie in cookies:
        if cookie['name'] in vk_necessary_cookies_for_reply:
            part_cookie = f"{cookie['name']}={cookie['value']}; "
            full_cookie += "".join(part_cookie)

    return full_cookie


def twitter_cookie_refactor(cookies_base64):
    """
    переводим base64 формат в json и перерабатываем нужные куки в словарь
    """

    full_cookie = ''
    csrf_token = ''
    cookies = cookie_to_json(cookies_base64)
    if cookies is None: return full_cookie, csrf_token

    for cookie in cookies:
        if cookie['name'] in twitter_necessary_cookies_for_reply:
            part_cookie = f"{cookie['name']}={cookie['value']}; "
            full_cookie += "".join(part_cookie)
            if cookie['name'] in 'ct0':
                csrf_token = cookie['value']

    return full_cookie, csrf_token
