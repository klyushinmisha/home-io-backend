from webargs.flaskparser import FlaskParser

parser = FlaskParser()

from .auth import *
from .devices import *
from .scripts import *
from .users import *
