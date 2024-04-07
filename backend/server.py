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
    template_folder='../frontend/public'
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
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/contact', methods=['GET'])
def contact():
   return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
