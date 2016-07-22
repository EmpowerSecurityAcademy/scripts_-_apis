import pymongo
import sys
import json
sys.path.append('../')
from import_config import load_config
from pymongo import MongoClient
import nltk
import requests


config = load_config()

client = MongoClient(config["database"]["connection_url"])

db = client[config['database']['database_name']]
conn = db[config['database']['collection_name']]


def process_tweets():

	cursor = conn.find()

	for tweet in cursor:
		if "translated" not in tweet or tweet["translated"] == "false":
			r = requests.get('https://www.googleapis.com/language/translate/v2?key=' + config["google"]["credentials"] + "&source=en&target=de&q=" + tweet["text"])
			converted = r.json()
			tweet["german_translation"] = converted["data"]["translations"][0]["translatedText"]
			conn.save(tweet)



if __name__ == '__main__':
	process_tweets()