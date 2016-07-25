import json
import pymongo
import sys
sys.path.append('../')
from import_config import load_config
from pymongo import MongoClient
from flask import Flask, jsonify, request, make_response, g
from bson.json_util import dumps
from bson.objectid import ObjectId

basic_api = Flask(__name__)

config = load_config()
client = MongoClient(config["database"]["connection_url"])

db = client[config['database']['database_name']]
basic_api.conn = db[config['database']['collection_name']]

url_root = '/tweets/api/v2.0/'

def format_json(element):
	converted = dumps(element)
	modified = json.loads(converted)
	new_task = {}
	new_task["id"] = str(modified["_id"]['$oid'])
	new_task["text"] = modified["text"]
	new_task["german_translation"] = modified["german_translation"]
	return new_task

@basic_api.route(url_root+'tweets', methods=['GET'])
def do_tasks():
	if request.method == 'GET':
		data = basic_api.conn.find()
		response = []
		for element in data:
			response.append(format_json(element))
		return make_response(jsonify({'tweets':response}), 200)

# RESTFUL operations related to a specific task

@basic_api.route(url_root+'tweets/<tweet_id>', methods=['GET'])
def do_task(task_id):
	if request.method == 'GET':
		data = basic_api.conn.find_one({"_id": ObjectId(task_id)})
		return make_response(jsonify({'tweet':format_json(data)}), 200)


	return make_response(jsonify({'status_code': 500}), 500)


if __name__ == '__main__':
    basic_api.run(debug=True, host='0.0.0.0', port=5002)