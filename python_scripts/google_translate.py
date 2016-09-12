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


def translate_tweets():

	cursor = conn.find()

	for tweet in cursor:
		# r = requests.get('https://www.googleapis.com/language/translate/v2?key=' + config["google"]["credentials"] + "&source=en&target=es&q=" + tweet["text"])
		# converted = r.json()
		# tweet["spanish_translation"] = converted["data"]["translations"][0]["translatedText"]
		r = requests.get('https://www.googleapis.com/language/translate/v2?key=' + config["google"]["credentials"] + "&source=en&target=de&q=" + tweet["text"])
		converted = r.json()
		tweet["google_translation"] = converted["data"]["translations"][0]["translatedText"]
		tweet["translated"] = "true"
		conn.save(tweet)
		print(tweet)


{u'parts_of_speech': [[u'Great', u'JJ'], [u'article', u'NN'], [u'-', u':'], [u'&', u'CC'], [u'gt', u'NN'], [u';', u':'], [u'https', u'NN'], [u':', u':'], [u'//t.co/hYaAeWI66r', u'JJ'], [u'#', u'#'], [u'devsecops', u'NNS'], [u'#', u'#'], [u'cloudsecurity', u'NN']], u'text': u'Great article -&gt; https://t.co/hYaAeWI66r #devsecops #cloudsecurity', u'created_at': datetime.datetime(2016, 7, 3, 19, 51, 47), u'twitter_id': u'749692132789805059', u'processed_text': [u'Great', u'article', u'-', u'&', u'gt', u';', u'https', u':', u'//t.co/hYaAeWI66r', u'#', u'devsecops', u'#', u'cloudsecurity'], 'google_translation': u'Gro\xdfe Artikel -', u'processed': u'true', u'translated': 'true', u'_id': ObjectId('57b610f50be444a56bfd6ac3'), u'type': u'original', u'spanish_translation': u'Gran art\xedculo -'}

{u'parts_of_speech': [[u'@', u'NN'], [u'WhiteHouse', u'NNP'], [u'How', u'NNP'], [u'do', u'VBP'], [u'we', u'PRP'], [u'get', u'VB'], [u'involved', u'VBN'], [u'in', u'IN'], [u'the', u'DT'], [u'TechHire', u'NNP'], [u'initiative', u'NN'], [u'?', u'.'], [u'Thanks', u'NNS'], [u'!', u'.']], u'text': u'@WhiteHouse How do we get involved in the TechHire initiative?  Thanks!', u'created_at': datetime.datetime(2016, 8, 17, 18, 40, 28), u'twitter_id': u'765981637813346305', u'processed_text': [u'@', u'WhiteHouse', u'How', u'do', u'we', u'get', u'involved', u'in', u'the', u'TechHire', u'initiative', u'?', u'Thanks', u'!'], 'google_translation': u'@WhiteHouse Wie wir in der TechHire Initiative engagieren? Vielen Dank!', u'processed': u'true', u'translated': 'true', u'_id': ObjectId('57b610f30be444a56bfd6aaa'), u'type': u'original', u'spanish_translation': u'@WhiteHouse \xbfC\xf3mo nos involucramos en la iniciativa TechHire? \xa1Gracias!'}


if __name__ == '__main__':
	translate_tweets()