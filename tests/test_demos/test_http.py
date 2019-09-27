import os

import pytest

from demos.http.http_app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


def test_config(app):
    assert app.config['ENV'] == 'development'
    assert os.getenv("PASSWORD") == '123456'
    print(app.name)


def test_hello(client):
    response = client.get('/')
    assert response.data == '<h1>Hello, {0}!</h1>[Not Authenticated]'.format('Human').encode()
