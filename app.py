# Load/import pre-requisites. Constucted using Python 3.7.0
import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from classes import Search

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



# Basebuild function
# Search for scheduled appointments - no filters.
@app.route('/')
@app.route('/get_appointment')
def get_appointment():
    appointment = Search(appointments_collection).find_all()
    return render_template("appointment.html",
                            appointment = appointment)

# Basebuild function

@app.route('/add_appointment', methods=["POST", "GET"])
def add_appointment():
    
    facility = Search(facility_collection).find_all()
    depts = Search(departments_collection).find_all()

    return render_template("add_appointment.html", facility = facility, depts = depts)

@app.route('/services',  methods=["POST"])
def services():
    depts = Search(departments_collection).find_all()
    print(depts)

    data = request.form['ref']
    print(data)
    
    for dept in depts:
        if dept['ref'] == data:
            services = dept['services']
            print(services) 
                    
    if services:
        return jsonify({"data": services})
    print(services) 

    return jsonify({"error" : "an error occured"})

    

# Basebuild function
# Adds a new appointment
@app.route('/insert_appointment',  methods=["POST", "GET"])
def insert_appointment():
    appointment = appointments_collection
    appointment.insert_one(request.form.to_dict())
    return redirect(url_for('get_appointment'))

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/edit_appointment/<task_id>')
def edit_appointment(task_id):
    _appointment = Search(appointments_collection).find_by_task_id(task_id)
    all_departments = Search(departments_collection).find_all()
    all_serviceItem = Search(services_collection).find_all()
    return render_template('edit_appointment.html', 
                            appointment=_appointment, departments=all_departments, services=all_serviceItem)

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/update_appointment/<task_id>')
def update(task_id):
    appointment = appointments_collection
    appointment.update({'_id': ObjectId(task_id)},
    {
        'dept_name': request.form.get['dept_name'],
        'task_description': request.form.get['task_description'],
        'task_name': request.form.get['task_name'],
        'sched_date': request.form.get['sch_date'],
        'sched_time': request.form.get['sch_time'],
        'is_urgent': request.form.get['is_urgent']
    })
    return redirect(url_for('get_appointment'))

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/delete_appointment/<task_id>')
def delete_appointment(task_id):
    appointments_collection.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_appointment'))

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