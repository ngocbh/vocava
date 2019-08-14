from __future__ import absolute_import

from server import app
from flask import request, jsonify
from bson.json_util import dumps

from ..databases.mongo_models import *
from .. services import oxford_dictionary as od

import json

@app.route('/api/dictionary', methods=['GET'])
def get_dictionary():
	words = Dictionary.objects()
	dictionary = [word.to_dict() for word in words]
	print(dictionary)
	return jsonify(dictionary)

@app.route('/api/get-oxford-result', methods=['GET', 'POST'])
def get_oxford_result():
	"""
	uasge: http://0.0.0.0:3000/get-oxford-result?word=example
	"""
	word = request.args.get('word')
	word_info = od.get_word_info(word)
	user_id = request.args.get('user-id')
	if user_id == None:
		user_id = 1
	try:
		user = User.objects().get(index=int(user_id))
		for i in range(len(user.learning_words)):
			if user.learning_words[i].word == word:
				user.learning_words[i].num_search += 1
		for i in range(len(user.unknown_words)):
			if user.unknown_words[i].word == word:
				user.unknown_words[i].num_search += 1
		user.save()
	except Exception:
		return 'Doesnot match any user id from database', 404
	
	return jsonify(word_info)