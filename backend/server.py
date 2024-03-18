from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/api')
def index():
    data = {'data': str(datetime.now())}
    return data

if __name__ == '__main__':
    app.run(debug=True, port=8080)