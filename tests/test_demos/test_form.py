import pytest
from loguru import logger

from demos.form.app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture(scope='class')
def session_client(app):
    return app.test_client()


def test_index(client):
    rv = client.open("/", method="GET")
    assert rv.status_code == 200
    assert b'HTML Form' in rv.data
