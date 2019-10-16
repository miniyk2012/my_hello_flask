import os

from flask import Flask
from flask_ckeditor import CKEditor
from flask_dropzone import Dropzone
from flask_session import Session
from loguru import logger

import config
from views import add_routes


def _config_log():
    logger.add("logs/form_app.log", rotation="12:00")


def _inject_variables():
    return dict(alert_color="purple")


def _config_jinja(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.config['UPLOAD_PATH'] = os.path.join(app.root_path, "uploads")


def _init_plugins(app):
    CKEditor(app)
    Dropzone(app)
    Session(app)


def create_app():
    _config_log()
    app = Flask(__name__)

    app.config.from_object(config)
    app.context_processor(_inject_variables)

    _init_plugins(app)
    add_routes(app)
    _config_jinja(app)
    return app
