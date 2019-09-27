import pytest
from demos.http.app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app


def test_hello(client):
    response = client.get('/')
    assert response.data == '<h1>Hello, {0}!</h1>[Not Authenticated]'.format('Human').encode()