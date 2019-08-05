from __future__ import absolute_import

from .mongo_models import WordDoc, UserDoc, DictionaryDoc
from ..utils.parameters import *

import mongoengine as mge
import pandas as pd
import datetime
import codecs

NOW_LEVEL={0: 300,1: 1000,2: 2000,3: 3000,4: 4000,5: 6000,6: 8000,7: 12000,8: 16000,9: 20000}

def load_dictionary():
	DictionaryDoc.objects().delete()

	dictionary = DictionaryDoc()
	df = pd.read_csv(DICTIONARY_FILE)
	cur_level = 0
	for index, row in df.head(100).iterrows():
		sfi = int(row['sfi']*1000)
		word = WordDoc(index=row['lemma'], level=cur_level, sfi=sfi, wordlist=row['wordlist'])
		dictionary.words.append(word)
		if cur_level >= NOW_LEVEL[cur_level]:
			cur_level += 1

	dictionary.save()

	num_dict = DictionaryDoc.objects().count()
	print('Found {} dictionary with tag "mongodb" and {} words in dictionary'.format(num_dict, len(dictionary.words)))

def build_demo_user():
	UserDoc.objects().delete()
	dictionary = DictionaryDoc.objects().get()
	
	user1 = UserDoc(index=1, username='ngocjr7', email='ngocjr7@gmail.com',
		password='123456', first_name='Ngoc', last_name='Bui', level=0)
	user1.init_level(dictionary)
	user1.save()

	num_user = UserDoc.objects().count()
	print('Found {} users with tag "mongodb"'.format(num_user))

def init_databases():
	load_dictionary()
	build_demo_user()

if __name__ == '__main__':
	init_databases()