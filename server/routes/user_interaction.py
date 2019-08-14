from __future__ import absolute_import

from server import app
from flask import request, jsonify
from bson.json_util import dumps

from ..databases.mongo_models import *
from ..services import oxford_dictionary as od
from ..services import task_generator as tg

import json

@app.route('/exam-result', methods=['POST', 'GET'])
def update_exam_result():
	if(request.is_json):
		results = request.get_json()
		user_id = request.args.get('user-id')
		user = User.objects().get(index=int(user_id))
		for result in results:
			word = result['word']
			answer = result['answer']
			score = 0
			for v in answer:
				if v == 0:
					score -= 10
				else:
					score += 10
			for i in range(len(user.learning_words)):
				if user.learning_words[i].word == word:
					ma_score = user.learning_words[i].ma_score
					ma_score = min(100, max(ma_score + score, 0))
					# print(word, ma_score)
					user.learning_words[i].ma_score = ma_score
		user.save()
		return jsonify("OK")
	else:
		return jsonify("Wrong json format")


