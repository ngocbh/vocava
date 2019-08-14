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
	print(request.data)
	print(request.get_data())
	if(request.is_json):
		results = request.get_json()
		user_id = request.args.get('user-id')
		user = User.objects().get(index=int(user_id))
		rets = []
		for result in results:
			word = result['word']
			answer = result['answer']
			print(word, answer)
			score = 0
			for v in answer:
				if v == 0:
					score -= 10
				else:
					score += 10
			for i in range(len(user.learning_words)):
				if user.learning_words[i].word == word:
					ma_score = user.learning_words[i].ma_score
					new_ma_score = min(100, max(ma_score + score, 0))
					user.learning_words[i].ma_score = new_ma_score
					rets.append({'word': word, 'old_ma_score': ma_score, 'new_ma_score': new_ma_score})
					break
		
		# total_score = 0
		# dictionary = Dictionary.objects()
		# for wordwp in user.learning_words:
		# 	word = wordwp.word
		# 	ma_score = wordwp.ma_score
		# 	for idx in range(len(dictionary)):
		# 		if dictionary[i].index == word:
		# 			total_score += ma_score / 100 * dictionary[i].level
		# 			break
		# level = total_score / len(user.learning_words)
		# print("New level =", level)
		user.save()
		return jsonify(rets)
	else:
		return jsonify("Wrong json format")


