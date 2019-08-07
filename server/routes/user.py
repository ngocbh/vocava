from __future__ import absolute_import

from server import app
from flask import request, jsonify
from bson.json_util import dumps

from ..databases.mongo_models import *
from ..services import oxford_dictionary as od
from ..services import task_generator as tg

import json

@app.route('/user-info', methods=['GET'])
def get_user_info():
	user_id = request.args.get('user-id')

	if user_id != None:
		try:
			user = User.objects().get(index=int(user_id))
		except Exception:
			return 'Doesnot match any user id from database', 404
		return jsonify(user.to_dict())
	else:
		users = User.objects()
		ret = [user.to_dict() for user in users]
		return jsonify(ret)


