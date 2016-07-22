import tweepy
import pymongo
import sys
import json
sys.path.append('../')
from import_config import load_config
from pymongo import MongoClient

config = load_config()

client = MongoClient(config["database"]["connection_url"])

db = client[config['database']['database_name']]
conn = db[config['database']['collection_name']]

def get_tweets():

	auth = tweepy.OAuthHandler(config["twitter"]["consumer_key"], config["twitter"]["consumer_secret"])
	auth.set_access_token(config["twitter"]["access_key"], config["twitter"]["access_secret"])
	api = tweepy.API(auth)

	new_tweets = api.user_timeline(screen_name = "empowersec", count=200)

	for tweet in new_tweets:
		extracted_data = {}
		extracted_data["type"] = "original"
		extracted_data["processed"] = "false"
		extracted_data["translated"] = "false"
		extracted_data["twitter_id"] = tweet.id_str
		extracted_data["created_at"] = tweet.created_at
		extracted_data["text"] = tweet.text.encode("utf-8")
		conn.insert_one(extracted_data)
		print(extracted_data)

if __name__ == '__main__':
	get_tweets()
