# Load/import pre-requisites. Constucted using Python 3.7.0
from dotenv import load_dotenv
import os
from flask import Flask, redirect, request, jsonify, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# App Configuration                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
load_dotenv()

app = Flask(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Connect to external MongoDB database through URI variable hosted on app server.                          #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

client = MongoClient(os.getenv('MONGO_URI'), tlsCAFile=certifi.where())

db = client[(os.getenv('MONGO_DBNAME'))]


# MongoDb Collections
users_collection = db.users
appointments_collection = db.appointment
facilities_collection = db.facility
departments_collection = db.departments
services_collection = db.serviceItem
dept_template_collection = db.dept_templates
site_template_collection = db.site_templates
image_template_collection = db.image_templates

class Search:
    def __init__(self, collection):
        self.collection = collection

    def find_all(self):
        return self.collection.find()

    def find_one(self):
        return self.collection.find_one()

    def find_one_by_id(self, id):
        return self.collection.find_one_by_id({"_id": ObjectId(id)})
    
   
