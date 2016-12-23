# encoding: utf-8
from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Mp, User
from . import api
from .decorators import permission_required
from .errors import forbidden
from flask_jwt import jwt_required, current_identity


@api.route('/mps/')
@jwt_required()
def get_mps():
	# request.args.items().__str__()
	username = request.args.get('username')
	print username
	mps = User.query.filter_by(username=username).first().subscribed_mps
	mps_list = [ mp.to_json() for mp in mps ]
	print mps_list
	return jsonify(mps_list)

