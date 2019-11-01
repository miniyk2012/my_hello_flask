import os
import sys
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from loguru import logger

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = str(Path(__file__).parents[2])
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

db = SQLAlchemy()


def _config_log():
    logger.add("logs/form_app.log", rotation="12:00")


def _config_jinja(app):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True


def _init_plugins(app):
    # SQLite URI compatible, database URL
    WIN = sys.platform.startswith('win')
    if WIN:
        prefix = 'sqlite:///'
    else:
        prefix = 'sqlite:////'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                      prefix + os.path.join(app.root_path, 'data.db'))  # 绝对路径
    db.init_app(app)


def create_app():
    from demos.database import config, cmds, views

    _config_log()

    app = Flask(__name__)
    app.config.from_object(config)

    _init_plugins(app)
    cmds.register(app)
    views.register(app)
    return app

