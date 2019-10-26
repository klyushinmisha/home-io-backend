import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database

from .api.v1.views import *
from .api.v1 import api
from .models import *
from ..config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.db = db
    migrations_dir = os.environ.get('MIGRATIONS_DIR')
    Migrate(app, db, directory=migrations_dir)
    JWTManager(app)
    with app.app_context():
        app.db.session.enable_baked_queries = True
    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        create_database(app.config["SQLALCHEMY_DATABASE_URI"])
    app.register_blueprint(api, url_prefix='/api/v1')
    return app
