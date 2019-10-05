class Config(object):
    DEBUG = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@home_io_backend_postgres/home_io_backend"