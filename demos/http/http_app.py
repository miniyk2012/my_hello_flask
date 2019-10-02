import os
import time

from jinja2.utils import generate_lorem_ipsum
from loguru import logger

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import escape
from flask import (Flask, request, redirect, url_for, session, abort, after_this_request,
                   Response, make_response, jsonify, current_app, g)


def config_log():
    logger.add("logs/http_app.log", rotation="12:00")


def create_app():
    app = Flask(__name__)
    config_log()

    logger.info(os.getenv('SECRET_KEY', 'secret string'))
    app.secret_key = os.getenv('SECRET_KEY', 'secret string')

    load_envs()

    @app.before_request
    def get_name():
        name = request.args.get('name')
        if name is None:
            name = request.cookies.get('name', 'Human')
        logger.warning(f'get cookie: {name}')
        g.name = name

    # get name value from query string and cookie
    @app.route('/')
    @app.route('/hello', methods=['POST', 'GET'])
    def hello():
        name = g.name
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
        logger.error('not found')
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
            logger.info(response.is_json)

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
            logger.info(response.is_json)

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
            logger.info(response.is_json)

        elif content_type == 'json':
            body = {"note": {
                "to": "Peter",
                "from": "Jane",
                "heading": "Remider",
                "body": "Don't forget the party!"
            }
            }

            response = jsonify(body)
            logger.info(response.is_json)
            # logger.info(response.get_json())

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

    @app.route('/login')
    def login():
        session['logged_in'] = True
        return redirect(url_for('hello'))

    @app.route('/admin')
    def admin():
        if 'logged_in' in session:
            return 'Welcome to admin page.'
        abort(403)

    @app.route('/logout')
    def logout():
        if 'logged_in' in session:
            session.pop('logged_in')
        return redirect(url_for('hello'))

    # AJAX
    @app.route('/post')
    def show_post():
        post_body = generate_lorem_ipsum(n=2)

        return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#load').click(function() {
            $.ajax({
                url: '/more',
                type: 'get',
                success: function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>''' % post_body

    @app.route('/more')
    def load_post():
        return generate_lorem_ipsum(n=1)

    @app.route('/currentapp')
    def get_current_app():
        logger.info(type(request._get_current_object()))
        logger.info(type(request))
        logger.info(type(current_app))
        logger.info(type(current_app._get_current_object()))
        return current_app.name

    @app.route('/do-something')
    def do_something():
        time.sleep(0.1)
        logger.info(request.referrer)
        return redirect_back()

    # redirect to last page
    @app.route('/foo')
    def foo():
        return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
               % url_for('do_something', next=request.full_path)

    @app.route('/bar')
    def bar():
        return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' \
               % url_for('do_something', next=request.full_path)

    return app


def load_envs():
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
    flask_env = Path(__file__).parent / '.flaskenv'
    load_dotenv(dotenv_path=flask_env)


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        logger.info(f'target={target}')
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    logger.info(f'host_url={request.host_url}')
    logger.info(f'ref_url={ref_url}')
    logger.info(f'test_url={test_url}')
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


app = create_app()
