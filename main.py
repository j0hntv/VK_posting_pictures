import requests
import random
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] - %(message)s')


def get_comics_data(comics_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    logging.info('Response received')
    json = response.json()
    url = json.get('img')
    title = json.get('safe_title')
    alt = json.get('alt')
    logging.info(f'Image URL: {url}')
    logging.info(f'Title: {title}')
    logging.info(f'Alt: {alt}')
    return (url, title, alt)


def save_image(url, name):
    response = requests.get(url)
    response.raise_for_status()
    image = response.content
    with open(name, 'wb') as image_file:
        image_file.write(image)
    logging.info(f'Saved <{name}>')


def get_upload_url():
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {'access_token': ACCESS_TOKEN,
               'group_id': GROUP_ID,
               'v': V}

    response = requests.get(url, params=payload)
    response_json = response.json()
    upload_url = response_json['response']['upload_url']
    logging.info('Upload URL received')
    return upload_url


def upload_image(url, image):
    image_file_descriptor = open(image, 'rb')
    files = {'photo': image_file_descriptor}
    response = requests.post(url, files=files)
    image_file_descriptor.close()

    response_json = response.json()
    server = response_json.get('server')
    photo = response_json.get('photo')
    hash_ = response_json.get('hash')

    if all((server, photo, hash_)):
        logging.info('Server, photo, hash received')
        return server, photo, hash_
    else:
        raise requests.exceptions.HTTPError

def save_wall_photo(server, photo, hash_):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'server': server,
        'photo': photo,
        'hash': hash_,
        'group_id': GROUP_ID,
        'access_token': ACCESS_TOKEN,
        'v': V
    }
    response = requests.get(url, params=payload)
    return response.json()


def main():
    random_image_number = random.randint(1, 1000)
    url, title, alt = get_comics_data(random_image_number)
    image_name = url.split('/')[-1]
    save_image(url, image_name)
    upload_url = get_upload_url()
    server, photo, hash_ = upload_image(upload_url, image_name)
    save_wall_photo(server, photo, hash_)


if __name__ == "__main__":
    load_dotenv()
    GROUP_ID = os.getenv('GROUP_ID')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    V = 5.101
    main()
    
    