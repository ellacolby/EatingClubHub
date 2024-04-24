# external imports
import os
from flask import Flask, jsonify, abort, redirect, request, session, render_template, make_response

# internal imports
import auth
import alchemydatabase as db
from datetime import datetime
from alchemydatabase import (
    create_announcement,
    create_event,
    get_records
)
from name import get_name

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

def auth_info():
    cas_username = auth.authenticate()
    name = get_name(cas_username)

    # check if officer
    user_id = cas_username
    is_officer = any(user.user_id == user_id for user in db.get_officers())
    club_id, club_name = None, None
    if is_officer:
        club_id, club_name = db.get_officer_club_info(user_id)
    return name, is_officer, club_id, club_name

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

@app.route('/api/make_new_officer', methods=['POST'])
def make_new_officer():
    user_id = request.form['netid']
    _, is_officer, club_id, club_name = auth_info()

    db.create_officer(user_id=user_id, club_id=club_id)

    html_code = render_template(
       'pages/profile.html',
       is_officer=is_officer,
       club_name=club_name,
    )
    response = make_response(html_code)
    return response

@app.route('/api/edit_profile', methods=['POST'])
def edit_profile():
    user_id = auth.authenticate()
    pronouns = request.form['pronouns']
    about_me = request.form['about_me']
    _, is_officer, club_id, club_name = auth_info()

    if pronouns:
        db.edit_user_field(user_id, 'pronouns', pronouns)
    if about_me:
        db.edit_user_field(user_id, 'about_me', about_me)

    html_code = render_template(
       'pages/profile.html',
       is_officer=is_officer,
       club_name=club_name,
    )
    response = make_response(html_code)
    return response

    
@app.route('/api/create_event', methods=['POST'])
def create_new_event():
    event_name = request.form['eventName']
    location = request.form['location']
    description = request.form['description']
    start_datetime = request.form['startDateTime']
    end_datetime = request.form['endDateTime']

    # Creates new event in database
    create_event(
        name=event_name, 
        location=location, 
        description=description, 
        start_time=start_datetime, 
        end_time=end_datetime
    )

    html_code = render_template('pages/calendarpage.html')
    response = make_response(html_code)
    return response

@app.route('/api/create_announcement', methods=['POST'])
def create_new_announcement():
    announcement_title = request.form['announcementTitle']
    announcement_descrip = request.form['announcementDescription']

    # Creates new announcement in database
    create_announcement(
        title=announcement_title, 
        description=announcement_descrip
    )
    fetched_announcements = announcements()
    fetched_announcements = [list(announcement) for announcement in fetched_announcements['announcements']]  # Convert tuples to lists
    
    _, is_officer, _, _ = auth_info()

    html_code = render_template(
        'pages/announcements/announcementspage.html',
        announcements=fetched_announcements,
        is_officer=is_officer
    )
    response = make_response(html_code)
    return response
    
#-----------------------------------------------------------------------
# Page Renderings

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
    cas_username, is_officer, _, _ = auth_info()
    # Use the username from the session for consistency
    return render_template('pages/home.html', USERNAME=cas_username, is_officer=is_officer)

@app.route('/contact', methods=['GET'])
def contact_page():
   return render_template('pages/contact.html')

@app.route('/profile', methods=['GET'])
def profile_page():
    _, is_officer, club_id, club_name = auth_info()
    return render_template(
        'pages/profile.html',
        is_officer=is_officer,
        club_name=club_name,
        )

@app.route('/eventcreation', methods=['GET'])
def event_creation_page():
    return render_template('pages/events/eventcreation.html')

@app.route('/announcementcreation', methods=['GET'])
def announcement_creation_page():
    return render_template('pages/announcements/announcementcreation.html')

@app.route('/announcements', methods=['GET'])
def announcements_page():
    fetched_announcements = announcements()
    fetched_announcements = [list(announcement) for announcement in fetched_announcements['announcements']]  # Convert tuples to lists
    print(fetched_announcements)
    _, is_officer, _, _ = auth_info()

    return render_template(
        'pages/announcements/announcementspage.html',
        announcements=fetched_announcements,
        is_officer=is_officer
    )

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

    all_events = {
        'sunday': sunday_events,
        'monday': monday_events,
        'tuesday': tuesday_events,
        'wednesday': wednesday_events,
        'thursday': thursday_events,
        'friday': friday_events,
        'saturday': saturday_events
    }
    _, is_officer, _, _ = auth_info()
    
    return render_template(
        'pages/events/calendarpage.html',
        events=all_events,
        list_events=[event for row in list(all_events.values()) for event in row],
        is_officer=is_officer
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)
