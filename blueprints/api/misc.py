from flask import jsonify
from classes.status import Status
from . import api

@api.route('/test')
def test():
    return jsonify(Status.dict(Status.SUCCESS))