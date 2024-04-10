# external imports
import os
from flask import Flask, jsonify, abort, redirect, request, session, render_template, make_response

# internal imports
import auth
import alchemydatabase as db
from datetime import datetime
from alchemydatabase import (
    create_announcement,
    create_club,
    create_event,
    create_user,
    get_records
)

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../frontend/static',
    template_folder='../frontend'
)
app.secret_key = os.environ['APP_SECRET_KEY']

# Middleware  for Auth
@app.before_request
def authenticate():
    auth.authenticate()

#-----------------------------------------------------------------------

@app.route('/logout')
def logout():
    return auth.logout()

#-----------------------------------------------------------------------
# API Routes
@app.route('/api/announcements')
def announcements():
    res = get_records('announcement')
    print('announcements:', res)
    return {'announcements': res}

@app.route('/api/clubs')
def clubs():
    res = get_records('club')
    # res = get_clubs()
    print('clubs', res)
    return {'clubs': res}

@app.route('/api/events')
def events():
    res = get_records('event')
    print('events:', res)
    return {'events': res}

@app.route('/api/users')
def users():
    res = get_records('user')
    print('users:', res)
    return {'users': res}

@app.route('/api/create_event', methods=['POST'])
def create_new_event():
    event_name = request.form['eventName']
    location = request.form['location']
    description = request.form['description']
    start_datetime = request.form['startDateTime']
    end_datetime = request.form['endDateTime']

    # Creates new event in database
    eventid = get_records('event')[-1][0]
    create_event(event_id=eventid+1, name=event_name, location=location, description=description, start_time=start_datetime, end_time=end_datetime)

    # Render the event creation success page directly
    html_code = render_template('pages/eventcreation_success.html')
    response = make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
        # Authenticate the user and get the CAS username
    cas_username = auth.authenticate()
    print('username:', cas_username)

    # Store authenticated username in session if not already present
    if 'cas_username' not in session:
        session['cas_username'] = cas_username

    # Check if the user exists in the database and create if not
    user_exists = any(user.netid == cas_username for user in db.get_users())
    if not user_exists:
        db.create_user(user_id=int(cas_username[2:]), name=cas_username[:2], netid=cas_username, profile_pic=None)
        
    # check if officer
    user_id = int(cas_username[2:])
    is_officer = any(user.user_id == user_id for user in db.get_officers())

    # Use the username from the session for consistency
    return render_template('pages/home.html', USER_NAME=session['cas_username'], is_officer=is_officer)

@app.route('/contact', methods=['GET'])
def contact_page():
   return render_template('pages/contact.html')

@app.route('/eventcreation', methods=['GET'])
def event_creation_page():
   return render_template('pages/eventcreation.html')

@app.route('/events', methods=['GET'])
def events_page():
    fetched_events = events()
    fetched_events = list(map(lambda event: {
            'name': event[1], 
            'location': event[2],
            'description': event[3], 
            'start_time': event[4],
            'end_time': event[4]
        }, fetched_events['events']))
    sunday_events = list(filter(lambda event: "Sun" in event['start_time'], fetched_events))
    monday_events = list(filter(lambda event: "Mon" in event['start_time'], fetched_events))
    tuesday_events = list(filter(lambda event: "Tue" in event['start_time'], fetched_events))
    wednesday_events = list(filter(lambda event: "Wed" in event['start_time'], fetched_events))
    thursday_events = list(filter(lambda event: "Thu" in event['start_time'], fetched_events))
    friday_events = list(filter(lambda event: "Fri" in event['start_time'], fetched_events))
    saturday_events = list(filter(lambda event: "Sat" in event['start_time'], fetched_events))

    print('MONDAY EVENTS',  monday_events)


    return render_template(
        'pages/calendarpage.html',
        sunday_events=sunday_events,
        monday_events=monday_events,
        tuesday_events=tuesday_events,
        wednesday_events=wednesday_events,
        thursday_events=thursday_events,
        friday_events=friday_events,
        saturday_events=saturday_events
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)
