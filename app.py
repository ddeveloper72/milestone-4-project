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
@app.route('/get_appointment')
def get_appointment():
    return render_template("appointment.html",
                            appointment = mongo.db.appointment.find())

# Basebuild function

@app.route('/add_appointment')
def add_appointment():
    return render_template("add_appointment.html",
                            facility = mongo.db.facility.find(),
                            departments = mongo.db.departments.find(),
                            serviceItem = mongo.db.serviceItem.find())

# Basebuild function
# Adds a new appointment
@app.route('/insert_appointment',  methods=["POST"])
def insert_appointment():
    appointment = mongo.db.appointment
    appointment.insert_one(request.form.to_dict())
    return redirect(url_for('get_appointment'))

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/edit_appointment/<task_id>')
def edit_appointment(task_id):
    _appointment = mongo.db.appointment.find_one({"_id": ObjectId(task_id)})
    all_departments = mongo.db.departments.find()
    all_serviceItem = mongo.db.serviceItem.find()
    return render_template('edit_appointment.html', 
                            appointment=_appointment, departments=all_departments, services=all_serviceItem)

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/update_appointment/<task_id>')
def update(task_id):
    appointment = mongo.db.appointment
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
    mongo.db.appointment.remove({'_id': ObjectId(task_id)})
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