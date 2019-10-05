import os

from flask import Flask
from flask_migrate import Migrate
from sqlalchemy_utils import database_exists, create_database

from .models import *
from ..config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.db = db
    migrations_dir = os.environ.get('MIGRATIONS_DIR')
    Migrate(app, db, directory=migrations_dir)
    with app.app_context():
        app.db.session.enable_baked_queries = True
    if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
        create_database(app.config["SQLALCHEMY_DATABASE_URI"])
    return app
