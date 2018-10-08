# Load/import pre-requisites. Constucted using Python 3.7.0
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

# Connect to external MongoDB database through URI variable hosted on app server. 
app.config["MONGO_DBNAME"] = 'mediacal_tm'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# Basebuild function
# Search for scheduled appointments - no filters.
@app.route('/')
@app.route('/get_departmemts')
def get_departments():
    return render_template("departments.html",
                            appointment = mongo.db.appointment.find())


if __name__ == '__main__':
    
    # assign a port ID works with Vscode
   
    app.run(host=os.getenv('IP'),
        port=os.getenv('PORT'),
        # debug set to true to help during development
        debug=True)

""" if __name__ == '__main__':

    # Cloud 9 Environmental variables

    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    # debug set to true to help during development
    debug=True) """