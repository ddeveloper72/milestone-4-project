# Load/import pre-requisites. Constucted using Python 3.7.0
import os
import datetime
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import json

from classes import Search

app = Flask(__name__)

# Connect to external MongoDB database through URI variable hosted on app server. 
app.config['MONGO_DBNAME'] = 'mediacal_tm'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# MongoDb Collections
appointments_collection = mongo.db.appointment
facilities_collection = mongo.db.facility
departments_collection = mongo.db.departments
services_collection = mongo.db.serviceItem
dept_template_collection = mongo.db.dept_templates
site_template_collection = mongo.db.site_templates



# Basebuild function
# Search for scheduled appointments - no filters.
@app.route('/')
@app.route('/get_appointment')
def get_appointment():
    appointment = Search(appointments_collection).find_all()
    return render_template('appointment.html', page_title='Appointments',
                            appointment = appointment)

# Basebuild function

@app.route('/add_appointment', methods=['POST', 'GET'])
def add_appointment():
    
    facility = Search(facilities_collection).find_all()
    departments = Search(departments_collection).find_all()

    return render_template("add_appointment.html", facility = facility, departments = departments)

@app.route('/service',  methods=['POST', 'GET'])
def service():
    departments = departments_collection.find()
    print(departments)

    # data comes from cur_value in $('#department').change(function()
    data = request.form['dept_name']
    print(data)
    
    for dept in departments:
        if dept['dept_name'] == data:
            service = dept['service']
                       
    print(service) 

    #return data to                 
    if service:
        return jsonify({'data': service})
    print(service) 

    return jsonify({'error' : 'an error occured'})
    

# Basebuild function
# Adds a new appointment
@app.route('/insert_appointment',  methods=['POST', 'GET'])
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


@app.route('/service_update',  methods=['POST', 'GET'])
def service_update():
    services = departments_collection.find()
    print(services)

    # data comes from cur_value in $('#department').change(function()
    data = request.form['dept_name']
    print(data)
    
    for dept in services:
        if dept['dept_name'] == data:
            service = dept['service']
            print(service) 
    #return data to                 
    if service:
        return jsonify({'data': service})
    print(service) 

    return jsonify({'error' : 'an error occured'})


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
    return render_template('get_departments.html', page_title='All Departments',
                            departments = departments)



# Basebuild function
# Lets us edit the name of a specific department
@app.route('/department/<dept_id>')
def department(dept_id):
    return render_template('department.html',  page_title='Department',
                            department = departments_collection.find_one(
                                {'_id': ObjectId(dept_id)}))

# Basebuild function
# Lets us edit the name of a specific department
@app.route('/edit_department/<dept_id>')
def edit_department(dept_id):
    return render_template('edit_department.html',  page_title='Edit Department',
                            department = departments_collection.find_one(
                                {'_id': ObjectId(dept_id)}))

# Basebuild function
# The name of a specific department is written back to the document
@app.route('/update_department/<dept_id>', methods=['POST'])
def update_department(dept_id):
    departments_collection.update_many({'_id': ObjectId(dept_id)},
        {'$set': {
            'dept_name': request.form.get('dept_name'),
            'main_contact.$[].phone': request.form.get('phone1'),
            'main_contact.$[].email': request.form.get('email'),
            'site.$[].phone': request.form.get('phone2')
        }
        }) 
        
    return redirect(url_for('get_departments'))

# Basebuild function
# The sites and departments are rendered to html
@app.route('/add_department',  methods=['POST', 'GET'])
def add_department():
       
    items = dept_template_collection.find()    
    facility = site_template_collection.find()    
        
    return render_template('add_department.html', page_title='Add a Department', 
                        data = items, facility = facility)

# Basebuild function
# The services are matched to the department selected
@app.route('/dept_update',  methods=['POST', 'GET'])
def dept_update():
    services = dept_template_collection.find() 
    print(services)

    # data comes from cur_value in $('#department').change(function()
    data = request.form['dept_name']
    print(data)
    
    for dept in services:
        if dept['dept_name'] == data:
            service = dept['service']
            print(service) 
    #return data to                 
    if service:
        return jsonify({'data': service})
    print(service) 

    return jsonify({'error' : 'an error occured'})

# Basebuild function
# The services are matched to the department selected
@app.route('/deptimg_update',  methods=['POST', 'GET'])
def dept_imgupdate():
    image = dept_template_collection.find() 
    

    # data comes from cur_value in $('#department').change(function()
    data = request.form['dept_name']
    print(data)
    
    for dept in image:
        if dept['dept_name'] == data:
            image = dept['img_url']
            print(image) 
    #return data to                 
    if service:
        return jsonify({'data': image})
    print(image) 

    return jsonify({'error' : 'an error occured'})



# Basebuild function
# Insert new department into collection
@app.route('/insert_department', methods=['POST'])
def insert_department():
       
    department = departments_collection
    #try:
    department_doc = {
            'dept_name': request.form.get('dept_name'),
            'dept_info': 'Infomation about this department',
            'img_url': '',
            'main_contact': [
            {
              'phone': '',
              'email': ''
            },
            {
              'email': '',
              'phone': ''
            }
            ],
            'site': [{
                'location': request.form.get('site_name'),
                'phone': ''
            }],
            'service':  [
                 request.form.get('service')
            ]
            }
    
    department.insert_one(department_doc)
    #except:
        #print('Error adding department to collection')
       
    return redirect(url_for('get_departments'))




# Basebuild function
# The name of a specific department is written back to the document
@app.route('/update_service/<serv_id>', methods=['POST'])
def update_service(serv_id):
    services_collection.update_one({'_id': ObjectId(serv_id)},

        {'$set': {'service.$[].name': request.form.get('service')}})
        
       
    return redirect(url_for('get_departments'))
    


if __name__ == '__main__':
    
    # assign a port ID works with Vscode
   
    app.run(host=os.getenv('IP'),
        port=os.getenv('PORT'),
        # debug set to true to help during development
        debug=True)




''' if __name__ == '__main__':

    # Cloud 9 Environmental variables

    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    # debug set to true to help during development
    debug=True) '''