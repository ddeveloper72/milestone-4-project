#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Load/import pre-requisites. Constructed using Python 3.6.7                                                #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
import os
import datetime
from datetime import datetime
from time import gmtime, strftime
from flask import Flask, render_template, session, redirect, request, url_for, jsonify, flash, render_template_string
from flask_login import LoginManager, login_user, logout_user, current_user
from urllib.parse import urlparse, urljoin
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
import operator
from functools import wraps, reduce
import json

# import environmental variables from external env.py
if os.path.exists('env.py'):
    import env

from classes import Search

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Connect to external MongoDB database through URI variable hosted on app server.                          #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
app.config['MONGO_DBNAME'] = 'mediacal_tm'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# MongoDb Collections                                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
users_collection = mongo.db.users
appointments_collection = mongo.db.appointment
facilities_collection = mongo.db.facility
departments_collection = mongo.db.departments
services_collection = mongo.db.serviceItem
dept_template_collection = mongo.db.dept_templates
site_template_collection = mongo.db.site_templates
image_template_collection = mongo.db.image_templates



@app.route('/')
def appointment():
    """
    Home page is appointment.html
    """

    if 'user' in session:
        login_user = users_collection.find_one({'username' : session['user']})
        flash('You are logged in as ' + session['user'], 'alert-success') 
        return redirect(url_for('get_appointment', 
                                username=session['user'],
                                 user_id=login_user['_id']))
        
    return redirect(url_for('get_appointment'))




@app.route('/logout')
def logout(): 
    """
    Log the user out
    """

    session.clear()
    flash('You are now logged out', 'alert-success') 
    return redirect(url_for('get_appointment'))



def is_safe_url(target):
    """ 
    Securely Redirect Back from Flask Snippets to ensure that all redirects 
    lead back to the same server- our own server.
    """

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc




@app.route('/login', methods=['GET','POST'])
def login():
    """
    Simple user authentication 
    """
    error = None
    users = users_collection

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            login_user = users.find_one({'username' : username})
        except:
            flash('Sorry there seems to be problem with the data', 'alert-warning')
            return redirect(url_for('get_appointment')) 

        if login_user:
            if check_password_hash(login_user['password'], password):
                session['user'] = username
                session['logged_in'] = True

                if 'next' in session:
                    next = session['next']

                    if is_safe_url(next):
                        redirect(next)

                flash('%s has successfully logged in' % request.form['username'], 'alert-success')
                return redirect(url_for('get_appointment', user_id=login_user['_id']))

        flash(u'Invalid username/password combination', 'alert-warning')
        return render_template('login.html', 
                                    page_title='Login', 
                                    error=error)  
        
    
    return render_template('login.html', 
                            page_title='Log-in', 
                            error=error)
    
   



@app.route('/register', methods=['POST', 'GET'])
def register():
    """ 
    Simple user registration.
    """

    error = None
    if request.method == 'POST':
        users = users_collection
        login_user = users.find_one({'username' : request.form['username']})
        created = datetime.utcnow()

        try:
            if login_user is None:
                hashed_pass = generate_password_hash(request.form['pass'])
                users.insert_one(
                    {'username' : request.form['username'], 
                    'password' : hashed_pass,
                    'favourites' : [
                        'You have no favourites selected yet'
                        ],
                    'created': created})
            
                login_user = users.find_one(
                    {'username': request.form['username']})

                session['user'] = request.form['username']  
                session['logged_in'] = True
                
                flash('%s has successfully logged in' % request.form['username'], 'alert-success')
                return redirect(url_for('get_appointment', 
                                        user_id=login_user['_id']))

            flash('That username already exists!', 'alert-warning')

        except DuplicateKeyError:
            flash('That username already exists!', 'alert-warning')

    return render_template('registration.html', 
                            page_title='Register', 
                            error=error)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# User Profile Views                                                                                       #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


@app.route ('/profile/<user_id>', methods=['POST', 'GET'])
def profile(user_id):
    """ 
    Show profile page, check for likes by the user and display them.
    """

    if 'user' in session:
        login_user = users_collection.find_one({'username': session['user']})
        departments = Search(departments_collection).find_all()
        facility = Search(facilities_collection).find_all()    

        try:
            id_deptlikes = users_collection.find({'username': session['user']})
            
            list_deptlikes = []
            likes =  [i['likes'] for i in id_deptlikes]

            for like in likes[0]:
                list_deptlikes.append({"_id": ObjectId(like)})            
            
            favourites = [i for i in departments_collection.find( { "$or": list_deptlikes})] 


        except:
            flash('There are no favourites in your profile yet, %s' %
                  session['user'], 'alert-warning')
        
        else:
            return render_template('profile.html', 
                                    page_title = "Profile Page",
                                    login_user = login_user, 
                                    user_id = login_user['_id'],
                                    favourites = favourites,
                                    facility = facility,
                                    departments = departments)

    return render_template('profile.html',      
                            page_title='Profile', 
                            login_user = login_user,
                            user_id = user_id,
                            facility = facility,
                            departments = departments)



@app.route ('/update_profile/<user_id>', methods=['POST'])
def update_profile(user_id):
    """ 
    Update profile db
    """
    
    users_collection.update_many({'_id': ObjectId(user_id)},
    {'$set': {
            'likes': request.form.getlist('favourites'),
            'user_contact': [
                {
              'phone': request.form.get('phone'),
              'email': request.form.get('email')
                }
            ],
            'site_name': request.form.get('site_name'),
            'dept_name': request.form.get('dept_name'),
            }
    })
    flash('Your profile has been updated %s' %
                  session['user'], 'alert-success')
    return redirect(request.referrer)



@app.route('/add_favourite/<dept_id>/<user_id>', methods=['POST','GET'])
def add_favourite(dept_id, user_id):
    """ 
    Create a favourite/like and add to the user profile db
    """

    try:
        login_user = users_collection.find_one({'_id': ObjectId(user_id)})
    except:
        flash('There was an error retrieving the data from the database', 'alert-danger')
        return redirect(request.referrer)
    if dept_id in login_user["favourites"]:
        flash('This department is already in your favourites', 'alert-warning')
        return redirect(request.referrer)
    else: 
        
        departments_collection.find_one({'_id': ObjectId(dept_id)}) 
        users_collection.update({'_id': ObjectId(user_id)},
        {'$push': 
        {'likes': dept_id}
        
        })

        flash('This department has been added as a favourite', 'alert-success')
        return redirect(request.referrer)    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Appointments views                                                                                       #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

@app.route('/get_appointment', defaults={'user_id': None})
@app.route('/get_appointment/<user_id>')
def get_appointment(user_id):
    """ 
    Search for scheduled appointments - no filters.
    """

    if 'user' in session:
        login_user = users_collection.find_one({"username": session['user']})
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
        login_user = users_collection.find_one({"username": session['user']})
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
    
    """ 
    data comes from cur_value in $('#department').change(function()
    """

    data = request.form['dept_name']
        
    for dept in departments:
        if dept['dept_name'] == data:
            service = dept['service']
                       
                  
    if service:
        return jsonify({'data': service})
    

    return jsonify({'error' : 'an error occurred'})
    


@app.route('/insert_appointment', methods=['POST', 'GET'], defaults={'user_id': None})
@app.route('/insert_appointment/<user_id>')
def insert_appointment(user_id):
    """ 
    Adds a new appointment
    """

    if 'user' in session:
        login_user = users_collection.find_one({"username": session['user']})
        appointment = appointments_collection
        appointment.insert_one(request.form.to_dict())
        return redirect(url_for('get_appointment',
                        username=session['user'], 
                        user_id=login_user['_id']))

    return render_template('login.html', page_title='Log-in')


@app.route('/edit_appointment', defaults={'user_id': None})
@app.route('/edit_appointment/<app_id>/<user_id>')
def edit_appointment(app_id, user_id):
    """ 
    Lets us edit the data for an existing appointment
    """

    if 'user' in session:
        login_user = users_collection.find_one({"username": session['user']})   
        _appointment = appointments_collection.find_one({'_id': ObjectId(app_id)})
        all_depts = departments_collection.find()
        return render_template('edit_appointment.html',
                                page_title='Edit Appointment',
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

    """ 
    data comes from cur_value in $('#department').change(function()
    """

    data = request.form['dept_name']
        
    for dept in services:
        if dept['dept_name'] == data:
            service = dept['service']
             
                   
    if service:
        return jsonify({'data': service})
    

    return jsonify({'error' : 'an error occurred'})



@app.route('/update_appointment/<app_id>/<user_id>', methods=['POST'])
def update_appointment(app_id, user_id):
    """ 
    Lets us edit the data for an existing appointment
    """
    appointments = appointments_collection
    appointments.update_many({'_id': ObjectId(app_id)},
    {'$set': {
        'user_id': user_id,
        'created': datetime.utcnow(),
        'dept_name': request.form.get('dept_name'),
        'service': request.form.get('service'),
        'task_description': request.form.get('task_description'),
        'task_name': request.form.get('task_name'),
        'date_time': request.form.get('date_time'),
        'user_name':  request.form.get('user_name'),
        'is_urgent': request.form.get('is_urgent'),
        'is_archived': request.form.get('is_archived')
    }
        
    })
    return redirect(url_for('get_appointment'))


@app.route('/delete_appointment/<app_id>/<user_id>')
def delete_appointment(app_id, user_id):
    """ 
    Lets us edit the data for an existing appointment
    """

    if 'user' in session:
        login_user = users_collection.find_one({"username": session['user']})      
        appointments_collection.remove({'_id': ObjectId(app_id)})
        return redirect(url_for('get_appointment', 
                        username=session['user'], 
                        user_id=login_user['_id']))

    return render_template('login.html', page_title='Log-in')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Departments views                                                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

@app.route('/get_departments', defaults={'user_id': None})
@app.route('/get_departments/<user_id>')
def get_departments(user_id):
    """ 
    Lets us return the names of all the departments
    """
    if 'user' in session:
        login_user = users_collection.find_one({"username": session['user']}) 
        departments = Search(departments_collection).find_all()
        return render_template('get_departments.html', 
                                page_title='Departments',
                                departments = departments, 
                                username=session['user'], 
                                user_id=login_user['_id'])
    
    return render_template('login.html', page_title='Log-in')




@app.route('/department/<dept_id>/<user_id>')
def department(dept_id, user_id):
    """ 
    Lets us edit the name of a specific department
    """

    if 'user' in session:
        login_user = users_collection.find_one({"username": session['user']}) 
        return render_template('department.html',  
                                page_title='Department',
                                department = departments_collection.find_one(
                                {'_id': ObjectId(dept_id)}), 
                                username=session['user'], 
                                user_id=login_user['_id'])

    return render_template('login.html', page_title='Log-in')


@app.route('/edit_department/<dept_id>/<user_id>')
def edit_department(dept_id, user_id):
    """ 
    Lets us edit the name of a specific department
    """

    if 'user' in session:
        login_user = users_collection.find_one({"username": session['user']}) 
        return render_template('edit_department.html',  
                                page_title='Information',
                                department = departments_collection.find_one(
                                {'_id': ObjectId(dept_id)}), 
                                username=session['user'], 
                                user_id=login_user['_id'])

    return render_template('login.html', page_title='Log-in')


@app.route('/update_department/<dept_id>/<user_id>', methods=['POST'])
def update_department(dept_id, user_id):
    """ 
    The name of a specific department is written back to the document
    """

    departments_collection.update_many({'_id': ObjectId(dept_id)},
        {'$set': {
            'dept_info': request.form.get('dept_info'),
            'main_contact.$[].phone': request.form.get('phone1'),
            'main_contact.$[].email': request.form.get('email'),
            'site.$[].phone': request.form.get('phone2')
        }
        }) 
        
    return redirect(url_for('get_departments'))



@app.route('/add_department',  methods=['POST', 'GET'], defaults={'user_id': None})
@app.route('/add_department/<user_id>')
def add_department(user_id):
    """ 
    The sites and departments are rendered to html
    """

    if 'user' in session: 
        login_user = users_collection.find_one({"username": session['user']})  
        items = dept_template_collection.find()    
        facility = site_template_collection.find()        
        
        return render_template('add_department.html', 
                                page_title='Add a Department', 
                                data = items, facility = facility, 
                                username=session['user'], 
                                user_id=login_user['_id'])

    return render_template('login.html', page_title='Log-in')
   


@app.route('/dept_update',  methods=['POST', 'GET'])
def dept_update():
    """ 
    The services are matched to the department selected
    """
    
    services = dept_template_collection.find()    

    site = request.form.get('site_name')
    

    """ 
    data comes from cur_value in $('#department').change(function() 
    """

    data = request.form['dept_name']
    
    for dept in services:
        if dept['dept_name'] == data:
            service = dept['service']
          
                   
    if service:
        return jsonify({'data': service})
    
    return jsonify({'error' : 'an error occurred'})
    


@app.route('/deptimg_update',  methods=['POST', 'GET'])
def dept_imgupdate():
    """ 
    The services are matched to the department selected
    """

    image = dept_template_collection.find() 
    

    """ 
    data comes from cur_value in $('#department').change(function() 
    """

    data = request.form['dept_name']
    
    
    for dept in image:
        if dept['dept_name'] == data:
            image = dept['img_url']
            
                  
    if service:
        return jsonify({'data': image})
    

    return jsonify({'error' : 'an error occurred'})




@app.route('/insert_department/<user_id>', methods=['POST'])
def insert_department(user_id):
    """ 
    Insert new department into collection
    """

    if 'user' in session: 
        login_user = users_collection.find_one({"username": session['user']})   
        department = departments_collection
        
        department_doc = {
                'dept_owner': session['user'],                 
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
        

        return redirect(url_for('get_departments',
                                username=session['user'], 
                                user_id=login_user['_id']))



@app.route('/update_service/<serv_id>', methods=['POST'])
def update_service(serv_id):
    """ 
    The name of a specific department is written back to the document
    """

    services_collection.update_one({'_id': ObjectId(serv_id)},

        {'$set': {'service.$[].name': request.form.get('service')}})
        
       
    return redirect(url_for('get_departments'))
    

@app.route('/delete_department/<dept_id>/<user_id>')
def delete_department(dept_id, user_id):
    """ 
    Lets us delete an existing department
    """

    if 'user' in session:
        login_user = users_collection.find_one({"username": session['user']})      
        departments_collection.remove({'_id': ObjectId(dept_id)})
        return redirect(url_for('get_departments', 
                        username=session['user'], 
                        user_id=login_user['_id']))

    return render_template('login.html', page_title='Log-in')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Page not found 404 Views                                                                                 #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
@app.errorhandler(404)
def page_not_found(e):
    """ 
    note that we set the 404 status explicitly 
    """
    return render_template('404.html'), 404

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Page not found 404 Views                                                                                 #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
@app.errorhandler(Exception)
def handle_exception(e):
    """ 
    note that we set the 500 status explicitly 
    """
    return render_template('500.html'), 500

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Development/Production environment test for debug                                                        #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == '__main__':
    
    if os.environ.get("DEVELOPMENT"):
   
        app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),            
            debug=True)
    else:
        app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),            
            debug=False)
