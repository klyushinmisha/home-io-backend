import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    SCRIPTS_PATH = os.environ.get('SCRIPTS_PATH')
