# external imports
import os
from flask import Flask, jsonify, abort, redirect, request, session, render_template

# internal imports
import auth
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
    return {'data': res}

@app.route('/api/clubs')
def clubs():
    res = get_records('club')
    # res = get_clubs()
    print('clubs', res)
    return {'data': res}

@app.route('/api/events')
def events():
    res = get_records('event')
    print('events:', res)
    return {'data': res}

@app.route('/api/users')
def users():
    res = get_records('user')
    print('users:', res)
    return {'data': res}

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index_page():
    return render_template('pages/index.html')

@app.route('/home', methods=['GET'])
def home_page():
    return render_template('pages/home.html')

@app.route('/contact', methods=['GET'])
def contact_page():
   return render_template('pages/contact.html')

@app.route('/events', methods=['GET'])
def events_page():
    return render_template('pages/calendarpage.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
