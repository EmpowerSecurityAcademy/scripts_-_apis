import pymongo
import sys
import json
sys.path.append('../')
from import_config import load_config
from pymongo import MongoClient
import nltk

config = load_config()

client = MongoClient(config["database"]["connection_url"])

db = client[config['database']['database_name']]
conn = db[config['database']['collection_name']]


def process_tweets():

	cursor = conn.find()

	for tweet in cursor:
		tweet["processed_text"] = nltk.word_tokenize(tweet["text"])
		tweet["parts_of_speech"] = nltk.pos_tag(tweet["processed_text"])
		tweet["processed"] = "true"
		print(tweet)



if __name__ == '__main__':
	process_tweets()