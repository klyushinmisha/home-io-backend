from webargs.flaskparser import FlaskParser

parser = FlaskParser()

from .auth import *
from .users import *
from .devices import *
