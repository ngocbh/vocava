from __future__ import absolute_import

from server import app
from flask import request, jsonify
from bson.json_util import dumps

from ..databases.mongo_models import *
from .. services import oxford_dictionary as od

import json

@app.route('/user-info', methods=['GET'])
def get_user_info():
	try:
		user_id = request.args.get('id')
	except:
		user_id = None

	if user_id != None:
		try:
			user = UserDoc.objects().get(index=int(user_id))
		except Exception:
			return 'Doesnot match any user id from database'
		return jsonify(user.to_dict())
	else:
		users = UserDoc.objects()
		ret = [user.to_dict() for user in users]
		return jsonify(ret)
