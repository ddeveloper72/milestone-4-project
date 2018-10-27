# Load/import pre-requisites. Constucted using Python 3.7.0
import os
import datetime
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime

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

@app.route('/service',  methods=["POST", "GET"])
def service():
    departments = departments_collection.find()
    print(departments)

    # data comes from cur_value in $("#department").change(function()
    data = request.form['dept_name']
    print(data)
    
    for dept in departments:
        if dept['dept_name'] == data:
            service = dept['service']
            print(service) 
    #return data to                 
    if service:
        return jsonify({"data": service})
    print(service) 

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
@app.route('/edit_appointment/<app_id>')
def edit_appointment(app_id):    
    _appointment = appointments_collection.find_one({'_id': ObjectId(app_id)})
    all_depts = departments_collection.find()
    return render_template('edit_appointment.html', 
                            appointment=_appointment, departments=all_depts)


@app.route('/service_update',  methods=["POST", "GET"])
def service_update():
    departments = departments_collection.find()
    print(departments)

    # data comes from cur_value in $("#department").change(function()
    data = request.form['dept_name']
    print(data)
    
    for dept in departments:
        if dept['dept_name'] == data:
            service = dept['service']
            print(service) 
    #return data to                 
    if service:
        return jsonify({"data": service})
    print(service) 

    return jsonify({"error" : "an error occured"})


# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/update_appointment/<app_id>', methods=['POST'])
def update_appointment(app_id):
    appointments = appointments_collection
    appointments.update_many({'_id': ObjectId(app_id)},
    {'$set': {
        'dept_name': request.form.get('dept_name'),
        'service': request.form.get('service'),
        'task_description': request.form.get('task_description'),
        'task_name': request.form.get('task_name'),
        'date_time': request.form.get('date_time'),
        'emp_name': request.form.get('emp_name'),
        'is_urgent': request.form.get('is_urgent'),
        'is_archived': request.form.get('is_archived')
    }
        
    })
    return redirect(url_for('get_appointment'))

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/delete_appointment/<app_id>')
def delete_appointment(app_id):
    appointments_collection.remove({'_id': ObjectId(app_id)})
    return redirect(url_for('get_appointment'))


# Basebuild function
# Lets us return the names of all the departments
@app.route('/get_departments')
def get_departments():
    departments = Search(departments_collection).find_all()
    return render_template("get_departments.html",
                            departments = departments)



# Basebuild function
# Lets us edit the name of a specific department
@app.route('/get_departments')
@app.route('/edit_department/<dept_id>')
def edit_department(dept_id):
    return render_template('edit_department.html', 
                            department = departments_collection.find_one(
                                {'_id': ObjectId(dept_id)}))


# Basebuild function
# The name of a specific department is written back to the document
@app.route('/update_department/<dept_id>', methods=['POST'])
def update_department(dept_id):
    departments_collection.update_one({'_id': ObjectId(dept_id)},
        {'$set': {'dept_name': request.form.get('dept_name')}}) 
        # NOT ['category_name'] is not subscriptable
    return redirect(url_for('get_departments'))

# Basebuild function
# The name of a specific department is written back to the document
@app.route('/update_service/<dept_id>', methods=['POST'])
def update_service(dept_id):
    departments_collection.update_one({'_id': ObjectId(dept_id)},
        {'$set': {'service': request.form.get('service')}}) 
        # NOT ['category_name'] is not subscriptable
    return redirect(url_for('get_departments'))


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