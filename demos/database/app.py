from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

from demos.database import config

db = SQLAlchemy()


def _config_log():
    logger.add("logs/form_app.log", rotation="12:00")


def _config_jinja(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True


def _init_plugins(app):
    db.init_app(app)


def create_app():
    _config_log()

    app = Flask(__name__)
    app.config.from_object(config)

    _init_plugins(app)
