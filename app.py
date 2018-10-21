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
facilities_collection = mongo.db.facility
departments_collection = mongo.db.departments




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
    
    facility = Search(facilities_collection).find_all()
    departments = Search(departments_collection).find_all()
    
    return render_template("add_appointment.html", facility = facility, departments = departments)

@app.route('/service',  methods=["POST"])
def service():
    depts = Search(departments_collection).find_all()
    print(depts)

    # data comes from cur_value in $("#department").change(function()
    data = request.form['dept_name']
    print(data)
    
    for dept in depts:
        if dept['dept_name'] == data:
            services = dept['service']
            print(service) 
    #return data to                 
    if services:
        return jsonify({"data": service})
    print(service) 

    return jsonify({"error" : "an error occured"})

    

# Basebuild function
# Adds a new appointment
@app.route('/insert_appointment',  methods=["POST", "GET"])
def insert_appointment():
    appointment = mongo.db.appointment
    appointment.insert_one(request.form.to_dict())
    return redirect(url_for('get_appointment'))

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/edit_appointment/<task_id>')
def edit_appointment(task_id):
    _appointment = Search(appointments_collection).find_by_task_id(task_id)
    all_depts = Search(departments_collection).find_all()
    return render_template('edit_appointment.html', 
                            appointment=_appointment, departments=all_depts)

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/update_appointment/<task_id>')
def update(task_id):
    appointment = appointments_collection
    appointment.update({'_id': ObjectId(task_id)},
    {
        'dept_name': request.form.get['dept_name'],
        'service': request.form.get['service'],
        'task_description': request.form.get['task_description'],
        'task_name': request.form.get['task_name'],
        'date_time': request.form.get['datetimepicker1'],
        'emp_name': request.form.get['emp_name'],
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