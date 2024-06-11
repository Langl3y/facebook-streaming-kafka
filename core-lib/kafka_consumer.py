import json

from confluent_kafka import Consumer, KafkaError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Kafka configuration
with open('config.json') as config_file:
    conf = json.load(config_file)

consumer = Consumer(**conf)
consumer.subscribe(['facebook_comments'])

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(comment):
    vs = analyzer.polarity_scores(comment)
    return 'positive' if vs['compound'] >= 0.05 else 'negative' if vs['compound'] <= -0.05 else 'neutral'


while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    comment = msg.value().decode('utf-8')
    sentiment = analyze_sentiment(comment)
    print(f"Comment: {comment} | Sentiment: {sentiment}")

consumer.close()