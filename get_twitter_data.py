from requests_oauthlib import OAuth1
from twitter_api.twitter_api import get_recent_tweets
import secret_settings as ss
import traceback
import csv

auth = OAuth1(ss.TWITTER_PUBLIC_CONSUMER_KEY, ss.TWITTER_SECRET_CONSUMER_KEY, ss.TWTTER_PUBLIC_ACCESS_TOKEN, ss.TWTTER_SECRET_ACCESS_TOKEN)

query = '#bitcoin'

tweet_count = 0
with open('./data/twitter_text.csv', 'w', encoding='utf-8') as csv_file:
    dict_writer = csv.DictWriter(csv_file,
                                 fieldnames=('created_at', 'user_name', 'followers_count', 'text'),
                                 quoting=csv.QUOTE_NONNUMERIC)
    dict_writer.writeheader()

    tweet_mode = 'extended'
    followers_limit = 500
    text_key = 'full_text' if tweet_mode == 'extended' else 'text'

    try:
        for tweet_batch in get_recent_tweets(auth, query, max_count=6000, language='en', tweet_mode=tweet_mode):
                for tweet in tweet_batch['statuses']:
                    user = tweet['user']
                    if not tweet.get('retweeted_status', None) \
                            and user.get('followers_count', 0) > followers_limit:

                        dict_writer.writerow({
                            'created_at': tweet['created_at'],
                            'user_name': tweet['user']['screen_name'],
                            'text': tweet[text_key],
                            'followers_count': user['followers_count']
                        })
                        tweet_count += 1
    except Exception as e:
        traceback.print_exc()
print('Number of tweets: {}'.format(tweet_count))
