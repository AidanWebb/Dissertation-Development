from flask import Blueprint

website = Blueprint('website', __name__)

from . import root_pages
