from __future__ import absolute_import

from server.databases.mongo_models import *
from server.utils.parameters import *
from server.utils.parameters import *
import random

def choose_task4word(ma_score):
	if ma_score < 10:
		return 0
	elif ma_score < 30:
		return 1
	elif ma_score < 50:
		return 2
	elif ma_score < 70:
		return 3
	elif ma_score < 90:
		return 4
	else:
		return 5

def choose_3task4word(ma_score):
	if ma_score < 10:
		return [0,1,2]
	elif ma_score < 30:
		return [1,2,3]
	elif ma_score < 50:
		return [2,3,4]
	elif ma_score < 70:
		return [3,4,5]
	elif ma_score < 90:
		return [4,5,5]
	else:
		return [5,5,5]


def choose_learning_words(user, size):
	rets = []
	user.learning_words.sort(key=lambda wordwp: -wordwp.ma_score)
	for i in range(min(size, len(user.learning_words))):
		wordwp = user.learning_words[i]
		tasks = choose_3task4word(wordwp.ma_score)
		for task in tasks:
			rets.append((wordwp,task))
	return rets

def choose_new_words(user, size):
	rets = []
	user.unknown_words.sort(key=lambda wordwp: -wordwp.priority-wordwp.num_search)
	for i in range(min(size, len(user.unknown_words))):
		wordwp = user.unknown_words[i]
		tasks = choose_3task4word(wordwp.ma_score)
		for task in tasks:
			rets.append((wordwp,task))
	return rets

def shuffle(wordwps):
	rets = []
	for wordwp, task in wordwps:
		left = -1
		for i in range(len(rets) - 1, -1, -1):
			if rets[i][0].word == wordwp.word:
				left = i
				break
		if left == -1:
			left = 0
			right = int(len(rets) / 2)
		else:
			right = len(rets)
			left = min(right, left + 2)
		random_idx = random.randint(left, right)
		rets.insert(random_idx, ((wordwp, task)))

	return rets

def choose_tasks(user):
	wordwps = []

	wordwps.extend(choose_learning_words(user, user.learning_words_per_exam))

	free_learning_size = user.learning_words_per_exam - len(wordwps)
	num_newword = min(user.size_learning_words - len(user.learning_words), 
		user.new_words_per_exam + int(free_learning_size/2))

	wordwps.extend(choose_new_words(user, num_newword))
	
	# print("------shuffe-----")
	wordwps = shuffle(wordwps)
	# for wordwp, task in wordwps:
	# 	print(wordwp.word, task)
	return wordwps





