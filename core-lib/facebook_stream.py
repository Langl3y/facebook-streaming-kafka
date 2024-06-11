import os
import requests
from dotenv import load_dotenv
from utils import get_facebook_access_token

load_dotenv()

FB_PAGE_ID = os.getenv('FB_PAGE_ID')


def get_facebook_comments():
    access_token = get_facebook_access_token()
    url = f'https://graph.facebook.com/{FB_PAGE_ID}/comments'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


if __name__ == '__main__':
    comments = get_facebook_comments()
    for comment in comments['data']:
        print(comment['message'])
