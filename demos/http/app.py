import os

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from jinja2 import escape
from flask import Flask, request, redirect, url_for, session


def create_app():
    app = Flask(__name__)
    print(os.getenv('SECRET_KEY', 'secret string'))
    app.secret_key = os.getenv('SECRET_KEY', 'secret string')

    # get name value from query string and cookie
    @app.route('/')
    @app.route('/hello')
    def hello():
        name = request.args.get('name')
        if name is None:
            name = request.cookies.get('name', 'Human')
        response = '<h1>Hello, %s!</h1>' % escape(name)  # escape name to avoid XSS
        # return different response according to the user's authentication status
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
        return response


    # use int URL converter
    @app.route('/goback')
    @app.route('/goback/<int:year>')
    def go_back(year=100):
        return 'Welcome to %d!' % (2019 - year)


    # redirect
    @app.route('/hi')
    def hi():
        return redirect(url_for('go_back'))

    return app



app = create_app()



