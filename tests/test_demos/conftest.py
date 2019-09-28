import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parents[2]))  # 将项目根目录加入搜索路径


@pytest.fixture
def app_ctx(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def req_ctx(app):
    with app.test_request_context() as ctx:
        yield ctx


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
