# external imports
import os
from flask import Flask, jsonify, abort, redirect, request, session

# internal imports
import auth
from datetime import datetime
from database import (
    create_announcement,
    create_club,
    create_event,
    create_user,
    get_announcements, 
    get_clubs, 
    get_events, 
    get_users
)

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

# Middleware  for Auth
@app.before_request
def authenticate():
    res = auth.authenticate()
    if 'username' in session:
        return
    if res.headers['Location'] is not None:
        return {'login_url': res.headers['Location']}

#-----------------------------------------------------------------------

# Routes for authentication.

@app.route('/logout')
def logout():
    res = auth.logoutcas()
    return res

#-----------------------------------------------------------------------

@app.route('/announcements')
def announcements():
    res = get_announcements()
    print('announcements:', res)
    return {'data': res}

@app.route('/clubs')
def clubs():
    res = get_clubs()
    print('clubs', res)
    return {'data': res}

@app.route('/events')
def events():
    res = get_events()
    print('events:', res)
    return {'data': res}

@app.route('/users')
def users():
    res = get_users()
    print('users:', res)
    return {'data': res}

if __name__ == '__main__':
    app.run(debug=True, port=8080)
