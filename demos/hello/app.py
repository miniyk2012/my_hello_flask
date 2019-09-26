from flask import Flask, url_for


app = Flask(__name__)


@app.route('/')
def index():
    return f'<h1>Hello, World!</h1> {url_for("greet", name="yangkai", _external=True)}'

@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'


@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name
