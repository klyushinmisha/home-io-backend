import os


class Config(object):
    TESTING = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    SCRIPTS_PATH = os.environ.get('SCRIPTS_PATH')
