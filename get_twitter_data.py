from requests_oauthlib import OAuth1
from twitter_api.twitter_api import get_recent_tweets
import secret_settings as ss
import csv

auth = OAuth1(ss.TWITTER_PUBLIC_CONSUMER_KEY, ss.TWITTER_SECRET_CONSUMER_KEY, ss.TWTTER_PUBLIC_ACCESS_TOKEN, ss.TWTTER_SECRET_ACCESS_TOKEN)

query = '#bitcoin'

tweet_count = 0
with open('./data/twitter_text.csv', 'w') as csv_file:
    dict_writer = csv.DictWriter(csv_file, ('created_at', 'user_name', 'followers_count', 'text'))
    dict_writer.writeheader()
    for tweet_batch in get_recent_tweets(auth, query, max_count=1000, language='en'):
        for status in tweet_batch['statuses']:
            dict_writer.writerow({
                'created_at': status['created_at'],
                'user_name': status['user']['created_at'],
                'text': status['text'],
                'followers_count': status['user']['followers_count']
            })
            tweet_count += 1
print('Number of tweets: {}'.format(tweet_count))
