from __future__ import absolute_import 

from nltk.corpus import wordnet

from server.databases import *

def find_syn_n_ant(word_name, size=3, level=None):
	synonyms = []
	antonyms = []
	for syn in wordnet.synsets(word_name):
		for lemma in syn.lemmas():
			# word = Dictionary.objects().get(index=lemma.name().lower())
			if len(synonyms) < size:
				synonyms.append(lemma.name())

			if lemma.antonyms() and len(antonyms) < size:
				antonyms.append(lemma.antonyms()[0].name())
	return list(set(synonyms)), list(set(antonyms))

def tokenize_word(word, n=1):
	ret = []
	buff = ''
	for c in word:
		if len(buff) == n:
			ret.append(buff)
			buff = c
		else:
			buff += c
	if len(buff) > 0:
		ret.append(buff)
	return ret