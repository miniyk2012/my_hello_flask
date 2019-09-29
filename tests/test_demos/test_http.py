import os

import pytest
from flask import Response

from demos.http.http_app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture(scope='class')
def session_client(app):
    return app.test_client()


class TestHttp:

    def test_config(self, app):
        assert app.config['ENV'] == 'development'
        assert os.getenv("SECRET_KEY") == '123456'
        # print(app.name)

    def test_url_map(self, app):
        print(app.url_map)

    def test_hello(self, client):
        response = client.get('/?name=yangkai')
        assert response.data == '<h1>Hello, {0}!</h1>[Not Authenticated]'.format('yangkai').encode()

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