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
	return jsonify(dictionary)



@app.route('/api/get-oxford-result', methods=['GET', 'POST'])
def get_oxford_result():
	"""
	uasge: http://0.0.0.0:3000/get-oxford-result?word=example
	"""
	word = request.args.get('word')
	word_info = od.get_word_info(word)
	return jsonify(word_info)