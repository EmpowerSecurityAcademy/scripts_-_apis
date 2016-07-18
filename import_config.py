
import json

def load_config():
	with open('config.json') as json_data:
		config = json.load(json_data)
		return config