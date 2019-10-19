import pytest

from demos.database.app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app

