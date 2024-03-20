from flask import Flask
from datetime import datetime
from database import (
    get_announcements,
    get_clubs,
    get_events,
    get_users,
)

app = Flask(__name__)

@app.route('/api')
def index():
    data = {'data': str(datetime.now())}
    return data

@app.route('/announcements')
def announcements():
    res = get_announcements()
    print(res)
    return res


@app.route('/clubs')
def clubs():
    res = get_clubs()
    print(res)
    return res

@app.route('/events')
def events():
    res = get_events()
    print(res)
    return res

@app.route('/users')
def users():
    res = get_users()
    print(res)
    return res

if __name__ == '__main__':
    app.run(debug=True, port=8080)