import requests
from pprint import pprint

BASE_URL = "https://api.twitter.com/1.1/search/tweets.json"
TWEET_URL = "https://api.twitter.com/1.1/statuses/show.json"


def get_recent_tweets_page(auth, query,
                           since_id=None, max_id=None, to_date=None,
                           count_per_page=100, language='en', result_type='recent',
                           tweet_mode='compat'):
    query_params = {'q': query, 'count': count_per_page, 'lang': language, 'result_type': result_type,
                    'tweet_mode': tweet_mode}

    if to_date:
        query_params['until'] = to_date

    if since_id or since_id == 0:
        query_params['since_id'] = since_id

    if max_id or max_id == 0:
        query_params['since_id'] = since_id

    return requests.get(BASE_URL, params=query_params, auth=auth)


def get_tweet_by_id(auth, id, tweet_mode='compat'):
    query_params = {'id': id, 'tweet_mode': tweet_mode}

    return requests.get(TWEET_URL, params=query_params, auth=auth)


def get_recent_tweets(auth, query, to_date=None, max_count=1000, language='en', result_type='recent', tweet_mode='compat'):
    n_tweets_processed = 0
    n_tweets_in_batch = 1

    while n_tweets_processed < max_count or n_tweets_in_batch == 0:
        if n_tweets_processed == 0:
            tweet_batch = get_recent_tweets_page(auth, query, to_date=to_date, count_per_page=100,
                                                 language=language, result_type=result_type,
                                                 tweet_mode=tweet_mode).json()
        else:
            tweet_batch = get_recent_tweets_page(auth, query, since_id=min_id, max_id=max_id - 1, to_date=to_date,
                                                 count_per_page=100, language=language, result_type=result_type,
                                                 tweet_mode=tweet_mode).json()
        if tweet_batch.get('errors', None):
            raise ValueError('API error: {}'.format(tweet_batch['errors']))
        all_ids = [tweet['id'] for tweet in tweet_batch['statuses']]
        max_id = max(all_ids)
        min_id = min(all_ids)
        n_tweets_in_batch = len(all_ids)
        n_tweets_processed += n_tweets_in_batch

        yield tweet_batch


if __name__ == '__main__':
    from requests_oauthlib import OAuth1
    import secret_settings as ss

    auth = OAuth1(ss.TWITTER_PUBLIC_CONSUMER_KEY, ss.TWITTER_SECRET_CONSUMER_KEY, ss.TWTTER_PUBLIC_ACCESS_TOKEN, ss.TWTTER_SECRET_ACCESS_TOKEN)

    query = 'bitcoin'
    tweet_mode = 'extended'
    text_key = 'full_text' if tweet_mode == 'extended' else 'text'
    followers_limit = 500

    for i, tweet_batch in enumerate(get_recent_tweets(auth, query, tweet_mode=tweet_mode)):
        for tweet in tweet_batch['statuses']:
            user = tweet['user']
            if not tweet.get('retweeted_status', None) \
                    and user.get('followers_count', 0) > followers_limit:
                print('{:30} {}'.format(user['screen_name'], tweet[text_key]))
                print('------------------------')
