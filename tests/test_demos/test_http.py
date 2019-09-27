import os

import pytest

from demos.http.app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


def test_config(app):
    assert app.config['ENV'] == 'development'
    assert os.getenv("PASSWORD") == '123456'


def test_hello(client):
    response = client.get('/')
    assert response.data == '<h1>Hello, {0}!</h1>[Not Authenticated]'.format('Human').encode()
