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
@app.route('/get_appointments')
def get_appointments():
    return render_template("appointments.html",
                            appointment = mongo.db.appointment.find())

@app.route('/add_appointment')
def add_appointment():
    return render_template("add_appointment.html",
                            departments = mongo.db.departments.find())


@app.route('/insert_appointment',  methods=["POST"])
def insert_appointment():
    appointment = mongo.db.appointment
    appointment.insert_one(request.form.to_dict())
    return redirect(url_for('get_appointments'))


""" @app.route('/edit_appointment/<appointment_id>')
def edit_appointment(appointment_id):
    _appointment = mongo.db.appointment.find_one({'_id': ObjectId(appointment_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editappointment.html', 
                            appointment=_appointment, categories=all_categories) """

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