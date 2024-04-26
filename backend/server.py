# external imports
import os
from flask import Flask, jsonify, abort, redirect, request, session, render_template, make_response
import json

# internal imports
import auth
import alchemydatabase as db
from datetime import datetime
from alchemydatabase import (
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
# @app.before_request
# def authenticate():
#     auth.authenticate()

def auth_info():
    _, cas_username = auth.authenticate()
    
    if cas_username is None:
        return None, None, None, None
    
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
    return {'announcements': res}

@app.route('/api/clubs')
def clubs():
    res = get_records('club')
    return {'clubs': res}

@app.route('/api/events')
def events():
    res = get_records('event')
    return {'events': res}

@app.route('/api/users')
def users():
    res = get_records('user')
    return {'users': res}

@app.route('/api/make_new_officer', methods=['POST'])
def make_new_officer():
    user_id = request.form['netid']
    cas_username, is_officer, club_id, club_name = auth_info()
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)

    db.create_officer(user_id=user_id, club_id=club_id)
    _, netid = auth.authenticate()
    user_info = db.get_user_info(netid)

    html_code = render_template(
        'pages/profile.html',
        is_officer=is_officer,
        club_name=club_name,
        user_info=user_info
    )
    response = make_response(html_code)
    return response

@app.route('/api/edit_profile', methods=['POST'])
def edit_profile():
    cas_username, is_officer, _, club_name = auth_info()
    if cas_username is None:
        return splash_page()
    _, netid = auth.authenticate()
    pronouns = request.form['pronouns']
    about_me = request.form['about_me']
    
    db.edit_user_field(netid, 'pronouns', pronouns)
    db.edit_user_field(netid, 'about_me', about_me)
        
    user_info = db.get_user_info(netid)

    html_code = render_template(
        'pages/profile.html',
        is_officer=is_officer,
        club_name=club_name,
        user_info=user_info
    )
    response = make_response(html_code)
    return response

    
@app.route('/api/create_event', methods=['POST'])
def create_new_event():
    cas_username, is_officer, club_id, club_name = auth_info()
    
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)
    
    event_name = request.form['eventName']
    location = club_name
    description = request.form['description']
    start_datetime = request.form['startDateTime']
    end_datetime = request.form['endDateTime']

    # Creates new event in database
    db.create_event(
        name=event_name, 
        location=location, 
        description=description, 
        start_time=start_datetime, 
        end_time=end_datetime
    )
    
    html_code = render_template(
        'pages/events/calendarpage.html',
        is_officer=is_officer
    )
    response = make_response(html_code)
    return response

@app.route('/api/attend_event', methods=['POST'])
def attend_event():
    _, uid = auth.authenticate()
    cas_username, _, _, _ = auth_info()
    
    if cas_username is None:
        return splash_page()
    
    event_id = request.args.get('eventId')

    print('Event ID:', event_id)

    # Creates new event in database
    db.create_event_attendee(
        event_id = event_id,
        user_id = uid
    )

    print('helloooo')

    return {'success': True}
    

@app.route('/api/delete_event', methods=['POST'])
def delete_event():
    cas_username, is_officer, _, _ = auth_info()
    
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)
    
    event_id = request.args.get('eventId')
    success = db.delete_event(event_id)
    return {'success': success}


@app.route('/api/get_event_attendees', methods=['GET'])
def get_event_attendees():
    event_id = request.args.get('eventId')
    uid_attendees = db.get_event_attendees(event_id=event_id)
    name_attendees = list(map(lambda attendee: get_name(attendee), uid_attendees))

    return {'attendees': name_attendees}
# @app.route('/api/edit_event', methods=['POST'])
# def edit_event():
#     _, is_officer, club_id, club_name = auth_info()
#     event_name = request.form['eventName']
#     location = club_name
#     description = request.form['description']
#     start_datetime = request.form['startDateTime']
#     end_datetime = request.form['endDateTime']

#     db.edit_event(new_name=event_name, new_location=location, new_description=description, new_start_time=start_datetime, new_end_time=end_datetime)

#     html_code = render_template(
#         'pages/events/calendarpage.html',
#         is_officer=is_officer
#     )
#     response = make_response(html_code)
#     return response


@app.route('/api/create_announcement', methods=['POST'])
def create_new_announcement():
    cas_username, is_officer, club_id, _ = auth_info()
    
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)
    
    announcement_title = request.form['announcementTitle']
    announcement_descrip = request.form['announcementDescription']

    # Creates new announcement in database
    db.create_announcement(
        title=announcement_title, 
        description=announcement_descrip,
        club_id=club_id
    )
    fetched_announcements = announcements()
    fetched_announcements = [list(announcement) for announcement in fetched_announcements['announcements']]  # Convert tuples to lists
    

    html_code = render_template(
        'pages/announcements/announcementspage.html',
        announcements=fetched_announcements,
        is_officer=is_officer
    )
    response = make_response(html_code)
    return response

@app.route('/api/delete_announcement', methods=['POST'])
def delete_announcement():
    cas_username, is_officer, _, _ = auth_info()
    
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)
    
    announcement_id = int(request.data.decode('utf-8'))
    db.delete_announcement(announcement_id=announcement_id)

    fetched_announcements = announcements()
    fetched_announcements = [list(announcement) for announcement in fetched_announcements['announcements']]  # Convert tuples to lists

    html_code = render_template(
        'pages/announcements/announcementspage.html',
        announcements=fetched_announcements,
        is_officer=is_officer
    )
    response = make_response(html_code)
    return response

# @app.route('/api/edit_announcement', methods=['POST'])
# def delete_announcement():
#     announcement_title = request.form['announcementTitle']
#     announcement_descrip = request.form['announcementDescription']

#     db.edit_announcement(new_title=announcement_title,new_description=announcement_descrip)

#     _, is_officer, _, _ = auth_info()
#     fetched_announcements = announcements()
#     fetched_announcements = [list(announcement) for announcement in fetched_announcements['announcements']]  # Convert tuples to lists

#     html_code = render_template(
#         'pages/announcements/announcementspage.html',
#         announcements=fetched_announcements,
#         is_officer=is_officer
#     )
#     response = make_response(html_code)
#     return response
#-----------------------------------------------------------------------
# Page Renderings

@app.route('/', methods=['GET'])
@app.route('/splash', methods=['GET'])
def splash_page():
    ticket = request.args.get('ticket')
    url, name = auth.authenticate()
    
    if name is not None:
        return home_page()
    if ticket is None:
        images = ['styles/cannon.jpeg','styles/cap.jpeg', 'styles/charter.jpeg', 'styles/cloister.jpeg', 'styles/colo.jpeg', 'styles/cottage.png', 'styles/ivy.jpeg', 'styles/quad.jpeg', 'styles/terrace.jpeg', 'styles/ti.jpeg', 'styles/tower.jpeg']
        return render_template('pages/splash.html', images=images, CAS_LOGIN_URL=url)
    return home_page()
        

@app.route('/home', methods=['GET'])
def home_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    images = ['styles/cannon.jpeg','styles/cap.jpeg', 'styles/charter.jpeg', 'styles/cloister.jpeg', 'styles/colo.jpeg', 'styles/cottage.png', 'styles/ivy.jpeg', 'styles/quad.jpeg', 'styles/terrace.jpeg', 'styles/ti.jpeg', 'styles/tower.jpeg']
    
    fetched_announcements = announcements()
    fetched_announcements = [list(announcement) for announcement in fetched_announcements['announcements']]  # Convert tuples to lists
    
    announcements_dict = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: []
    }
    
    for i in range(1, 12):
        for announcement in fetched_announcements:
            if announcement[4] == i:
                prev = announcements_dict[i]
                prev.append(announcement)
                announcements_dict[i] = prev
        
    # Use the username from the session for consistency
    return render_template('pages/home.html', USERNAME=cas_username, is_officer=is_officer, images=images, announcements=announcements_dict)

@app.route('/contact', methods=['GET'])
def contact_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    return render_template('pages/contact.html', is_officer=is_officer)

@app.route('/profile', methods=['GET'])
def profile_page():
    cas_username, is_officer, club_id, club_name = auth_info()
    if cas_username is None:
        return splash_page()
    
    _, netid = auth.authenticate()
    user_info = db.get_user_info(netid)
    return render_template(
        'pages/profile.html',
        is_officer=is_officer,
        club_name=club_name,
        user_info=user_info
    )

@app.route('/eventcreation', methods=['GET'])
def event_creation_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)
    return render_template('pages/events/eventcreation.html', is_officer=is_officer)

@app.route('/announcementcreation', methods=['GET'])
def announcement_creation_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)
    return render_template('pages/announcements/announcementcreation.html', is_officer=is_officer)

@app.route('/announcements', methods=['GET'])
def announcements_page():
    fetched_announcements = announcements()
    fetched_announcements = [list(announcement) for announcement in fetched_announcements['announcements']]  # Convert tuples to lists
    cas_username, is_officer, club_id, _ = auth_info()
    
    if cas_username is None:
        return splash_page()

    return render_template(
        'pages/announcements/announcementspage.html',
        announcements=fetched_announcements,
        is_officer=is_officer,
        club_id=club_id
    )

@app.route('/events', methods=['GET'])
def events_page():
    cas_username, is_officer, _, club_name = auth_info()
    
    if cas_username is None:
        return splash_page()
    
    return render_template(
        'pages/events/calendarpage.html',
        username=json.dumps(cas_username),
        is_officer=is_officer,
        club_name=json.dumps(club_name)
    )

@app.errorhandler(404)
def not_found(e):
    images = ['styles/cannon.jpeg','styles/cap.jpeg', 'styles/charter.jpeg', 'styles/cloister.jpeg', 'styles/colo.jpeg', 'styles/cottage.png', 'styles/ivy.jpeg', 'styles/quad.jpeg', 'styles/terrace.jpeg', 'styles/ti.jpeg', 'styles/tower.jpeg']
    cas_username, is_officer, _, _ = auth_info()
    
    if cas_username is None:
        return splash_page()
    return render_template(
        'pages/error404.html',
        images=images,
        is_officer=is_officer
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)
