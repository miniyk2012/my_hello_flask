import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parents[2] / pathlib.Path('demos') / pathlib.Path('form')))  # 将form目录加入搜索路径

import pytest
from flask_wtf import FlaskForm
from loguru import logger
from wtforms import Form, BooleanField, StringField, validators, PasswordField, SubmitField

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


def test_config(app):
    assert app.secret_key == "12345"
    assert app.root_path == "/Users/thomas_young/Documents/projects/my_hello_flask/demos/form"


class TestWTForms:
    clz = Form

    @pytest.fixture
    def _login_form_clz(self):
        class LoginForm(self.clz):
            username = StringField('Username', render_kw={"placeholder": "Your name"},
                                   validators=[validators.DataRequired()])
            password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(8, 128)])
            remember = BooleanField('Remember me', default="checked")
            submit = SubmitField('Log in')

        return LoginForm

    @pytest.fixture
    def form(self, _login_form_clz):
        return _login_form_clz()

    def test_login_form(self, form):
        assert form.username() == '''<input id="username" name="username" placeholder="Your name" required type="text" value="">'''
        assert form.username.label() == '''<label for="username">Username</label>'''

        assert form.password() == '''<input id="password" name="password" required type="password" value="">'''
        assert form.password.label() == '''<label for="password">Password</label>'''

        self.expect_data(form)

        logger.info(form.remember())
        logger.info(form.remember.label())

        logger.info(form.submit())
        logger.info(form.submit.label())

        assert form.username(style="width: 200px;") \
               == '''<input id="username" name="username" placeholder="Your name" required style="width: 200px;" type="text" value="">'''

    def expect_data(self, form):
        assert form.data == {'username': None, 'password': None, 'remember': True, 'submit': False}


class TestFlaskWTF(TestWTForms):
    clz = FlaskForm

    @pytest.fixture
    def form(self, app, _login_form_clz):
        request_ctx = app.test_request_context('/')
        request_ctx.push()
        yield _login_form_clz()  # FlaskForm必须在请求上下文中才能实例化
        request_ctx.pop()

    def expect_data(self, form):
        logger.info(form.data)
        assert form.data == {'username': None, 'password': None, 'remember': True, 'submit': False, 'csrf_token': None}
