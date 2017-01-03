# encoding: utf-8
from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Mp, User
from . import api
from flask_jwt import jwt_required, current_identity
from flask_security import auth_token_required

@api.route('/mps/')
@auth_token_required
def get_mps():
	# request.args.items().__str__()
	email = request.args.get('email')
	print email
	mps = User.query.filter_by(email=email).first().subscribed_mps
	mps_list = [ mp.to_json() for mp in mps ]
	print mps_list
	return jsonify(mps_list)

