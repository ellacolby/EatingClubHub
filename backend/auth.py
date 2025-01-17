#!/usr/bin/env python

#-----------------------------------------------------------------------
# auth.py
# Authors: Alex Halderman, Scott Karlin, Brian Kernighan, Bob Dondero
#-----------------------------------------------------------------------

import urllib.request
import urllib.parse
import re
import flask
import alchemydatabase as db
from sqlalchemy.exc import IntegrityError
from name import get_name

#-----------------------------------------------------------------------

_CAS_URL = 'https://fed.princeton.edu/cas/'

#-----------------------------------------------------------------------

# Return url after stripping out the "ticket" parameter that was
# added by the CAS server.

def strip_ticket(url):
    if url is None:
        return "something is badly wrong"
    url = re.sub(r'ticket=[^&]*&?', '', url)
    url = re.sub(r'\?&?$|&$', '', url)
    return url

#-----------------------------------------------------------------------

# Validate a login ticket by contacting the CAS server. If
# valid, return the user's username; otherwise, return None.

def validate(ticket):
    val_url = (_CAS_URL + "validate" + '?service='
        + urllib.parse.quote(strip_ticket(flask.request.url))
        + '&ticket=' + urllib.parse.quote(ticket))
    lines = []
    with urllib.request.urlopen(val_url) as flo:
        lines = flo.readlines()   # Should return 2 lines.
    if len(lines) != 2:
        return None
    first_line = lines[0].decode('utf-8')
    second_line = lines[1].decode('utf-8')
    if not first_line.startswith('yes'):
        return None
    return second_line

#-----------------------------------------------------------------------

# Authenticate the remote user, and return the user's username.
# Do not return unless the user is successfully authenticated.

def authenticate():
    login_url = (_CAS_URL + 'login?service=' +
            urllib.parse.quote(flask.request.url))

    # If the username is in the session, then the user was
    # authenticated previously.  So return the username.
    if 'username' in flask.session:
        return login_url, flask.session.get('username')
    
    # [already logged in, username]
    # [first log in, ]

    # If the request does not contain a login ticket, then redirect
    # the browser to the login page to get one.
    ticket = flask.request.args.get('ticket')
    if ticket is None:
        login_url = (_CAS_URL + 'login?service=' +
            urllib.parse.quote(flask.request.url))
        return login_url, None
        flask.abort(flask.redirect(login_url))


    # If the login ticket is invalid, then redirect the browser
    # to the login page to get a new one.
    username = validate(ticket)
    if username is None:
        login_url = (_CAS_URL + 'login?service='
            + urllib.parse.quote(strip_ticket(flask.request.url)))
        flask.abort(flask.redirect(login_url))

    username = username.strip()
    # Check if the user exists in the database and create if not
    user_exists = any(user.user_id == username for user in db.get_users())
    if not user_exists:
        try:
            try:
                name = get_name(username)
            except ValueError:
                print("Not a Princeton student")
            db.create_user(user_id=username, name=name, netid=username, profile_pic=None)
        except IntegrityError:
            print("A user with this ID already exists.")

    # The user is authenticated, so store the username in
    # the session.
    flask.session['username'] = username
    return None, username

#-----------------------------------------------------------------------

def logout():
    # Log out of the CAS session, and then the application.
    flask.session.clear()
    #logout_url = (_CAS_URL + 'logout?service='
    #    + urllib.parse.quote("http://localhost:8080"))
    logout_url = ('/')
    flask.abort(flask.redirect(logout_url))
