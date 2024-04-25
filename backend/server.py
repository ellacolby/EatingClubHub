# external imports
import os
from flask import Flask, jsonify, abort, redirect, request, session, render_template, make_response

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
    cas_username, is_officer, club_id, club_name = auth_info()
    
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return error404()

    db.create_officer(user_id=cas_username, club_id=club_id)

    html_code = render_template(
       'pages/profile.html',
       is_officer=is_officer,
       club_name=club_name,
    )
    response = make_response(html_code)
    return response

@app.route('/api/edit_profile', methods=['POST'])
def edit_profile():
    cas_username, is_officer, _, club_name = auth_info()
    if cas_username is None:
        return splash_page()
    
    pronouns = request.form['pronouns']
    about_me = request.form['about_me']

    if pronouns:
        db.edit_user_field(cas_username, 'pronouns', pronouns)
    if about_me:
        db.edit_user_field(cas_username, 'about_me', about_me)

    html_code = render_template(
       'pages/profile.html',
       is_officer=is_officer,
       club_name=club_name,
    )
    response = make_response(html_code)
    return response

    
@app.route('/api/create_event', methods=['POST'])
def create_new_event():
    cas_username, is_officer, club_id, club_name = auth_info()
    
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        print("reached is officer false")
        return error404()
    
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
    cas_username, is_officer, _, _ = auth_info()
    
    if cas_username is None:
        return splash_page()
    
    event_id = 0

    # Creates new event in database
    db.create_event_attendee(
        event_id = event_id,
        user_id = cas_username
    )
    
    html_code = render_template(
        'pages/events/calendarpage.html',
        is_officer=is_officer
    )
    response = make_response(html_code)
    return response

@app.route('/api/delete_event', methods=['POST'])
def delete_event():
    cas_username, is_officer, _, _ = auth_info()
    
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return error404()
    
    event_id = request.args.get('eventId')
    print('event_id:', event_id)
    success = db.delete_event(event_id)
    return {'success': success}

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
        return error404()
    
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
        return error404()
    
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
        images = ['styles/cap.jpeg', 'styles/colo.jpeg', 'styles/cannon.jpeg']
        return render_template('pages/splash.html', images=images, CAS_LOGIN_URL=url)
    return home_page()
        

@app.route('/home', methods=['GET'])
def home_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    images = ['styles/cap.jpeg', 'styles/colo.jpeg', 'styles/cannon.jpeg']
    
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
    
    print(fetched_announcements)
    print(announcements_dict)
    
    # Use the username from the session for consistency
    return render_template('pages/home.html', USERNAME=cas_username, is_officer=is_officer, images=images, announcements=announcements_dict)

@app.route('/contact', methods=['GET'])
def contact_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    return render_template('pages/contact.html', is_officer=is_officer)

@app.route('/error404', methods=['GET'])
def error404():
    images = ['styles/cap.jpeg', 'styles/colo.jpeg', 'styles/cannon.jpeg']
    return render_template('pages/error404.html', images=images)

@app.route('/profile', methods=['GET'])
def profile_page():
    cas_username, is_officer, club_id, club_name = auth_info()
    if cas_username is None:
        return splash_page()
    return render_template(
        'pages/profile.html',
        is_officer=is_officer,
        club_name=club_name,
        )

@app.route('/eventcreation', methods=['GET'])
def event_creation_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return error404()
    return render_template('pages/events/eventcreation.html', is_officer=is_officer)

@app.route('/announcementcreation', methods=['GET'])
def announcement_creation_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return error404()
    return render_template('pages/announcements/announcementcreation.html', is_officer=is_officer)

@app.route('/announcements', methods=['GET'])
def announcements_page():
    fetched_announcements = announcements()
    fetched_announcements = [list(announcement) for announcement in fetched_announcements['announcements']]  # Convert tuples to lists
    print(fetched_announcements)
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
    cas_username, is_officer, _, _ = auth_info()
    
    if cas_username is None:
        return splash_page()
    
    return render_template(
        'pages/events/calendarpage.html',
        is_officer=is_officer
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)
