import unittest
import app
from import_config import load_config
import json 
from pymongo import MongoClient

config = load_config()

client = MongoClient(config['test_database']["connection_url"])
db = client[config['test_database']['database_name']]
app.basic_api.conn = db[config['test_database']['collection_name']]

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'done': False
    }
]

class AppTestCases(unittest.TestCase):

    def setUp(self):
        app.basic_api.conn.remove()
        app.basic_api.conn.insert_one(tasks[0])
        app.basic_api.conn.insert_one(tasks[1])
        self.test_app = app.basic_api.test_client()

    def test_get_tasks(self):
        response = self.test_app.get('/todo/api/v2.0/tasks')
        data = json.loads(response.data)
        self.assertEqual(data['tasks'][0]['title'], 'Buy groceries')

    def test_post_tasks(self):
        response = self.test_app.post('/todo/api/v2.0/tasks', 
                       data=json.dumps(dict(title='Eat a sandwich', description='Enjoy it a lot', done=0)),
                       content_type = 'application/json')
        data = json.loads(response.data) 
        self.assertGreater(len(data['id']), 0)

    def test_get_task(self):
        response = self.test_app.get('/todo/api/v2.0/tasks')
        data1 = json.loads(response.data)
        response = self.test_app.get('/todo/api/v2.0/tasks/'+ data1['tasks'][0]['id'])
        data = json.loads(response.data)
        self.assertEqual(data['task'], {
                                            'id': data1['tasks'][0]['id'],
                                            'title': 'Buy groceries',
                                            'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
                                            'done': False
                                        })

    def test_put_task(self):
        response = self.test_app.get('/todo/api/v2.0/tasks')
        data1 = json.loads(response.data)
        response = self.test_app.put('/todo/api/v2.0/tasks/'+data1['tasks'][0]['id'], 
                       data=json.dumps(dict(title='Order from Instacart', description='Milk, Cheese, Pizza, Fruit, Tylenol, Burrito', done=0)),
                       content_type = 'application/json')
        data = json.loads(response.data)
        self.assertEqual(data['task'], {
                                            'id': data1['tasks'][0]['id'],
                                            'title': 'Order from Instacart',
                                            'description': 'Milk, Cheese, Pizza, Fruit, Tylenol, Burrito',
                                            'done': False
                                        })

    def test_delete_task(self):
        response = self.test_app.post('/todo/api/v2.0/tasks', 
                       data=json.dumps(dict(title='Eat a sandwich', description='Enjoy it a lot', done=0)),
                       content_type = 'application/json')
        data1 = json.loads(response.data) 
        response = self.test_app.delete('/todo/api/v2.0/tasks/'+data1['id'])
        data = json.loads(response.data)
        self.assertEqual(data['deleted_id'], data1['id'])

if __name__ == '__main__':
    unittest.main()