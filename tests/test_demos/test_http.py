import os

import pytest
from flask import Response, current_app, request, url_for
from loguru import logger

from demos.http.http_app import create_app
from utils import here

HERE = here(__name__)


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture(scope='class')
def session_client(app):
    return app.test_client()


class TestHttp:

    def test_config(self, app, client):
        assert app.config['ENV'] == 'development'
        assert os.getenv("SECRET_KEY") == '123456'
        # app.root_path == /path/to/my_hello_flask/demos/http
        assert app.root_path == os.path.join(os.path.dirname(os.path.dirname(HERE)), "demos", "http")

    def test_context(self, app, client):
        response = client.get('/currentapp')
        assert response.data.decode() == app.name

        with app.app_context():
            assert current_app.name == app.name

        request_ctx = app.test_request_context('/curious?name=yangkai')
        request_ctx.push()
        assert request.method == 'GET'
        assert request.args['name'] == 'yangkai'
        assert request.path == '/curious'
        assert request.url == 'http://localhost/curious?name=yangkai'
        assert url_for('hello') == '/hello'  # 依赖请求上下文才可以执行
        request_ctx.pop()

    def test_url_map(self, app):
        logger.info(app.url_map)

    def test_hello(self, client):
        response = client.get('/?name=yangkai')
        assert response.data == '<h1>Hello, {0}!</h1>[Not Authenticated]'.format('yangkai').encode()

    def test_after_request(self, client):
        response = client.get('/after_this_request')
        assert response.data.decode() == 'Ok! No'

    def test_404(self, client):
        response: Response = client.get('/notexist')
        assert response.status_code == 404

    def test_direct(self, client):
        response = client.post('/hi')
        assert response.status_code == 302

    def test_unsupported_method(self, client):
        response = client.post('/')
        assert response.status_code == 405

        response = client.get('/')
        assert response.status_code == 200
        assert response.headers.get('Set-Cookie') is None

    def test_500(self, client):
        response: Response = client.get('/500')
        assert response.status_code == 500
        assert response.is_json
        assert response.json == {'message': 'Error!'}
        assert response.headers.get('Set-Cookie') is None

    def test_set_cookie(self, client):
        response: Response = client.get('/set/yangkai')
        assert response.status_code == 302
        assert response.headers.get('Set-Cookie') is not None

        response = client.get('/')
        assert response.data == '<h1>Hello, {0}!</h1>[Not Authenticated]'.format('yangkai').encode()

    def test_do_something(self, client):
        response: Response = client.get('/do-something?next=/foo?')
        assert 'foo' in response.location
        response: Response = client.get('/do-something?next=http://www.baidu.com')
        assert 'baidu' not in response.location
        assert 'hello' in response.location

    def test_redirect(self):
        from flask import redirect
        # 经实验发现, route必须在第一次请求发生前已经都设置好, 否则会报错.
        # 由于app fixture是session级别的的, 故不能在其他case跑过之后, 再在其上挂新的route
        # 因此这里新建一个独立的app, 请求在route挂上后再发起
        isolate_app = create_app()

        @isolate_app.route('/invalid-redirect')
        def invalid_redirect():
            return redirect('www.baidu.com')

        @isolate_app.route('/valid-redirect')
        def valid_redirect():
            return redirect('http://www.baidu.com')  # redirect需要有schema[http, https]

        client = isolate_app.test_client()
        response: Response = client.get('/invalid-redirect')
        assert client.get(response.location).status_code == 404
        logger.info(f'valid {response.location}')  # redirect需要有schema[http, https]

        response: Response = client.get('/valid-redirect')
        logger.info(f'valid {response.location}')

        redirect_response = client.get(response.location)
        assert 'www.baidu.com' in redirect_response.data.decode()


class TestSession:

    @pytest.fixture
    def login(self, session_client):
        session_client.get('/login')

    @pytest.fixture
    def logout(self, session_client):
        session_client.get('/logout')

    def test_admin_403(self, logout, session_client):
        response = session_client.get('/admin')
        assert response.status_code == 403

    def test_admin_success(self, logout, login, session_client):
        response = session_client.get('/admin')
        assert response.status_code == 200
        assert response.data == 'Welcome to admin page.'.encode()
