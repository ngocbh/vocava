from __future__ import absolute_import

from .mongo_models import Dictionary, User
from ..utils.parameters import *
from ..utils.utils import find_syn_n_ant
import mongoengine as mge
import pandas as pd
import datetime
import codecs

NOW_LEVEL={0: 300,1: 1000,2: 2000,3: 3000,4: 4000,5: 6000,6: 8000,7: 12000,8: 16000,9: 20000, 10:100000}

def load_dictionary():
	Dictionary.objects().delete()

	df = pd.read_csv(DICTIONARY_FILE)
	cur_level = 0
	for index_row, row in df.iterrows():
		sfi = int(row['sfi']*1000)
		word = Dictionary(index=str(row['lemma']), level=cur_level, sfi=sfi, wordlist=str(row['wordlist']))
		word.synonyms, word.antonyms = find_syn_n_ant(word.index, word.level)
		word.save()
		if index_row >= NOW_LEVEL[cur_level]:
			cur_level += 1

	num_words = Dictionary.objects().count()
	print('Found {} words in dictionary'.format(num_words))

def build_demo_user():
	User.objects().delete()
	dictionary = Dictionary.objects()
	
	user1 = User(index=1, username='ngocjr7', email='ngocjr7@gmail.com',
		password='123456', first_name='Ngoc', last_name='Bui', level=3)
	user1.init_level(dictionary)
	user1.save()

	num_user = User.objects().count()
	print('Found {} users with tag "mongodb"'.format(num_user))

def init_databases():
	load_dictionary()
	build_demo_user()

if __name__ == '__main__':
	init_databases()