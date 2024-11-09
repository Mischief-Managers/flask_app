import json
import requests
from pymongo import MongoClient
from flask import Flask, render_template, request
app = Flask(__name__)

mongo_client = MongoClient('localhost', 27017)
 
@app.route('/add-record')
def add_record():  
    response = requests.json()
    mongo_client = mongo_client.flask_db
    db = mongo_client.records
    insertion = db.insert_one(response)

    return json.dumps({'message': 'success'}), 200, {'Content-Type': 'application/json'}

@app.route('/get-records')
def get_records():
    mongo_client = mongo_client.flask_db
    db = mongo_client.records
    records = db.find()
    return json.dumps(records), 200, {'Content-Type': 'application/json'}
 

@app.route('/get-specific-record')
def get_specific_record():
    record_id = request.json.get("record_id")  
    mongo_client = mongo_client.flask_db
    db = mongo_client.records
    record = db.find_one({"record_id": record_id})
    return json.dumps(record), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0', port=4500)