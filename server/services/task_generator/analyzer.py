from __future__ import absolute_import

from server.databases.mongo_models import *
from server.utils.parameters import *
from server.utils.parameters import *
import random

def choose_task4word(ma_score):
	if ma_score < 25:
		return 1
	elif ma_score < 50:
		return 2
	elif ma_score < 75:
		return 3
	else:
		return 4

def choose_3task4word(ma_score):
	if ma_score < 25:
		return [1, 2]
	elif ma_score < 50:
		return [2,3]
	elif ma_score < 75:
		return [3,4]
	else:
		return [4]


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
	cnt = 0
	while cnt < min(size, len(user.unknown_words)):
		print("CNT", cnt)
		wordwp = user.unknown_words[0]
		tasks = choose_3task4word(wordwp.ma_score)
		for task in tasks:
			rets.append((wordwp,task))
		# move wordwp from unknown_words to learning_words
		user.learning_words.append(wordwp)
		print("Move", wordwp.word)
		user.unknown_words.pop(0)
		cnt += 1
	user.save()
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
	total = 0
	for wordwp, task in wordwps:
		total += wordwp.ma_score
	print(user.learning_words_per_exam, len(wordwps))
	if total / len(wordwps) >= 50:
		free_learning_size = max(0, user.learning_words_per_exam - len(wordwps))
		print(user.new_words_per_exam + free_learning_size, len(wordwps))
		wordwps.extend(choose_new_words(user, user.new_words_per_exam + free_learning_size))
	
	print("------shuffe-----")
	wordwps = shuffle(wordwps)
	for wordwp, task in wordwps:
		print(wordwp.word, task)
	return wordwps





