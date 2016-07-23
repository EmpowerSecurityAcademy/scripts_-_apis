import tweepy
import sys

sys.path.append('../')
from import_config import load_config

auth = tweepy.OAuthHandler(config["twitter"]["consumer_key"], config["twitter"]["consumer_secret"])
auth.set_access_token(config["twitter"]["access_key"], config["twitter"]["access_secret"])
api = tweepy.API(auth)

new_tweets = api.user_timeline(screen_name = "empowersec", count=200)

for tweet in new_tweets:
	extracted_data = {}
	extracted_data["twitter_id"] = tweet.id_str
	extracted_data["created_at"] = tweet.created_at
	extracted_data["text"] = tweet.text.encode("utf-8")
	print(extracted_data)
