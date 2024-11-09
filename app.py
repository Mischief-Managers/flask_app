import os
import re
import json
import uuid
import gridfs
import base64
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

UPLOAD_FOLDER = 'uploads'
 
# @app.route('/add-record', methods=["POST"])
# def add_record():  
#     response = request.files
#     image_path = response["image"]
#     file_content = image_path.read()
#     file_content = bson.binary.Binary(file_content)
#     # base64_image = encode_image(file_content)
#     prompt = ("Analyze the image and make two dictionary of key-value pairs of the information present in the image. "
#               "The first dictionary should have all the main attributes in large/bold font. "
#               "Second dictionary should have the secondary attributes represented in small font. "
#               " The output should be in json format of { 'primary' :{'key1':'value1',. . }, 'secondary' :['key1':'value1',. . ]}.")
#     attributes = extract_information(file_content, prompt)
#     response["attributes"] = attributes
    
#     record_id = uuid.uuid4()
#     response["record_id"] = record_id
#     db = mongo_client["inventory_db"]
#     fs = gridfs.GridFS(db)
#     # with open(image_path, 'rb') as image_file:
#     encoded_image = bson.binary.Binary(image_path.read())
#     response["image"] = encoded_image

#     collection = db["records"]
#     current_datetime = datetime.datetime.now()
#     date_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
#     response["date_time"] = date_time_str
#     insertion = collection.insert_one(response)

#     return jsonify({'message': 'success'})

# def save_base64_image(base64_string, save_to_disk=True):
#     try:
#         # Extract the image format and base64 data
#         if ',' in base64_string:
#             format_header, base64_data = base64_string.split(',', 1)
#             # Extract image format (png, jpeg, etc.)
#             image_format = re.search(r'data:image/(\w+);base64', format_header).group(1)
#         else:
#             base64_data = base64_string
#             image_format = 'png'  # Default format if not specified
        
#         # Decode base64 data
#         image_data = base64.b64decode(base64_data)
        
#         # Generate unique filename
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f'image_{timestamp}.{image_format}'
        
#         # Save to disk if required
#         if save_to_disk:
#             file_path = os.path.join(UPLOAD_FOLDER, filename)
#             with open(file_path, 'wb') as f:
#                 f.write(image_data)
        
#         # Create document for MongoDB
#         image_document = {
#             'filename': filename,
#             'file_data': Binary(image_data),
#             'content_type': f'image/{image_format}',
#             'file_size': len(image_data),
#             'upload_date': datetime.now()
#         }
        
#         # Save to MongoDB
#         result = images_collection.insert_one(image_document)
        
#         return {
#             'success': True,
#             'file_id': str(result.inserted_id),
#             'filename': filename,
#             'size': len(image_data)
#         }
        
#     except Exception as e:
#         return {
#             'success': False,
#             'error': str(e)
#         }

@app.route("/add-record", methods=["POST"])
def add_record():
    data = request.get_json()
    with open("payload.json", "w") as f:
        json.dump(data, f)
        
    if not data or 'image' not in data:
        return jsonify({
            'error': 'No image data provided'
        }), 400
    
    base64_string = data['image']
    if "data:image/jpeg;base64," in base64_string:
        base64_string = base64_string.replace("data:image/jpeg;base64,", "")
    prompt = ("Analyze the image and make two dictionary of key-value pairs of the information present in the image. "
              "The first dictionary should have all the main attributes in large/bold font. "
              "Second dictionary should have the secondary attributes represented in small font. "
              " The output should be in json format of { 'primary' :{'key1':'value1',. . }, 'secondary' :['key1':'value1',. . ]}.")
    attributes = extract_information(base64_string, prompt)
    data["attributes"] = attributes
    
    record_id = str(uuid.uuid4())
    data["record_id"] = record_id
    db = mongo_client["inventory_db"]
    fs = gridfs.GridFS(db)
    data["image"] = base64_string

    collection = db["records"]
    current_datetime = datetime.datetime.now()
    date_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    data["date_time"] = date_time_str
    insertion = collection.insert_one(data)
    record = collection.find_one({"record_id": record_id}, {'_id': False, 'image': False})

    return jsonify({'message': 'success', "record": record})

@app.route('/update-record', methods={"POST"})
def update_record():
    db = mongo_client["inventory_db"]
    collection = db["records"]
    data = request.get_json()
    record_id = data["record_id"]
    previous_record = collection.find_one({"record_id": record_id})
    data["image"] = previous_record["image"]
    collection.delete_one({"record_id": record_id})
    insertion = collection.insert_one(data)
    record = collection.find_one({"record_id": record_id}, {'_id': False, 'image': False})

    return jsonify({'message': 'success', "record": record}), 200


@app.route('/get-records', methods=["GET"])
def get_records():
    db = mongo_client["inventory_db"]
    collection = db["records"]
    records = list(collection.find({}, {'_id': False, 'image': False}))
    # records = {"response": "success"}
    return jsonify(records), 200, {"Content-Type": "application/json"}
 

@app.route('/get-specific-record', methods=["POST"])
def get_specific_record():
    record_id = request.json.get("record_id")  
    db = mongo_client["inventory_db"]
    collection = db["records"] 
    record = collection.find_one({"record_id": record_id}, {'_id': False, "image": False})
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