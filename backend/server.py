# external imports
import os
import sys
from flask import (
    Flask, 
    request, 
    render_template, 
    make_response
)
import json

# internal imports
import auth
import alchemydatabase as db
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

def auth_info():
    _, cas_username = auth.authenticate()

    if cas_username is None:
        return None, None, None, None

    name = get_name(cas_username)

    # check if officer
    user_id = cas_username
    is_officer = any(
        user.user_id == user_id for user in db.get_officers())
    club_id, club_name = None, None
    if is_officer:
        club_id, club_name = db.get_officer_club_info(user_id)
    return name, is_officer, club_id, club_name

def announcements_format(need_dict):
    fetched_announcements = get_records('announcement')
    fetched_announcements = [list(announcement) for announcement in fetched_announcements]
    
    if need_dict:
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
                    
        return announcements_dict
    return fetched_announcements

#-----------------------------------------------------------------------

@app.route('/logout')
def logout():
    return auth.logout()

#-----------------------------------------------------------------------
# API Routes

@app.route('/api/announcements')
def announcements():
    try:
        res = get_records('announcement')
        return {'announcements': res}, 200
    except Exception as ex:
        print('ex:', str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500

@app.route('/api/clubs')
def clubs():
    try:
        res = get_records('club')
        return {'clubs': res}, 200
    except Exception as ex:
        print('ex:', str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500

@app.route('/api/events')
def events():
    try:
        res = get_records('event')
        return {'events': res}, 200
    except Exception as ex:
        print('ex:', str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500

@app.route('/api/users')
def users():
    try:
        res = get_records('user')
        return {'users': res}, 200
    except Exception as ex:
        print('ex:', str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500

@app.route('/api/make_new_officer', methods=['POST'])
def make_new_officer():
    try:
        if not 'netid' in request.form:
            raise Exception('netid is not included in the form request.')
        user_id = request.form['netid']
        cas_username, is_officer, club_id, _ = auth_info()
        if cas_username is None:
            return splash_page()
        if is_officer is False:
            return not_found(404)

        db.create_officer(user_id=user_id, club_id=club_id)
        return {
            'success': True,
            'message': 'New officer has been appointed.'
        }, 200
    except Exception as ex:
        print('ex:', str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500

    
@app.route('/api/edit_profile', methods=['POST'])
def edit_profile():
    cas_username, _, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    try:
        if not request.form:
            raise Exception('form was not submitted properly.')
        
        pronouns = request.form['pronouns']
        about_me = request.form['about_me']

        # User will have already been authenticated from auth_info()
        _, netid = auth.authenticate()

        db.edit_user_field(netid, 'pronouns', pronouns)
        db.edit_user_field(netid, 'about_me', about_me)
        return {
            'success': True,
            'message': 'The profile has been edited.',
        }, 200
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500


    
@app.route('/api/create_event', methods=['POST'])
def create_new_event():
    cas_username, is_officer, _, club_name = auth_info()

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
    try:
        db.create_event(
            name=event_name, 
            location=location, 
            description=description, 
            start_time=start_datetime, 
            end_time=end_datetime
        )
        return {
            'success': True,
            'message': 'Event created successfully.'
        }, 200
    except Exception as ex:        
        print(str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500

@app.route('/api/attend_event', methods=['POST'])
def attend_event():
    _, uid = auth.authenticate()
    cas_username, _, _, _ = auth_info()

    if cas_username is None:
        return splash_page()

    try:
        if not 'eventId' in request.json:
            raise Exception('event-id not found request')

        event_id = request.json['eventId']

        # Creates new event in database
        db.create_event_attendee(
            event_id = event_id,
            user_id = uid
        )
        return {
            'success': True,
            'message': 'The event has been marked as attended.',
        }, 200
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500


@app.route('/api/delete_event', methods=['POST'])
def delete_event():
    cas_username, is_officer, club_id, _ = auth_info()

    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)
        
    try:
        if not 'eventId' in request.json:
            raise Exception('event-id is not found in request body.')
        event_id = request.json['eventId']
        db.delete_event(event_id, club_id)
        return {
            'success': True,
            'messasge': 'The event has been deleted.'
        }, 200
    except Exception as ex:        
        print(str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500


@app.route('/api/get_event_attendees', methods=['GET'])
def get_event_attendees():
    event_id = request.args.get('eventId')
    try:
        uid_attendees = db.get_event_attendees(event_id=event_id)
        name_attendees = list(
            map(lambda attendee: get_name(attendee), uid_attendees))

        return {'attendees': name_attendees}, 200
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500


@app.route('/api/create_announcement', methods=['POST'])
def create_new_announcement():
    cas_username, is_officer, club_id, _ = auth_info()

    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)

    try:
        if not request.form:
            raise Exception('form not submitted properly')
        announcement_title = request.form['announcementTitle']
        announcement_descrip = request.form['announcementDescription']
        # Creates new announcement in database
        db.create_announcement(
            title=announcement_title, 
            description=announcement_descrip,
            club_id=club_id
        )

        return {
            'success': True,
            'message': 'The announcement has been created.'
        }, 200
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500

@app.route('/api/delete_announcement', methods=['POST'])
def delete_announcement():
    cas_username, is_officer, _, _ = auth_info()

    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)

    try:
        if not request.data:
            raise Exception('failed to decode data.')
        announcement_id = int(request.data.decode('utf-8'))

        db.delete_announcement(announcement_id=announcement_id)
        return {
            'success': True,
            'message': 'The announcement has been deleted.'
        }
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        return {
            'error': 'Internal Service Error',
            'message': str(ex)
        }, 500
    
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
        return render_template('pages/splash.html', CAS_LOGIN_URL=url)
    return home_page()
        

@app.route('/home', methods=['GET'])
def home_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    
    announcements_dict = announcements_format(True)
        
    # Use the username from the session for consistency
    return render_template('pages/home.html', USERNAME=cas_username, is_officer=is_officer, announcements=announcements_dict)

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
    return render_template(
        'pages/events/eventcreation.html',
        is_officer=is_officer
        )

@app.route('/announcementcreation', methods=['GET'])
def announcement_creation_page():
    cas_username, is_officer, _, _ = auth_info()
    if cas_username is None:
        return splash_page()
    if is_officer is False:
        return not_found(404)
    return render_template(
        'pages/announcements/announcementcreation.html',
        is_officer=is_officer
        )

@app.route('/announcements', methods=['GET'])
def announcements_page():
    fetched_announcements = db.get_announcements_with_club_names()

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
        is_officer=json.dumps(is_officer),
        club_name=json.dumps(club_name)
    )

@app.errorhandler(404)
def not_found(e):
    cas_username, is_officer, _, _ = auth_info()

    if cas_username is None:
        return splash_page()
    return render_template(
        'pages/error404.html',
        is_officer=is_officer
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)
