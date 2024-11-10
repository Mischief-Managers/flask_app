import os
import random
import pandas as pd
from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)

db = mongo_client['inventory_db']

def insert_data(data):
    collection = db["image_coordinates"]
    collection.insert_one(data)

def get_data():
    collection = db["records"]
    cursor = list(collection.find({}, {'_id': 0, 'image': 0}))
    return cursor

def generate_coordinates(min_val=0, max_val=500):
    # Decide randomly whether x or y will be in the 0-100 range
    if random.random() < 0.5:
        # x will be in range 0-100
        x = random.uniform(25, 100)
        # y can be any value in the wider range, excluding 0-100
        possible_ranges = [(min_val, 0), (100, max_val)]
        range_choice = random.choice(possible_ranges)
        y = random.uniform(*range_choice)
    else:
        # y will be in range 0-100
        y = random.uniform(25, 100)
        # x can be any value in the wider range, excluding 0-100
        possible_ranges = [(min_val, 0), (100, max_val)]
        range_choice = random.choice(possible_ranges)
        x = random.uniform(*range_choice)
    
    return x, y

data_items = get_data()
for item in data_items:
    record_id = item['record_id']
    building = item.get('building', None)
    x, y = generate_coordinates()
    insert_data({'record_id': record_id, 'building': building, 'x': x, 'y': y})
    