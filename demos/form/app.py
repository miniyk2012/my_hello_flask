from flask import Flask
from loguru import logger

import config
from views import add_routes


def config_log():
    logger.add("logs/form_app.log", rotation="12:00")


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    config_log()

    add_routes(app)
    return app
