from flask import Flask

app = Flask(__name__)

@app.route('/api')
def index():
    data = {'data': 'Hello, World'}
    return data

if __name__ == '__main__':
    app.run(debug=True, port=8080)