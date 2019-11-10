import os
import sys
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
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


def _init_plugins(app, test):
    WIN = sys.platform.startswith('win')
    if WIN:
        prefix = 'sqlite:///'
    else:
        prefix = 'sqlite:////'
    if not test:
        # SQLite URI compatible, database URL

        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                          prefix + os.path.join(app.root_path, 'data.db'))  # 绝对路径

    else:

        app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(PROJECT_DIR, 'tests', 'test_demos', 'testdata.db')
        app.config['SQLALCHEMY_ECHO'] = False
    db.init_app(app)

    migrate = Migrate(app, db)


def create_app(test=False):
    from demos.database import config, cmds, views

    _config_log()

    app = Flask(__name__)
    app.config.from_object(config)

    _init_plugins(app, test)

    cmds.register(app)
    views.register(app)


    return app
