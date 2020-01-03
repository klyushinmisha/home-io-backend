import os


class Config(object):
    DEBUG = True

    # NOTE: for development only!
    SECRET_KEY = 'a7527038916b46a2b79d65a0e6ee5d98'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    SCRIPTS_PATH = os.environ.get('SCRIPTS_PATH')
