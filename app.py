from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World version 1.0'

if __name__ == '__main__':
    app.run(debug=True)
