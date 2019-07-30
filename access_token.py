import requests
import os
from dotenv import load_dotenv

def get_access_token_url():
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    url = 'https://oauth.vk.com/authorize'
    payload = {'client_id': client_id, 'scope': ['photos', 'groups', 'wall', 'offline']}
    response = requests.get(url, params=payload)
    return response.url
    

if __name__ == "__main__":
    access_token_url = get_access_token_url()
    print(access_token_url)
    