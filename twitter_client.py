import json
import twitter

TWITTER_API = None
MEDIA_TYPES_AVAILABLE = ["photo", "video", "animated_gif"]
MEDIA_IMAGE_TYPES = ["photo", "video", "animated_gif"]


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
    has_images = False
    image_tweets = []

    for tweet in tweet_list:
        has_images = False
        if "extended_entities" in tweet:
            if "media" in tweet["extended_entities"]:
                for media in tweet["extended_entities"]["media"]:
                    if "type" in media:
                        if media["type"] in MEDIA_IMAGE_TYPES:
                            # print("Tweet {tid} has images: {imgs}".format(tid=tweet["id_str"], imgs=media["media_url_https"]))
                            has_images = True
        if has_images:
            image_tweets.append(tweet)

    return image_tweets


def get_image_urls_from_tweet(tweet: dict):
    image_urls = []
    if "extended_entities" in tweet:
        if "media" in tweet["extended_entities"]:
            for media in tweet["extended_entities"]["media"]:
                if media["type"] in MEDIA_IMAGE_TYPES:
                    image_url = media["media_url_https"]
                    if image_url not in image_urls:
                        # print("Appending tweet with url: {url}".format(url=image_url))
                        image_urls.append(media["media_url_https"])

    return image_urls
