import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_facebook_access_token():
    return os.getenv('ACCESS_TOKEN')


def get_facebook_comments():
    access_token = get_facebook_access_token()
    FB_PAGE_ID = os.getenv('FB_PAGE_ID')
    url = f'https://graph.facebook.com/{FB_PAGE_ID}/comments'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
