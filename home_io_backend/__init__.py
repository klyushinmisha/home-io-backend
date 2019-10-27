import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database

from .api.v1 import api
from .api.common.responses import MethodNotAllowedResponse
from .api.v1.views import *
from .models import *
from ..config import Config


def create_app():
    # create app and configure it
    # NOTE: config file depends on build type (dev, test, prod)
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize database connection
    db.init_app(app)
    app.db = db
    with app.app_context():
        app.db.session.enable_baked_queries = True

    # setup migrations
    # set custom migration folder
    migrations_dir = os.environ.get('MIGRATIONS_DIR')
    Migrate(app, db, directory=migrations_dir)

    # setup token manager
    JWTManager(app)

    # create database if not exists
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

    # bind api blueprints
    app.register_blueprint(api, url_prefix='/api/v1')

    # setup HTTP error handlers
    with app.app_context():
        from .api.common.error_handlers import handle_method_not_allowed, handle_unprocessable_entity

    return app
