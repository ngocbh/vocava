from __future__ import absolute_import

from server import app
from flask import request, jsonify
from bson.json_util import dumps

from ..databases.mongo_models import *
from ..services import oxford_dictionary as od
from ..services import task_generator as tg
import json

@app.route('/api/create-new-exam', methods=['GET', 'POST'])
def create_new_exam():
	user_id = request.args.get('user-id')
	if user_id == None:
		return 'user-id?????', 404
	exams = tg.generate_exam(user_id)
	print(exams)
	return jsonify(exams)


@app.route('/api/create-definition', methods=['GET', 'POST'])
def create_definition():
	word_index = request.args.get('word')
	if word_index == None:
		return 'please pass word arguments', 404
	task = tg.generate_definition(word_index)
	return jsonify(task)

@app.route('/api/create-definition-task', methods=['GET', 'POST'])
def create_definition_task():
	word_index = request.args.get('word')
	if word_index == None:
		return 'please pass word arguments', 404
	task = tg.generate_definition_task(word_index)
	return jsonify(task)

@app.route('/api/create-pronunciation-task', methods=['GET', 'POST'])
def create_pronunciation_task():
	word_index = request.args.get('word')
	if word_index == None:
		return 'please pass word arguments', 404
	task = tg.generate_pronunciation_task(word_index)
	return jsonify(task)

@app.route('/api/create-sentence-task', methods=['GET', 'POST'])
def create_sentence_task():
	word_index = request.args.get('word')
	if word_index == None:
		return 'please pass word arguments', 404
	task = tg.generate_sentence_task(word_index)
	return jsonify(task)

@app.route('/api/create-puzzle-task', methods=['GET', 'POST'])
def create_puzzle_task():
	word_index = request.args.get('word')
	if word_index == None:
		return 'please pass word arguments', 404
	task = tg.generate_puzzle_task(word_index)
	return jsonify(task)

@app.route('/api/create-practice-task', methods=['GET', 'POST'])
def create_practice_task():
	word_index = request.args.get('word')
	if word_index == None:
		return 'please pass word arguments', 404
	task = tg.generate_practice_task(word_index)
	return jsonify(task)



