# Hall Booking System

This is a project that allows registered users to request the admin to book halls by giving details like the date,timing of event and hall they want. Admins approve of the requests. Makes sure 2 bookings do not intersect with each other Made using Django and Django REST Framework and Djangorestframework-simplejwt.

## Features:

- Two bookings do not intersect with each other.
- Does not allow bookings that clash with slots already approved by the admin
- Users are allowed to edit the requirements of their bookings. If they edit an already booked slot, the booking_status changes to 'pending'
- User authorization using JWT

## Important!

The admin must have created a hall for the users to access it. This way the number of halls can be modified
While giving an input the request should be as follows

"hallname":"Aryabhatta", // give it as hallname while adding and if updating, made sure that we do not have to know the hall id, can give it just by knowing the name of the hall
"date": "2024-12-18",  // Date in 'YYYY-MM-DD' format
"start_time": "21:30:00",  // Time in 'HH:MM:SS' format
"end_time": "22:00:00"  // Time in 'HH:MM:SS' format

The order is not important, but maintain the formats 

## Functionality/URLS

#### 
GET- FOR everyone, The website opens to the list of halls that are provided

#### register
 POST- Creates the user, input fields are roll_no, username and password

#### login
 POST- Login user, input fields are username and password
 
#### createhall

 POST- FOR ADMINS ONLY, input fields - name


#### pendingrequests

 GET- FOR ADMINS ONLY, gets the requests that are pending sorted by the first ones sent

#### changebookingstatus/id

 POST- FOR ADMINS ONLY, input fields - booking_status. The admin can change it to any of the 4, 'available','booked' (to approve),'pending','rejected'. If the admin books a slot that has already been booked, it does not follow through, the status remains as pending
 id - is the id of the Schedule object made when a user requests to book a hall
  
#### bookhall

 POST- FOR USERS and ADMINS, input fields - hallname, start_time, end_time, date

#### changebookingdetails/id

FOR ADMINS and the USER who made the booking ONLY

id - is the id of the Schedule object made when a user requests to book a hall

GET- The details of the booking made

 PUT/PATCH-  input fields - hallname, date, start_time, end_time. If ediiting a slot that has already been booked, changes the booking status to pending

 DELETE- Delete the booking/request
 
#### getallbookings

 GET- FOR everyone, shows all the bookings that have been done (booking_status == booked)


## Backend Hosted URL
The backend is hosted on render at 
https://hall-booking-system-backend-3y1q.onrender.com


## To run the library system:

#### 1. Clone the repository:
   `git clone "https://github.com/thomasjames433/Hall_Booking_System_Backend.git"`
#### 2. Navigate into the project directory:
   `cd Hall_Booking_System`
#### 3. Install dependencies:
   - `python manage.py makemigrations`
   - `python manage.py migrate`  
   - `To createsuperuser: python manage.py createsuperuser`
   - `pip freeze > requirements.txt`
#### 4. Run the system:
   `python manage.py runserver`

## Technologies Used
- Django
- Django-Rest-Framework
- Django-Rest-Framework-simplejwt


## LICENSE

