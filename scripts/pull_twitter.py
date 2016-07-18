import tweepy
import pymongo
from import_config import load_config
from pymongo import MongoClient

config = load_config()

client = MongoClient(config["database"]["connection_url"])

db = client[config['database']['database_name']]
basic_api.conn = db[config['database']['collection_name']]

def get_tweets():

	auth = tweepy.OAuthHandler(config["twitter"]["consumer_key"], config["database"]["consumer_secret"])
	auth.set_access_token(config["twitter"]["access_key"], config["twitter"]["access_secret"])
	api = tweepy.API(auth)

	new_tweets = api.user_timeline(screen_name = "empowersec", count=200)

	for tweet in new_tweets:
		print(tweet)

if __name__ == '__main__':
	get_tweets()
