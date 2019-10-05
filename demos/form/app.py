from flask import Flask

import config
from views import add_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    add_routes(app)
    return app


