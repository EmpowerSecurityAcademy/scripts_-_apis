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

def do_anything():
	all_db = conn.find()

	for tweet in all_db:
		print(tweet["twitter_id"])
		print(tweet["text"])



def print_bill():
	print("bill")

if __name__ == '__main__':
	print_bill()
	do_anything()