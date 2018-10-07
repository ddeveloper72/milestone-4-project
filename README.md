# Milestone 4 Project

## [Your Medical Services Manager](https://ddeveloper72-your-medical.herokuapp.com/)

  *(Inter-departmental resource for consultations & appointments)*

### by Duncan Falconer for the Code Institute, 2018

1. The project brief can be found by clicking [here](https://github.com/ddeveloper72/milestone-4-project/blob/master/readme/brief.md).
  
2. The Guidelines for the project can be found by clicking [here](https://github.com/ddeveloper72/milestone-4-project/blob/master/readme/guidelines.md).

## 1. Project Goals

This project is all about facing a new, more difficult challenge which demonstrates Python as the backbone programming language which uses a NoSQL database, called MongoDB for managing all of the site user data.

The project needs to be able to demonstrate the use of CRUD functions:

    1. Create something
    2. Read something
    3. Update something
    4. Delete a something

The application is designed to be hosted on Heroku and will facilitate multiple end users simultaneously to manage their work related information on the site.  Users will be able to use the site by registering their names and then building their profile within the application.

The user's profile will let them select the medical facility at which they work.  They will then be able to select the department in which they work. They will then be able to see information about their department and edit the services offered by that department or add a new service in that department.

The user must then be able to the see the other departments at the medical facility.  They must be able to schedule an appointment for a service, offered by another department.  They must be able to mark the appointment a priority or not as well as favourite the department.  A favourites list of the departments must be available from their own profile.  They user must be able to unfavourite a department as well as to cancel or amend an appointment scheduled.

A nice to have, which is still being concidered for the design, will be to let the user rate a consultation by giving it stars out of 5.

## 2 .The UX Design
*(This template is with thanks from 
@sarahloh)*


#### Strategy

| Focus                                                       | User Needs                                                            | Business Objectives                             |
|-------------------------------------------------------------|-----------------------------------------------------------------------|-------------------------------------------------|
| What are you aiming to achieve?                             | To be able to save medical facility department & service informtion  |  |
|                                                             | To be able to find and use services within a medical facility.  |  |
| For whom?                                                   | To be able to see a list of favorite departments.  |  |
| TARGET AUDIENCE                                             | To be able to add new departments or services to the medical facility  |  |
|                                                             | To be able to change existing department or services  |  |
|                                                             | To be able to remove a service from a department.  |  |
|                                                             | To be able to book and edit a booking for a consultation.  |  |
|                                                             | To be able to rate a servce on completion of a consultation out of 5 stars.  |  |
|                                                             | To be able to add and change contact information for a service.  |  |
|                                                             | To be abel to set an urgency to a booking for a consultation.  |  |



#### Scope

| Focus                                                       | Functional Specification                                              | Content Requirements                            |
|-------------------------------------------------------------|-----------------------------------------------------------------------|-------------------------------------------------|
| Which features?                                             | View all services with an option to vew just favorites  | A non-relational database has been chosen. See database schema below. |
| What’s on the table?                                        | View all bookings, filterable by service and by urgency |  |
|                                                             | View service |  |
|                                                             | Update service |  |
|                                                             | Add appointment |  |
|                                                             | Update appointment |  |
|                                                             | Complete an appointment |  |
|                                                             | Delete an appointmet |  |
|                                                             | Add / remove a favorite service |  |
|                                                             | Create a user login |  |
|                                                             | Create a user dashboard |  |
|                                                             | Create a user settings profile |  |


#### Structure

| Focus                                                       | Interaction Design                                                           | Information Architecture                                                               |
|-------------------------------------------------------------|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| How is the information structured?                          | Where am I? / How did I get here? / What can I do here? / Where can I go?    | Organizational / Navigational schemas (tree / nested list / hub and spoke / dashboard) |
|                                                             | A list of departments offored by a facility will be displayed, with a login button | Tree Structure |
| How is it logically grouped?                                | A user will be prompted for thir name to log in.  If one does not exist, they will be prompted to setup a new profile in a department of their choice, or create a new department.  Their profile name will need to be different from all the other profiles. | Start/home page |
|                                                             | The user will be able to customize the services that they offer from their department. | Login facility/Create a new account |
|                                                             | The user will be able to see a list of services oppored by other departments and favorite the services offored by those departments. | Profile page for configuring department and services. |
|                                                             | The user will be able to schedule appointments for consultations in other departments, mark them important and amend/delete their appointment.  Should an appointment already exist for that time-slot for that service, the user will be prompted to pick a different time/date from a list of available slots in that week. | Add/remove departments and the information about them. |
|                                                             | Toggle icons, will let the user select or deselect departmetns to keep as their favorites. | Add/remove services and the information about them. |


#### Skeleton

| Focus                                                       | Interface Design                                       | Navigational Design  | Information Design  |
|-------------------------------------------------------------|--------------------------------------------------------|----------------------|---------------------|
| How will the information be represented?                    | See wireframes                                         |                      |                     |
| How will the user navigate to the information and features? | See mockups designs | All Services |  |
|                                                             |  | Manage Profile (Create & edit) |  |
|                                                             |  | Browse departments & services |  |
|                                                             |  | Create & edit own bookings |  |
|                                                             |  | Favourite departmets & services (Add & remove |  |
|                                                             |  | Login & logout |  |


#### Surface

| Focus                                                       | Visual Design                       |
|-------------------------------------------------------------|-------------------------------------|
| What will the finished product look like?                   |  |
|                                                             |  |
| What colours, typography and design elements will be used?  |  |

#### Mongo Database Schema

1. Appointment

```javascript
{
    "site": [
    "siteId"
  ],
  "department": [
    "deptId"
  ],
  "user": [
    "userId"
  ],
  "is_urgent": "off",
  "task_description": "",
  "task_name": [
    "servId"
  ],
  "sched_date": "",
  "sched_time": "",
  "status": "on"
}

```

2. Department Service

```javascript

{
    "dept": "Laboratory",
    "dept_info": "Infomation about this department",
    "img_url": "url reference to a category image for this department",
    "serv": [
        "Blood bank",
        "Biochemistry",
        "Haematology",
        "Histopathology",
        "Microbiology",
        "Public health diagnostic services",
        "Serology/immunology"
    ]
}

```

3. User Profile

```javascript

{
    "name": "",
    "staffNum": "",
    "password": "",
    "siteInfo": {
    "siteName": [
      "siteId"
    ],
    "deptId": [
      "deptId"
    ]
  },
  "profession": [
    "professionId"
  ],
  "img_url": "",
  "department_head": "off",
  "fav_dept": [
    "deptId"
  ],
  "fav_serv": [
    "servId"
  ],
  "appointments": [
    "appointmentId"
  ]
}

```

4. Facility

```javascript

{
    "site": "Naas General Hospital"
}

```

5. Profession

```javascript

{
    "profession": "Doctor"
}

```

6. Service Information

```javascript

{
    "serv": "Critical Care ICU HDU CCU",
    "description": "Service description"
}

```