from flask import Blueprint

api = Blueprint('api', __name__)

from . import misc
from . import auth
from . import core