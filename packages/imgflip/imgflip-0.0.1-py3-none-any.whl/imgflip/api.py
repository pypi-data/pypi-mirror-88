import requests


def get_memes():
    url = 'https://api.imgflip.com/get_memes'
    r = requests.get(url)
    data = r.json()
    return data['data']['memes']


def caption_image(template_id, username, password, text0, text1):
    url = 'https://api.imgflip.com/caption_image'
    data = {
        'template_id': template_id,
        'username': username,
        'password': password,
        'text0': text0,
        'text1': text1,
    }
    r = requests.post(url, data=data)
    return r.json()
