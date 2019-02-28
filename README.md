# Milestone 4 Project

## [Your Medical Services Manager](https://ddeveloper72-your-medical.herokuapp.com/)

  *(Inter-departmental resource for consultations & appointments)*

### by Duncan Falconer for the Code Institute, 2018


## 1. Project Goals

This project is all about facing a new, more difficult challenge which demonstrates Python as the backbone programming language which uses a NoSQL database, called MongoDB for managing all of the site user data.

The project needs to be able to demonstrate the use of CRUD functions:

    1. Create something
    2. Read something
    3. Update something
    4. Delete a something

The application is designed to be hosted on Heroku and will facilitate multiple end users simultaneously to manage their work related information on the site.  Users will be able to use the site by registering their names and then building their profile within the application.  The mongoDB database constructed for this application is hosted on [mLab](https://mlab.com/)

The user's profile will let them select the medical facility at which they work.  They will then be able to select the department in which they work. They will then be able to see information about their department and edit the services offered by that department or add a new service in that department.

The user must then be able to the see the other departments at the medical facility.  They must be able to schedule an appointment for a service, offered by another department.  They must be able to mark the appointment a priority or not as well as favourite the department.  A favourites list of the departments must be available from their own profile.  They user must be able to unfavourite a department as well as to cancel or amend an appointment scheduled.

A nice to have, which is still being considered for the design, will be to let the user rate a consultation by giving it stars out of 5.

## 2 .The UX Design
*(This template is with thanks from 
@sarahloh)*


#### Strategy

| Focus                                                       | User Needs                                                            | Business Objectives                             |
|-------------------------------------------------------------|-----------------------------------------------------------------------|-------------------------------------------------|
| What are you aiming to achieve?                             | To be able to save medical facility department & service information  |  |
|                                                             | To be able to find and use services within a medical facility.  |  |
|                                                             | To be able to favourite a department.  |  |
| For whom?                                                   | To be able to see a list of favourite departments.  |  |
| TARGET AUDIENCE                                             | To be able to add new departments or services to the medical facility  |  |
|                                                             | To be able to change existing department or services  |  |
|                                                             | To be able to remove a service from a department.  |  |
|                                                             | To be able to book and edit a booking for a consultation.  |  |
|                                                             | To be able to add and change contact information for a service.  |  |
|                                                             | To be able to set an urgency to a booking for a consultation.  |  |



#### Scope

| Focus                                                       | Functional Specification                                              | Content Requirements                            |
|-------------------------------------------------------------|-----------------------------------------------------------------------|-------------------------------------------------|
| Which features?                                             | View all services with an option to view just favourites  | A non-relational database has been chosen. See database schema below. |
| What’s on the table?                                        | View all bookings, filterable by service and by urgency |  |
|                                                             | View service |  |
|                                                             | Update service |  |
|                                                             | Add appointment |  |
|                                                             | Update appointment |  |
|                                                             | Complete an appointment |  |
|                                                             | Delete an appointment |  |
|                                                             | Add / remove a favourite service |  |
|                                                             | Create a user login |  |
|                                                             | Create a user dashboard |  |
|                                                             | Create a user settings profile |  |


#### Structure

| Focus                                                       | Interaction Design                                                           | Information Architecture                                                               |
|-------------------------------------------------------------|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| How is the information structured?                          | Where am I? / How did I get here? / What can I do here? / Where can I go?    | Organizational / Navigational schemas (tree / nested list / hub and spoke / dashboard) |
|                                                             | A list of departments offered by a facility will be displayed, with a login button | Tree Structure |
| How is it logically grouped?                                | A user will be prompted for their name to log in.  If one does not exist, they will be prompted to setup a new profile in a department of their choice, or create a new department.  Their profile name will need to be different from all the other profiles. | Start/home page |
|                                                             | The user will be able to customize the services that they offer from their department, when setting up a new department. | Login facility/Create a new account |
|                                                             | The user will be able to see a list of services offered by other departments and favourite the  departments. | Profile page for configuring department and services. |
|                                                             | The user will be able to schedule appointments for consultations in other departments, mark them important and amend/delete their appointment.  | Add/remove departments and the information about them. |
|                                                             | Toggle icons, will let the user select or deselect departments to keep as their favourites. | Add/remove services and the information about them. |


#### Skeleton

| Focus                                                       | Interface Design                                       | Navigational Design  | Information Design  |
|-------------------------------------------------------------|--------------------------------------------------------|----------------------|---------------------|
| How will the information be represented?                    | See wireframes                                         |                      |                     |
| How will the user navigate to the information and features? | See wireframes | All Services |  |
|                                                             |  | Manage Profile (Create & edit) |  |
|                                                             |  | Browse departments & services |  |
|                                                             |  | Create & edit appointments |  |
|                                                             |  | Favourite departments & services (Add & remove |  |
|                                                             |  | Login & logout |  |


#### Surface

| Focus                                                       | Visual Design                       |
|-------------------------------------------------------------|-------------------------------------|
| What will the finished product look like?                   |  |
|                                                             |  |
| What colours, typography and design elements will be used?  |  |

##### Wireframes

![Index](https://github.com/ddeveloper72/milestone-4-project/blob/master/static/images/readme/gallery.png "Fig 1 showing Wireframes")

#### 3. Application Construction

1. Tools used
   
   *  Written in VSCode
   * The noSQL database was created with MongoDB (see database included with repository) and is hosted at [MongoDB Hosting: Database-as-a-Service by mLab](https://mlab.com/home)
   * css files were created and stored locally within the application as static files.
   * The app as tested using Chrome dev tools & VSCode debugger
   * HTML and CSS checked with help from the Mark-up Validation Service
   * Version management and test branches created in git
   * Web deployment hosted on Heroku

2. Reference Literature
   
   * [MongoDB Documentation](https://docs.mongodb.com/)
   * [Quick-Start Guide to mLab](https://docs.mlab.com/)
   * [Quick-Start Guide to mLab \| mLab Documentation & Support](https://docs.mlab.com/)
   * [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
   * [Flask-Session](Flask-Session)
   * [Message Flashing](http://flask.pocoo.org/docs/1.0/patterns/flashing/)
   * [Deploying with Git \| Heroku Dev Centre](https://devcenter.heroku.com/articles/git)
   
3. Code Development

    The project brief was to follow a a pattern of **Test Driven Development**.  Testing was carried out writing functions and then verify the data returned from the function.  In this case, print statemetns were created to print cursor from a data collection and then print specific obects or key value pairs.

    Where CRUD opeations were beibng carreid out, the data was verified by watching the updates being caried out to the data collection hosted on mLab.

    Server codes were used to monitor POST GET transations from the forms.

4. Deployment Instructions

  1. Instructions for deployment to a hosing site: [Heroku](https://www.heroku.com/)
    
  In Heroku - Part 1

  1. Log into Heroku
  2. Select New and Create new App.
  3. Create a App name, select the region.
      - then Create app.

  4. Select Deploy 
      - Note the deployment instructions
  
  In Cloud 9

  1. Log in to Heroku:         
     - `heroku login`
  1. Verify the app name is present, created in step 1 above: 
      - `heroku apps`
  2. Connect git to new app location on Heroku: 
      - `heroku git:remote -a ddeveloper72-your-medical set git remote herokutohttps://git.heroku.com/ddeveloper72-your-medical`
  3. Create the requirements file, defining the modules imported to Heroku:
      - `sudo pip3freeze --local > requirements.txt`
  4. Create the proc file: 
      - `echo web: python run.py > Procfile`
  5. Add all project files: 
      - `git add .`
  6. Create a default message for the first commit to Heroku:
     - `git commit -am "makeit better- Use Heroku"`
  7. Push the project to Heroku: 
     - `git push heroku master`
     - `heroku buildpacks:clear`
  8.  Push the project to Heroku 
      - `git push heroku master` (watch the installation log for errors).
  9.  Scale the app dynos for Heroku:
      - `heroku ps:scale web=1`
  10. Set app.py debug to false before publishing
         
         
```python  
    if __name__ == '__main__':    
        if os.environ.get("DEVELOPMENT"):   
          app.run(host=os.getenv('IP'),
                port=os.getenv('PORT'),            
                debug=True)
        else:
            app.run(host=os.getenv('IP'),
                port=os.getenv('PORT'),            
                debug=False)
            
``` 

  11.   Execute 
        - `it push heroku master`
  12.    Save above changes to existing git profile 
         - `git push`

In Heroku - Part 1

  1. Select Settings
      - Select `Config Vars`
      - set `IP` to `0.0.0.0`
      - set `PORT` to `5000`
      - set `SECRET_KEY` to `Some_Secret`
  2. Select More, beside Open app:
      - Click `Restart all dynos`.
  3. Click Open app
      - Select new tab, [Milestone 4 Code Institute Project](https://ddeveloper72-your-medical.herokuapp.com/get_appointment)

#### 4. Mongo Database Schema

1. Appointment

```javascript
{
    "_id": {
        "$oid": "5c7033e7657a2e2e1c63550e"
    },
    "site_name": "Naas General Hospital",
    "dept_name": "Podiatry",
    "service": "Wound care management",
    "task_name": "John",
    "task_description": "Testing UTC date time",
    "date_time": "23-02-2019 20:30",
    "action": "",
    "created": {
        "$date": "2019-02-22T20:33:15.358Z"
    },
    "is_archived": null,
    "is_urgent": null,
    "user_id": "5c70352c657a2e2e1c63550f",
    "user_name": "John"
}

```

2. Department Service

```javascript

{
    "_id": {
        "$oid": "5bc725e9ddf88f8498a7da2b"
    },
    "dept_name": "Physiotherapy",
    "dept_info": "Infomation about this department",
    "img_url": "http://clipart.coolclips.com/480/vectors/tf05310/CoolClips_vc063115.png",
    "main_contact": [
        {
            "phone": "01-29 209291",
            "email": "Physiotherapy@hospital.ie"
        }
    ],
    "service": [
        "Critical Care ICU HDU CCU",
        "Surgical & Medical Wards",
        "Neurology",
        "Trauma",
        "Injury/Orthopaedics/Emergency Department Clinics",
        "Limb Reconstruction/ Amputee Rehabilitation",
        "Pulmonary Rehabilitation",
        "Cardiac Rehabilitation",
        "Paediatrics",
        "Care of the Elderly",
        "Oncology & Breast Care Service",
        "Adult & Paediatric CF Service",
        "Elective Orthopaedics",
        "Hydrotherapy",
        "Ante/Post Natal Care",
        "Continence Service",
        "SCBU"
    ],
    "site": [
        {
            "location": "Naas General Hospital",
            "phone": "045-29 209000"
        }
    ]
}

```

3. User Profile

```javascript

{
    "_id": {
        "$oid": "5c393581657a2e0bd8590744"
    },
    "username": "John",
    "password": "pbkdf2:sha256:50000$VenBfkl5$78062b7e315ee0ddcb8d15be6e9f26250222435b47ae65d93440ff19b264e061",
    "dept_name": "Peri-operative",
    "likes": [
        "5bc725e9ddf88f8498a7da2b",
        "5bc72619ddf88f8498a7da2c"
    ],
    "created": {
        "$date": "2019-01-12T00:32:01.564Z"
    },
    "user_contact": [
        {
            "phone": "0123456",
            "email": "John.Somebody@gmail.com"
        }
    ],
    "site_name": "Naas General Hospital"
}

```

4. Facility

```javascript

{
    "_id": {
        "$oid": "5bb7130fe7179a6602f55042"
    },
    "site_name": "Naas General Hospital",
    "site_info": "Naas, Co Kildare"
}

```

5. New Department_Template

```javascript

{
    "_id": {
        "$oid": "5be3858d02ea182abcb20f2b"
    },
    "dept_name": "Physiotherapy",
    "dept_info": "Infomation about this department",
    "img_url": [
        "http://clipart.coolclips.com/480/vectors/tf05310/CoolClips_vc063115.png"
    ],
    "service": [
        "Critical Care ICU HDU CCU",
        "Surgical & Medical Wards",
        "Neurology",
        "Trauma",
        "Injury/Orthopaedics/Emergency Department Clinics",
        "Limb Reconstruction/ Amputee Rehabilitation",
        "Pulmonary Rehabilitation",
        "Cardiac Rehabilitation",
        "Paediatrics",
        "Care of the Elderly",
        "Oncology & Breast Care Service",
        "Adult & Paediatric CF Service",
        "Elective Orthopaedics",
        "Hydrotherapy",
        "Ante/Post Natal Care",
        "Continence Service",
        "SCBU"
    ]
}

```

6. New Site_Template


```javascript

{
    "_id": {
        "$oid": "5be621d8fb6fc072d4670591"
    },
    "site": [
        {
            "location": "Naas General Hospital",
            "phone": "045-29 209291"
        }
    ]
}

```

7 Image_Template


```javascript
{
    "_id": {
        "$oid": "5be7f592d525102080b639fa"
    },
    "base_img": "http://clipart.coolclips.com/480/vectors/tf05309/CoolClips_vc062037.png"
}


```

#### 5. Development & Testing

  * When I first started developing this app, used Materialize CSS.  I really like the accordion styles, but unfortunately I rand into issues with the Materialize JQuery being incompatible with how I was injecting my services lists into the html.  The Materialize accordion wasn't permitting me to render my lists in the correct place.  So i has to switch to using pure bootstrap 4,  and then learned to implement a similar accordion style by means of a jinja for loop, that would increment the numerical element of the id tags, so as to allow me to crate the accordion elements. 
  
  ```html
  {% for app in appointment %}
   <div class="card-header accordian-card" id="heading{{ loop.index }}" data-toggle="collapse"
                        data-target="#collapse{{ loop.index }}" aria-expanded="false" aria-controls="collapse{{ loop.index }}"
                        data-toggle="tooltip">
  {% endfor %}
  ```
  
                      
  * During development, media responsiveness of the app was tested using Chrome dev tools to simulate different small and large screen devices.  
  * I later shared my application with family and friends on WhatsApp so that they could follow the Heroku link to the dashboard application on their mobile devices.  In this way  I found that I had to resize font sizes for the get_appointment and departments pages.  
  * I found response issues when viewing the game when switching between portrait and landscape modes in my development environment.  I was able to correct these by adding in media queries to my sass file.
  * When testing the game in multiplayer mode-  I created several player logins by running different browsers simultaneously.  The browsers and hardware that I used were:
      
    1.  Chrome
    2.  Firefox
    3.  Opra Browser
    4.  Internet Explorer
    5.  Edge
    6.  Chrome mobile
   
  ### Debugging Strategy
  
  I thought that the best way to test this game was to run a beta test by putting the game on Heroku and then letting everyone in my college try it.  While doing so, I asked for feedback on the game. This is the feedback I got:

### _The issues found_

  1. When logging in, the user name and password fields hadn't been made required.
  2. The appointments accordion would look and work better if the whole accordion was the button.
  3. The delete cancel and save buttons used to add, cancel or delete user input to the application, would be better if relocated to the right hand side of the cards.
  4. When a user selects a date/time for an appointment, the modal doesn't close automatically, till one selects the app outside of the date/time modal.
  5. When logging in with the incorrect username and password, the flash messaging didn't work.
  6. It was recommended that the user name be shown on the profile page.
  7. The phone number fields could be saved with nonsense numeric data.
  8. The hover styles on the date/time picker made the background the and colour the same.
  9. The user name of the person creating a department or and appointment is not being saved in the appointment.  When viewing an appointment, the name is being provide by session.username

### _The fixes implemented_
(Bugs were found by peer group review)

1. I made all text input fields required for the user registration and login forms as well as double checked all of the other forms used for collecting data for the application.
2. I moved the button controls into the accordion div, so now the accordion behaves like a button.
3. I changed the bootstrap grid styles for the application cards and in so doing, I also relocated the position of the buttons.
4. I have gone back to look at the stock code for the [Tempus Dominus](https://tempusdominus.github.io/bootstrap-4/) date time picker that i selected for this project and noted that this is the default behaviour for the button.  I realized then, that it is required.  If one were to select an incorrect date time, it would then be input into the date time field.  In this way, if a date time is selected, the user confirms this by then selecting outside the modal or by pressing enter on the keyboard.
5. An indentation error was found, that prevented the view function from returning the flash message.
6. A username heading was added to the profile page as well as included in some flash messaging.
7. A jQuery input field mask was installed, sourced from [Igor Escobar](https://igorescobar.github.io/jQuery-Mask-Plugin/) for structuring the telephone numbers.
8. The date time picker styles are now modified by css, to apply a strong contrasting colour when the mouse hovers over the text fields.
9. The document creator name is saved in the document.  Only if a user updates an appointment, does their new name overwrite the original appointment creator's name.

#### 6. Credits

- The images used in this project have been sourced from [Coolclips](http://www.coolclips.com/) with thanks
  
- There are loads of people that I want to give credit to.  These include, first and foremost my family for their support!

- My friends within the Code Institute who go by the Slack handles @abonello_lead @JoWings, @Eventret, @Miro, @MarieO, @saraloh, @JohnL3, @Sonya, @Shane Muirhead, my Mentor, Nishant and tutors @niel_ci and many others.  You guys have helped me to find my way and personally shared resources like UXD design templates-to help keep my thoughts on task and on track and help with my C9 and VSCode coding environments.  Thank you ladies and gentlemen!
    
<h6><span class="text-muted">Milestone 4 project for the Code Institute <br />by Duncan Falconer, 2018</span></h6>