import json
import uuid
import gridfs
import datetime
import requests
import bson.binary
import pandas as pd
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify 
from flask_cors import CORS
from text_extraction import extract_information, encode_image

app = Flask(__name__)
cors = CORS(app)
mongo_client = MongoClient('localhost', 27017)
 
@app.route('/add-record', methods=["POST"])
def add_record():  
    response = request.files
    image_path = response["image"]
    file_content = image_path.read()
    file_content = bson.binary.Binary(file_content)
    base64_image = encode_image(file_content)
    prompt = ("Analyze the image and make two dictionary of key-value pairs of the information present in the image. "
              "The first dictionary should have all the main attributes in large/bold font. "
              "Second dictionary should have the secondary attributes represented in small font. "
              " The output should be in json format of { 'primary' :{'key1':'value1',. . }, 'secondary' :['key1':'value1',. . ]}.")
    attributes = extract_information(base64_image, prompt)
    response["attributes"] = attributes
    
    record_id = uuid.uuid4()
    response["record_id"] = record_id
    db = mongo_client["inventory_db"]
    fs = gridfs.GridFS(db)
    # with open(image_path, 'rb') as image_file:
    encoded_image = bson.binary.Binary(image_path.read())
    response["image"] = encoded_image

    collection = db["records"]
    current_datetime = datetime.datetime.now()
    date_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    response["date_time"] = date_time_str
    insertion = collection.insert_one(response)

    return jsonify({'message': 'success'})

@app.route('/get-records', methods=["GET"])
def get_records():
    db = mongo_client["inventory_db"]
    collection = db["records"]
    records = list(collection.find({}, {'_id': False}))
    # records = {"response": "success"}
    return jsonify(records), 200, {"Content-Type": "application/json"}
 

@app.route('/get-specific-record', methods=["POST"])
def get_specific_record():
    record_id = request.json.get("record_id")  
    db = mongo_client["inventory_db"]
    collection = db["records"] 
    record = collection.find_one({"record_id": record_id})
    return jsonify(record)

@app.route('/add-records-from-file', methods=["POST"])
def add_records_from_file():
    file_path = request.json.get("file_path")
    db = mongo_client["inventory_db"]
    collection = db["records"]
    records = pd.read_csv(file_path).to_dict('records')
    insertion = collection.insert_many(records)
    return jsonify({'message': 'success'})

if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0', port=4500)