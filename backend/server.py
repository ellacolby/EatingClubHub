# external imports
import os
from flask import Flask, jsonify, abort, redirect, request, session, render_template

# internal imports
import auth
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

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../frontend/build',
    template_folder='../frontend/build'
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
    res = get_announcements()
    print('announcements:', res)
    return {'data': res}

@app.route('/api/clubs')
def clubs():
    res = get_clubs()
    print('clubs', res)
    return {'data': res}

@app.route('/api/events')
def events():
    res = get_events()
    print('events:', res)
    return {'data': res}

@app.route('/api/users')
def users():
    res = get_users()
    print('users:', res)
    return {'data': res}

# Temporary solution to load other pages
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8080)
