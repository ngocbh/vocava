from __future__ import absolute_import

from nltk.corpus import wordnet
from server import utils
from .analyzer import *

from server.databases import *

import random
import re

def build_bag_of_words(target_word, level, bag_of_words=[]):
	if len(bag_of_words) > 3:
		return random.sample(bag_of_words, k=3)

	bag_of_words = set(bag_of_words)
	words = []
	for word in Dictionary.objects(level=level):
		words.append(word)
		if len(words) > 100:
			break

	while len(bag_of_words) < 3:
		i = random.randint(0,len(words)-1)
		if words[i].index not in bag_of_words:
			bag_of_words.add(words[i].index)

	return list(bag_of_words)



def generate_definition(word_index):
	task = {}
	word = Dictionary.objects().get(index=word_index)
	word.update_oxford_result()

	task['type'] = 'definition'
	task['word'] = word_index
	try:
		task['shortDefinition'] = word.oxford_result['entries'][0]['shortDefinitions']
	except KeyError:
		task['definition'] = word.oxford_result['entries'][0]['definitions']

	task['synonyms'] = word.synonyms
	task['antonyms'] = word.antonyms
	return task


def generate_definition_task(word_index, bag_of_words=[]):
	task = {}
	word = Dictionary.objects().get(index=word_index)
	word.update_oxford_result()

	options = build_bag_of_words(word_index, word.level, bag_of_words)
	options.append(word.index)
	random.shuffle(options)

	task['type'] = 'definition_task'
	task['word'] = word_index
	try: 
		task['question'] = word.oxford_result['entries'][0]['shortDefinitions']
	except KeyError:
		task['question'] = word.oxford_result['entries'][0]['definition']

	task['options'] = options
	for i in range(0,4):
		if task['options'][i] == word_index:
			task['answer'] = i

	return task


def generate_pronunciation_task(word_index, bag_of_words=[]):
	task = {}
	word = Dictionary.objects().get(index=word_index)
	word.update_oxford_result()

	options = build_bag_of_words(word_index, word.level, bag_of_words)
	options.append(word.index)
	random.shuffle(options)

	task['type'] = 'pronunciation_task'
	task['word'] = word_index
	try: 
		task['question'] = word.oxford_result['entries'][0]['pronunciations']['audioFile']
	except KeyError:
		raise KeyError('We dont have audioFile for {}'.format(word_index))

	task['options'] = options
	for i in range(0,4):
		if task['options'][i] == word_index:
			task['answer'] = i

	task['explainAnswer'] = word.oxford_result['entries'][0]['pronunciations']['phoneticSpelling']

	return task

def generate_sentence_task(word_index, bag_of_words=[]):
	task = {}
	word = Dictionary.objects().get(index=word_index)
	word.update_oxford_result()

	options = build_bag_of_words(word_index, word.level, bag_of_words)
	options.append(word.index)
	random.shuffle(options)

	task['type'] = 'sentence_task'
	task['word'] = word_index

	try: 
		sen = word.oxford_result['entries'][0]['examples']
		sen = re.sub('[ \',]%s[ \',?!:.]*' % word_index, ' ___ ', sen)

		task['question'] = sen
	except KeyError:
		raise KeyError('We dont have sentence for {}'.format(word_index))

	task['options'] = options
	for i in range(0,4):
		if task['options'][i] == word_index:
			task['answer'] = i

	return task

def generate_puzzle_task(word_index):
	task = {}
	word = Dictionary.objects().get(index=word_index)
	word.update_oxford_result()

	task['type'] = 'puzzle_task'
	task['word'] = word_index

	try: 
		task['question'] = word.oxford_result['entries'][0]['pronunciations']['audioFile']
	except KeyError:
		raise ('We dont have audioFile for {}'.format(word_index))

	options = utils.tokenize_word(word_index, n=1)
	random.shuffle(options)

	task['options'] = options
	task['answer'] = word.index
	return task

def generate_practice_task(word_index):
	task = random.randint(1,4)
	if task == 1:
		return generate_definition_task(word_index)
	elif task == 2:
		return generate_pronunciation_task(word_index)
	elif task == 3:
		return generate_sentence_task(word_index)
	elif task == 4:
		return generate_puzzle_task(word_index)

def generate_exam(user_id):
	exams = []
	user = User.objects().get(index=int(user_id))
	wordwps = choose_tasks(user)
	bag_of_words = [wordwps[i][0].word for i in range(len(wordwps))]
	for i in range(len(wordwps)):
		wordwp = wordwps[i][0]
		word_index = wordwp.word
		task = wordwps[i][1]
		if task == 0:
			exams.append(generate_definition(word_index))
		elif task == 1:
			exams.append(generate_definition_task(word_index, bag_of_words))
		elif task == 2:
			exams.append(generate_pronunciation_task(word_index, bag_of_words))
		elif task == 3:
			exams.append(generate_sentence_task(word_index, bag_of_words))
		elif task == 4:
			exams.append(generate_puzzle_task(word_index))
		elif task == 5:
			exams.append(generate_practice_task(word_index))
	return exams
	