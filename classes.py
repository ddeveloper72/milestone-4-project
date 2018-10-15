# Load/import pre-requisites. Constucted using Python 3.7.0
import os
from flask import Flask, redirect, request, jsonify, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to external MongoDB database through URI variable hosted on app server. 
app.config["MONGO_DBNAME"] = 'mediacal_tm'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# MongoDb Collections
appointments_collection = mongo.db.appointment
facility_collection = mongo.db.facility
departments_collection = mongo.db.departments
services_collection = mongo.db.serviceItem

class Search:
    def __init__(self, collection):
        self.collection = collection

    def find_all(self):
        return self.collection.find()

    def find_by_task_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

