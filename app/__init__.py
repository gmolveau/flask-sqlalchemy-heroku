from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
import os, logging

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    # enable logging via gunicorn
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)

    from .api_v1 import api as api_v1_blueprint
    # all the routes of this api will be prefixed with "/api/v1"
    # ie. POST /api/v1/users/signup
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
