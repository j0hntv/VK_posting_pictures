import requests
import random
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] - %(message)s')


def save_image(url, name):
    response = requests.get(url)
    response.raise_for_status()
    image = response.content
    with open(name, 'wb') as image_file:
        image_file.write(image)
    logging.info(f'Saved <{name}>')


def get_comics_data(comics_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    logging.info(f'Response received')
    json = response.json()
    url = json.get('img')
    title = json.get('safe_title')
    alt = json.get('alt')
    return (url, title, alt)


def main():
    random_image_number = random.randint(1, 1000)
    url, title, alt = get_comics_data(random_image_number)
    name = url.split('/')[-1]
    save_image(url, name)
    print(title)
    print(alt)


if __name__ == "__main__":
    main()