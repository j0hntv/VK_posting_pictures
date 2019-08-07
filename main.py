import requests
import random
import logging
import os
from dotenv import load_dotenv


def get_total_comics_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    total_number = response_json.get('num')
    if total_number:
        logging.info(f'Total {total_number} comics')
        return total_number
    else:
        raise requests.exceptions.HTTPError


def get_comics_data(comics_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    url = response_json.get('img')
    title = response_json.get('safe_title')
    alt = response_json.get('alt')
    if all((url, title, alt)):
        logging.info(f'Image URL: {url}')
        logging.info(f'Title: {title}')
        logging.info(f'Alt: {alt}')
        return (url, title, alt)
    else:
        raise requests.exceptions.HTTPError


def save_image(url, name):
    response = requests.get(url)
    response.raise_for_status()
    image = response.content
    with open(name, 'wb') as image_file:
        image_file.write(image)
    logging.info(f'Saved <{name}>')


def get_upload_url(GROUP_ID, ACCESS_TOKEN, V):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': ACCESS_TOKEN,
        'group_id': GROUP_ID,
        #'v': V
        }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    if not response_json.get('error'):
        upload_url = response_json['response']['upload_url']
        logging.info('Upload URL received')
        return upload_url
    else:
        raise requests.exceptions.HTTPError


def upload_image(url, image):
    image_file_descriptor = open(image, 'rb')
    files = {'photo': image_file_descriptor}
    response = requests.post(url, files=files)
    image_file_descriptor.close()
    response.raise_for_status()

    response_json = response.json()
    server = response_json.get('server')
    photo = response_json.get('photo')
    hash_ = response_json.get('hash')

    if all((server, photo, hash_)):
        logging.info('Server, photo, hash received')
        return server, photo, hash_
    else:
        raise requests.exceptions.HTTPError


def save_wall_photo(server, photo, hash_, GROUP_ID, ACCESS_TOKEN, V):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'server': server,
        'photo': photo,
        'hash': hash_,
        'group_id': GROUP_ID,
        'access_token': ACCESS_TOKEN,
        'v': V
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    if not response_json.get('error'):
        photo_id = response_json['response'][0]['id']
        owner_id = response_json['response'][0]['owner_id']
        return photo_id, owner_id
    else:
        raise requests.exceptions.HTTPError


def post_wall(photo_id, owner_id, message, GROUP_ID, ACCESS_TOKEN, V):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'owner_id': f'-{GROUP_ID}',
        'access_token': ACCESS_TOKEN,
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': message,
        'v': V
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    error = response.json().get('error')
    if not error:
        logging.info('Image successfully posted')
    else:
        raise requests.exceptions.HTTPError


def main():
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] - %(message)s')

    load_dotenv()
    GROUP_ID = os.getenv('GROUP_ID')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    V = 5.101

    try:
        total_comics_number = get_total_comics_number()
        random_image_number = random.randint(1, total_comics_number+1)
        url, title, alt = get_comics_data(random_image_number)
        image_name = os.path.basename(url)
        save_image(url, image_name)

        upload_url = get_upload_url(GROUP_ID, ACCESS_TOKEN, V)
        server, photo, hash_ = upload_image(upload_url, image_name)
        photo_id, owner_id = save_wall_photo(server, photo, hash_, GROUP_ID, ACCESS_TOKEN, V)
        message = f'{title}\n---\n{alt}'
        post_wall(photo_id, owner_id, message, GROUP_ID, ACCESS_TOKEN, V)

        os.remove(image_name)
        logging.info('Image removed')

    except requests.exceptions.HTTPError as error:
        logging.error(error)
    
    finally:
        if os.path.isfile(image_name):
            os.remove(image_name)
            logging.info('Image removed')
    

if __name__ == "__main__":
    main()
    
    
    