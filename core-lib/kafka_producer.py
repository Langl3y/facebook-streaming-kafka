import os
from os.path import dirname, join
import requests
import time
from confluent_kafka import Producer
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

access_token = os.environ.get('ACCESS_TOKEN')
page_id = os.environ.get('FB_PAGE_ID')
post_id = os.environ.get('FB_POST_ID')

conf = {'bootstrap.servers': "localhost:9092"}
producer = Producer(**conf)


def get_comments(access_token, page_id, post_id):
    url = f'https://graph.facebook.com/v11.0/{page_id}_{post_id}/comments'
    params = {
        'access_token': access_token,
        'summary': 'true',
        'filter': 'stream',
        'order': 'reverse_chronological'
    }
    response = requests.get(url, params=params)
    return response.json()


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


while True:
    comments_data = get_comments(access_token, page_id, post_id)
    comments = comments_data.get('data', [])
    for comment in comments:
        producer.produce('facebook_comments', key=comment['id'], value=comment['message'], callback=delivery_report)
    producer.flush()
    time.sleep(10)
