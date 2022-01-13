import logging
import os

from flask import Flask, session

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql+psycopg2://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .database import db
    db.init_app(app)

    from .bcrypt import b_crypt
    b_crypt.init_app(app)

    from .cli import cli_init_app
    cli_init_app(app)

    from .marshmallow import ma
    ma.init_app(app)

    # enable logging via gunicorn
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)

    from .api_v1 import api as api_v1_blueprint
    # all the routes of this api will be prefixed with "/api/v1"
    # ie. POST /api/v1/users/signup
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
