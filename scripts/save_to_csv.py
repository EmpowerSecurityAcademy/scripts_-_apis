import pymongo
import sys
import json
sys.path.append('../')
from import_config import load_config
from pymongo import MongoClient
import unicodecsv

config = load_config()

client = MongoClient(config["database"]["connection_url"])

db = client[config['database']['database_name']]
conn = db[config['database']['collection_name']]


def write_tweets_to_csv():

	cursor = conn.find()
	file = unicodecsv.writer(open("../tmp/data.csv", "wb"))
	file.writerow(["german_translation"])

	for tweet in cursor:
		print(tweet["german_translation"])
		file.writerow([tweet["german_translation"]])


if __name__ == '__main__':
	write_tweets_to_csv()