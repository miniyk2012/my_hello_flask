import os

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import escape
from flask import (Flask, request, redirect, url_for, session, abort, after_this_request,
                   Response, make_response, jsonify)


def create_app():
    app = Flask(__name__)
    print(os.getenv('SECRET_KEY', 'secret string'))
    app.secret_key = os.getenv('SECRET_KEY', 'secret string')

    load_envs()

    # get name value from query string and cookie
    @app.route('/')
    @app.route('/hello', methods=['POST', 'GET'])
    def hello():
        name = request.args.get('name')
        if name is None:
            name = request.cookies.get('name', 'Human')
            # print(f'get cookie: {name}')
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
    @app.route('/hi', methods=['POST', 'GET'])
    def hi():
        return redirect(url_for('go_back'))

    colors = ['blue', 'white', 'red']

    # use any URL converter
    @app.route('/colors/<any(%s):color>' % ', '.join(colors))
    def three_colors(color):
        return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'

    # return error response
    @app.route('/brew/<drink>')
    def teapot(drink):
        if drink == 'coffee':
            abort(418)
        else:
            return 'A drop of tea.'

    # 404
    @app.route('/404')
    def not_found():
        print('not found')
        abort(404)

    @app.route('/after_this_request')
    def do_sth_after():
        @after_this_request
        def do_after(response: Response):
            response.data = response.data + b'! No'
            return response

        return 'Ok'

    # return response with different formats
    @app.route('/note', defaults={'content_type': 'text'})
    @app.route('/note/<content_type>')
    def note(content_type):
        content_type = content_type.lower()
        if content_type == 'text':
            body = '''Note
to: Peter
from: Jane
heading: Reminder
body: Don't forget the party!
'''
            response: Response = make_response(body)
            response.mimetype = 'text/plain'
            print(response.is_json)

        elif content_type == 'html':
            body = '''<!DOCTYPE html>
<html>
<head></head>
<body>
  <h1>Note</h1>
  <p>to: Peter</p>
  <p>from: Jane</p>
  <p>heading: Reminder</p>
  <p>body: <strong>Don't forget the party!</strong></p>
</body>
</html>
'''
            response = make_response(body)
            response.mimetype = 'text/html'
            print(response.is_json)

        elif content_type == 'xml':
            body = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>Peter</to>
  <from>Jane</from>
  <heading>Reminder</heading>
  <body>Don't forget the party!</body>
</note>
'''
            response = make_response(body)
            response.mimetype = 'application/xml'
            print(response.is_json)

        elif content_type == 'json':
            body = {"note": {
                "to": "Peter",
                "from": "Jane",
                "heading": "Remider",
                "body": "Don't forget the party!"
            }
            }

            response = jsonify(body)
            print(response.is_json)
            # print(response.get_json())

            # equal to:
            # response = make_response(json.dumps(body))
            # response.mimetype = "application/json"
        else:
            abort(400)
        return response

    # 500
    @app.route('/500')
    def error_500():
        return jsonify(message='Error!'), 500

    # set cookie
    @app.route('/set/<name>')
    def set_cookie(name):
        response: Response = make_response(redirect(url_for('hello')))
        response.set_cookie('name', name)
        return response

    return app


def load_envs():
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
    flask_env = Path(__file__).parent / '.flaskenv'
    load_dotenv(dotenv_path=flask_env)


app = create_app()
