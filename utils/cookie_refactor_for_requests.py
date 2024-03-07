from utils.cookie_format_change import cookie_to_json


necessary_cookies_for_reply = ['remixdt', 'remixlang', 'remixstlid', 'remixstid',
                               'remixlgck', 'remixscreen_dpr', 'remixscreen_depth',
                               'remixscreen_orient', 'remixcolor_scheme_mode', 'tmr_lvid',
                               'tmr_lvidTS', 'remixuas', 'remixnttpid', 'remixsuc', 'remixdmgr',
                               'remixuacck', 'remixdark_color_scheme', 'remixrefkey', 'remixscreen_width',
                               'remixscreen_height', 'remixua', 'remixnp', 'remixgp', 'remixcurr_audio',
                               'remixscreen_winzoom', 'remixpuad', 'remixnsid', 'remixsid', 'tmr_detect']


#переводим base64 формат в json и перерабатываем нужные куки в словарь
def vk_cookie_refactor(cookies_base64: str):
    full_cookie = ''
    cookies = cookie_to_json(cookies_base64)

    for cookie in cookies:
        if cookie['name'] in necessary_cookies_for_reply:
            #print(cookie['name'])
            part_cookie = f"{cookie['name']}={cookie['value']}; "
            full_cookie += "".join(part_cookie)
            #print(full_cookie)

    return full_cookie
