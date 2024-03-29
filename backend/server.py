# external imports
import os
from flask import Flask, jsonify, abort, redirect, request, session

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


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

# Middleware  for Auth
@app.before_request
def authenticate():
    if request.endpoint == 'logout':
        return
    res = auth.authenticate()
    if 'username' not in session and res.headers['Location'] is not None:
        return {'login_url': res.headers['Location']}

#-----------------------------------------------------------------------

# Routes for authentication.
@app.route('/login')
def login():
    if 'username' in session:
        return {'username': session['username']}

@app.route('/logout')
def logout():
    res = auth.logoutcas()
    return res

#-----------------------------------------------------------------------

@app.route('/announcements')
def announcements():
    res = get_records('announcement')
    print('announcements:', res)
    return {'data': res}

@app.route('/clubs')
def clubs():
    res = get_records('club')
    # res = get_clubs()
    print('clubs', res)
    return {'data': res}

@app.route('/events')
def events():
    res = get_records('event')
    print('events:', res)
    return {'data': res}

@app.route('/users')
def users():
    res = get_records('user')
    print('users:', res)
    return {'data': res}

if __name__ == '__main__':
    app.run(debug=True, port=8080)
