import requests as req

import config as cfg


def create_paste(text: str):
    body = {
        "api_dev_key": cfg.PasteBin.key,
        "api_paste_code": text,
        "api_paste_private": 1,
        "api_paste_name": str(hash(text)),
        "api_paste_expire_date": "10M",
        "api_paste_format": "text",
        "api_option": "paste",
    }
    response = req.post('https://pastebin.com/api/api_post.php', data=body)

    return response.text
