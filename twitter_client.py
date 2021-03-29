import json
import twitter

TWITTER_API = None


def auth_api(api_key: str, api_secret: str, token_key: str, token_secret: str):
    global TWITTER_API
    twitter_api = twitter.Api(consumer_key=api_key,
                              consumer_secret=api_secret,
                              access_token_key=token_key,
                              access_token_secret=token_secret)

    TWITTER_API = twitter_api

    return twitter_api


def get_tweets(api=None, screen_name=None):
    """
    Downloads all tweets from a given user.

    Uses twitter.Api.GetUserTimeline to retreive the last 3,200 tweets from a user.
    Twitter doesn't allow retreiving more tweets than this through the API, so we get
    as many as possible.
    """
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


def create_timeline_json(api, screen_name):
    print(screen_name)
    timeline = get_tweets(api=api, screen_name=screen_name)

    tweets = []
    for tweet in timeline:
        # print(type(tweet._json))
        tweets.append((tweet._json))

    dct = {"tweets": tweets}
    with open('examples/timeline.json', 'w+') as f:
        json.dump(dct, f)

def filter_image_tweets(tweet_list: list):
    image_tweets = []

    for tweet in tweet_list:
        if "entities" in tweet:
            if "media" in tweet["entities"]:
                image_tweets.append(tweet)

    return image_tweets
