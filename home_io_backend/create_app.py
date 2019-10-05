import os

from flask import Flask
from flask_migrate import Migrate

from .models import *
from ..config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.db = db
    migrations_dir = os.environ.get('MIGRATIONS_DIR')
    Migrate(app, db, directory=migrations_dir)
    return app
