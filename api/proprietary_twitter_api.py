import json
import pymongo
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

url_root = '/todo/api/v2.0/'

def format_json(element):
	converted = dumps(element)
	modified = json.loads(converted)
	new_task = {}
	new_task["id"] = str(modified["_id"]['$oid'])
	new_task["description"] = modified["description"]
	new_task["title"] = modified["title"]
	new_task["done"] = modified["done"]
	new_task["location"] = modified["location"]
	return new_task

@basic_api.route(url_root+'tasks', methods=['GET', 'POST', 'PUT'])
def do_tasks():
	if request.method == 'GET':
		data = basic_api.conn.find()
		response = []
		for element in data:
			response.append(format_json(element))
		return make_response(jsonify({'tasks':response}), 200)

	if request.method == 'POST':
		content = request.get_json(silent=True)
		result = basic_api.conn.insert_one(content)
		return jsonify({'id': str(result.inserted_id)})

	return make_response(jsonify({'status_code': 500}), 500)

# RESTFUL operations related to a specific task

@basic_api.route(url_root+'tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def do_task(task_id):
	if request.method == 'GET':
		data = basic_api.conn.find_one({"_id": ObjectId(task_id)})
		return make_response(jsonify({'task':format_json(data)}), 200)

	if request.method == 'PUT':
		content = request.get_json(silent=True)
		result = basic_api.conn.update_one(
			{"_id": ObjectId(task_id)},
			{"$set": {"title": content["title"], 
						"description": content["description"], 
						"done": content["done"]}}
		)
		data = basic_api.conn.find_one({"_id": ObjectId(task_id)})
		return make_response(jsonify({'task':format_json(data)}), 200)

	if request.method == 'DELETE':
		result = basic_api.conn.delete_one({"_id": task_id})
		return make_response(jsonify({'deleted_id': task_id}), 200)

	return make_response(jsonify({'status_code': 500}), 500)


if __name__ == '__main__':
    basic_api.run(debug=True, host='0.0.0.0', port=5002)