#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Load/import pre-requisites. Constucted using Python 3.6.7                                                #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
import os
import datetime
from datetime import datetime
from flask import Flask, render_template, session, redirect, request, url_for, jsonify, flash, render_template_string
from flask_login import LoginManager, login_user, logout_user, current_user
from urllib.parse import urlparse, urljoin
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import json

from classes import Search

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Connect to external MongoDB database through URI variable hosted on app server.                          #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
app.config['MONGO_DBNAME'] = 'mediacal_tm'
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# MongoDb Collections                                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
users = mongo.db.users
appointments_collection = mongo.db.appointment
facilities_collection = mongo.db.facility
departments_collection = mongo.db.departments
services_collection = mongo.db.serviceItem
dept_template_collection = mongo.db.dept_templates
site_template_collection = mongo.db.site_templates
image_template_collection = mongo.db.image_templates


# Basebuild function
# Home page is appointment.html
@app.route('/')
@app.route('/index')
def appointment():
    if 'user' in session:
        login_user = users.find_one({'username' : session['user']})
        flash('You are logged in as ' + session['user'], 'bg-success') 
        return render_template('appointment.html', 
                                username=session['user'],
                                 user_id=login_user['_id'])
        
    return render_template('appointment.html', 
                            page_title='Appointments')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Log out, Login and registration views                                                                    #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Login required
""" def loginRequired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('To access this, please log in first', 'bg-warning')
            return redirect(url_for('login'))
    
    return wrap """

# Basebuild function
# Logout current user
@app.route('/logout')
def logout():    
    session.clear()
    flash('You are now logged out', 'bg-success') 
    return redirect(url_for('get_appointment'))


# Basebuild function
# Simple user authentication 
""" @app.route('/login', methods=['GET','POST'])
def login():
    session['next'] = request.args.get('next')
    return render_template('login.html') """

# Basebuild function
# Securely Redirect Back from Flask Snipets to ensure that all redirects 
# lead back to the same server- our own server.
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# Basebuild function
# Simple user authentication 
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    users = mongo.db.users

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            login_user = users.find_one({'username' : username})
        except:
            flash('Sorry there seems to be problem with the data', 'bg-warning')
            return redirect(url_for('get_appointment')) 

        if login_user:
            if check_password_hash(login_user['password'], password):
                session['user'] = username
                session['logged_in'] = True

                if 'next' in session:
                    next = session['next']

                    if is_safe_url(next):
                        redirect(next)

                flash('%s has successfully logged in' % request.form['username'], 'bg-success')
                return redirect(url_for('get_appointment', user_id=login_user['_id']))

            flash(u'Invalid username/password combination', 'bg-warning')
            return render_template('login.html', 
                                    page_title='Log-in', 
                                    error=error)  
        
    
    return render_template('login.html', 
                            page_title='Log-in', 
                            error=error)
    
   

# Basebuild function
# Simple user registration - With no password as per project brief.
@app.route('/register', methods=['POST', 'GET'])

def register():
    error = None
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username' : request.form['username']})
        created = datetime.utcnow()

        try:
            if login_user is None:
                hashed_pass = generate_password_hash(request.form['pass'])
                users.insert_one(
                    {'username' : request.form['username'], 
                    'password' : hashed_pass,
                    'site': [],
                    'department' : [],
                    'favorites' : [],
                    'created': created})
            
                login_user = users.find_one(
                    {'username': request.form['username']})

                session['user'] = request.form['username']  
                session['logged_in'] = True
                
                flash('%s has successfully logged in' % request.form['username'], 'bg-success')
                return redirect(url_for('get_appointment', 
                                        user_id=login_user['_id']))

        except DuplicateKeyError:
            flash(u'That username already exists!', 'bg-warning') 

    return render_template('registration.html', 
                            page_title='Register', 
                            error=error)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Appointments views                                                                                       #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Basebuild function
# Search for scheduled appointments - no filters.
# , defaults={'user_id': None}
@app.route('/get_appointment', defaults={'user_id': None})
@app.route('/get_appointment/<user_id>')
def get_appointment(user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']})
        appointment = Search(appointments_collection).find_all()
    
        return render_template('appointment.html', 
                                page_title='Appointments',
                                appointment = appointment,
                                username=session['user'], 
                                user_id=login_user['_id'])
    else:
        appointment = Search(appointments_collection).find_all()

    return render_template('appointment.html', 
                            page_title='Appointments',
                            appointment = appointment)

    

@app.route('/add_appointment', defaults={'user_id': None})
@app.route('/add_appointment/<user_id>')
def add_appointment(user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']})
        facility = Search(facilities_collection).find_all()
        departments = Search(departments_collection).find_all()

        return render_template("add_appointment.html", 
                                page_title='Add Appointments',
                                facility = facility, 
                                departments = departments, 
                                username=session['user'], 
                                user_id=login_user['_id'])
    else:
        facility = Search(facilities_collection).find_all()
        departments = Search(departments_collection).find_all()

    return render_template("add_appointment.html", 
                                page_title='Add Appointments',
                                facility = facility, 
                                departments = departments)

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
@app.route('/insert_appointment', methods=['POST', 'GET'], defaults={'user_id': None})
@app.route('/insert_appointment/<user_id>')
def insert_appointment(user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']})
        appointment = appointments_collection
        appointment.insert_one(request.form.to_dict())
        return redirect(url_for('get_appointment',
                        username=session['user'], 
                        user_id=login_user['_id']))

    return render_template('login.html', page_title='Log-in')

# Basebuild function
# Lets us edit the data for an existing appointment
@app.route('/edit_appointment', defaults={'user_id': None})
@app.route('/edit_appointment/<app_id>/<user_id>')
def edit_appointment(app_id, user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']})   
        _appointment = appointments_collection.find_one({'_id': ObjectId(app_id)})
        all_depts = departments_collection.find()
        return render_template('edit_appointment.html', 
                                appointment=_appointment, 
                                departments=all_depts, 
                                username=session['user'], 
                                user_id=login_user['_id'])
    else:
        flash('To access this information, please login')
        return redirect(url_for('get_appointment'))

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
@app.route('/delete_appointment/<app_id>/<user_id>')
def delete_appointment(app_id, user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']})      
        appointments_collection.remove({'_id': ObjectId(app_id)})
        return redirect(url_for('get_appointment', 
                        username=session['user'], 
                        user_id=login_user['_id']))

    return render_template('login.html', page_title='Log-in')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Departments views                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Basebuild function
# Lets us return the names of all the departments
@app.route('/get_departments', defaults={'user_id': None})
@app.route('/get_departments/<user_id>')
def get_departments(user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']}) 
        departments = Search(departments_collection).find_all()
        return render_template('get_departments.html', 
                                page_title='All Departments',
                                departments = departments, 
                                username=session['user'], 
                                user_id=login_user['_id'])
    
    return render_template('login.html', page_title='Log-in')



# Basebuild function
# Lets us edit the name of a specific department
@app.route('/department/<dept_id>/<user_id>')
def department(dept_id, user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']}) 
        return render_template('department.html',  
                                page_title='Department',
                                department = departments_collection.find_one(
                                {'_id': ObjectId(dept_id)}), 
                                username=session['user'], 
                                user_id=login_user['_id'])

    return render_template('login.html', page_title='Log-in')

# Basebuild function
# Lets us edit the name of a specific department
@app.route('/edit_department/<dept_id>/<user_id>')
def edit_department(dept_id, user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']}) 
        return render_template('edit_department.html',  
                                page_title='Edit Department',
                                department = departments_collection.find_one(
                                {'_id': ObjectId(dept_id)}), 
                                username=session['user'], 
                                user_id=login_user['_id'])

    return render_template('login.html', page_title='Log-in')

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
@app.route('/add_department',  methods=['POST', 'GET'], defaults={'user_id': None})
@app.route('/add_department/<user_id>')
def add_department(user_id):
    if 'user' in session: 
        login_user = users.find_one({"username": session['user']})  
        items = dept_template_collection.find()    
        facility = site_template_collection.find()        
        
        return render_template('add_department.html', 
                                page_title='Add a Department', 
                                data = items, facility = facility, 
                                username=session['user'], 
                                user_id=login_user['_id'])

    return render_template('login.html', page_title='Log-in')
   

# Basebuild function
# The services are matched to the department selected
@app.route('/dept_update',  methods=['POST', 'GET'])
def dept_update():
    services = dept_template_collection.find()    

    site = request.form.get('site_name')
    print(site)

    """ existing_dept = departments_collection.find({'_id': 1, 'dept_name': request.form['dept_name'], 'site': {request.form.get('site_name')} })
    print(existing_dept) """


    # data comes from cur_value in $('#department').change(function()
    data = request.form['dept_name']
    print(data, site)
    for dept in services:
        if dept['dept_name'] == data:
            service = dept['service']
          # print(service) 
    #return data to                 
    if service:
        return jsonify({'data': service})
    # print(service) 
    return jsonify({'error' : 'an error occured'})
    

# Basebuild function
# The services are matched to the department selected
@app.route('/deptimg_update',  methods=['POST', 'GET'])
def dept_imgupdate():
    image = dept_template_collection.find() 
    

    # data comes from cur_value in $('#department').change(function()
    data = request.form['dept_name']
    #print(data)
    
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
@app.route('/insert_department/<user_id>', methods=['POST'])
def insert_department(user_id):
     if 'user' in session: 
        login_user = users.find_one({"username": session['user']})   
        department = departments_collection
        #try:
        department_doc = {
                'dept_name': request.form.get('dept_name'),
                'dept_info': request.form.get('dept_info'),
                'img_url': request.form.get('img_url'),
                'main_contact': [
                {
                  'phone': request.form.get('phone'),
                  'email': request.form.get('email')
                }
                ],
                'site': [{
                    'location': request.form.get('site_name'),
                    'phone': request.form.get('phone1')
                }],
                'service':  request.form.getlist('service'),
                }

        department.insert_one(department_doc)
        #except:
            #print('Error adding department to collection')

        return redirect(url_for('get_departments',
                                username=session['user'], 
                                user_id=login_user['_id']))


# Basebuild function
# The name of a specific department is written back to the document
@app.route('/update_service/<serv_id>', methods=['POST'])
def update_service(serv_id):
    services_collection.update_one({'_id': ObjectId(serv_id)},

        {'$set': {'service.$[].name': request.form.get('service')}})
        
       
    return redirect(url_for('get_departments'))
    
# Basebuild function
# Lets us delete an existing department
@app.route('/delete_department/<dept_id>/<user_id>')
def delete_department(dept_id, user_id):
    if 'user' in session:
        login_user = users.find_one({"username": session['user']})      
        departments_collection.remove({'_id': ObjectId(dept_id)})
        return redirect(url_for('get_departments', 
                        username=session['user'], 
                        user_id=login_user['_id']))

    return render_template('login.html', page_title='Log-in')

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