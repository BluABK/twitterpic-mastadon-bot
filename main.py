#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import twitter_client

with open("config.json", "r") as f:
    CONFIG = json.load(f)
    TWITTER_API_CONFIG = CONFIG["twitter_api"]
    TWITTER_CONFIG = CONFIG["twitter"]


if __name__ == "__main__":
    # Auth Twitter API
    twitter_api = twitter_client.auth_api(TWITTER_API_CONFIG["api_key"],
                                          TWITTER_API_CONFIG["api_key_secret"],
                                          TWITTER_API_CONFIG["access_token"],
                                          TWITTER_API_CONFIG["access_token_secret"])

    # Create an example examples/timeline.json to play with.
    twitter_client.create_timeline_json(twitter_api, TWITTER_CONFIG["users"][0])

    with open("examples/timeline.json", "r") as f:
        exampleTweets = json.load(f)

    # FIXME: DELETEME: Print an arbitrary tweet.
    # print(json.dumps(exampleTweets["tweets"][15], indent=4))

    print("Tweets with images:")
    image_tweets = twitter_client.filter_image_tweets(exampleTweets["tweets"])
    for tweet in image_tweets:
        print(tweet)
