from flask import Flask
from loguru import logger

import config
from views import add_routes


def _config_log():
    logger.add("logs/form_app.log", rotation="12:00")


def _inject_variables():
    return dict(alert_color="purple")


def config_jinja(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True


def create_app():
    _config_log()
    app = Flask(__name__)
    app.config.from_object(config)
    app.context_processor(_inject_variables)

    add_routes(app)
    config_jinja(app)
    return app
