import requests
from requests_oauthlib import OAuth1

BASE_URL = "https://api.twitter.com/1.1/search/tweets.json?"


def get_recent_tweets(query,
                      public_consummer_key, secret_consummer_key,
                      public_access_token, secret_access_token,
                      since_id=None, max_id=None,
                      count=100):

    query_params = {'q': query, 'count': count}
    auth = OAuth1(public_consummer_key, secret_consummer_key, public_access_token, secret_access_token)

    if since_id or since_id == 0:
        query_params['since_id'] = since_id

    if max_id or max_id == 0:
        query_params['since_id'] = since_id

    return requests.get(BASE_URL, params=query_params, auth=auth)


if __name__ == '__main__':
    import secret_settings as ss
    from pprint import pprint
    query = '#bitcoin'
    tweets = get_recent_tweets(query,
                               public_consummer_key=ss.TWITTER_PUBLIC_CONSUMER_KEY,
                               secret_consummer_key=ss.TWITTER_SECRET_CONSUMER_KEY,
                               public_access_token=ss.TWTTER_PUBLIC_ACCESS_TOKEN,
                               secret_access_token=ss.TWTTER_SECRET_ACCESS_TOKEN)
    statuses = tweets.json()['statuses']
    print('Number of tweets: {}'.format(len(statuses)))
    for status in statuses:
        print(status['user']['name'])
        print(status['user']['followers_count'])
        print(status['text'])
