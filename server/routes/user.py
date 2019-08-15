from __future__ import absolute_import

from server import app
from flask import request, jsonify
from bson.json_util import dumps
from mongoengine import ListField
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

@app.route('/reset-user', methods=['GET'])
def reset_user_data():
	user_id = request.args.get('user-id')
	field = request.args.get('field')
	if user_id == None:
		user_id = 1
	user = User.objects().get(index=int(user_id))
	if field == 'sentences':
		print("Clear user.sentence")
		user.sentences = []
	elif field == 'exam_score':
		print("Clear user.exam_score")
		user.exam_score = []
	
	user.save()
	return "OK"

@app.route('/statistic', methods=['GET'])
def statistic():
	user_id = request.args.get('user-id')
	if user_id == None:
		user_id = 1
	user = User.objects().get(index=int(user_id))
	result = {}
	quantity = {1: 0, 2: 0, 3: 0, 4: 0}
	for wordwp in user.learning_words:
		quantity[tg.analyzer.choose_task4word(wordwp.ma_score)] += 1
	result['quantity'] = quantity
	result['exam_score'] = [score for score in user.exam_score]
	return jsonify(result)
	