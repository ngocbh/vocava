from mongoengine import *

from server.services import oxford_dictionary as od

class Dictionary(Document):
	#name of word
	index = StringField(required=True)
	#default level of word
	level = IntField(min_value=0, max_value=20)
	#frequency of word
	sfi = IntField(min_value=0)
	#provider of word
	wordlist = StringField()
	#oxford word infomation
	oxford_result = DictField()
	#list topics of word
	topics = DictField()
	#synonyms of word
	synonyms = ListField()
	#antonyms of word
	antonyms = ListField()

	def to_dict(self):
		ret = {}
		ret.update({'index': self.index})
		ret.update({'level': self.level})
		ret.update({'sfi': self.sfi})
		ret.update({'wordlist': self.wordlist})
		ret.update({'oxford_result': self.oxford_result})
		return ret

	def update_oxford_result(self):
		if len(self.oxford_result) != 0:
			return
		self.oxford_result = od.get_word_info(self.index)
		self.save()


class WordWrapper(EmbeddedDocument):
	word = StringField(required=True)
	# memorization ability score
	ma_score = IntField(min_value=0, max_value=100)
	# number of user search 
	num_search = IntField(min_value=0)
	# priority of word
	priority = IntField(min_value=0)

	def to_dict(self):
		ret = {}
		ret['word'] = self.word
		ret['ma_score'] = self.ma_score
		ret['num_search'] = self.num_search
		ret['priority'] = self.priority
		return ret

class Exam(EmbeddedDocument):
	exam_id = IntField(min_value=0)
	user_id = IntField(min_value=0)
	tasks = ListField()

class User(Document):
	#id of user
	index = IntField(min_value=0)
	username = StringField(required=True)
	email = StringField()
	password = StringField(required=True)
	first_name = StringField(max_length=50)
	last_name = StringField(max_length=50)
	#current level of user
	level = IntField(min_value=0, max_value=20)
	#known words list
	known_words = ListField(EmbeddedDocumentField(WordWrapper))
	#unknown words list
	unknown_words = ListField(EmbeddedDocumentField(WordWrapper))
	#learning words list
	learning_words = ListField(EmbeddedDocumentField(WordWrapper))
	#user parameters
	size_unknown_words = IntField(min_value=0, default=100)
	size_learning_words = IntField(min_value=0, default=20)
	new_words_per_exam = IntField(min_value=0, default=2)
	learning_words_per_exam = IntField(min_value=0, default=5)
	#pending exam
	pending_exam = ListField(EmbeddedDocumentField(Exam))
	# properties of user, like 'bad-pronunciation',... cai nay de day thoi hien tai ko can lam.
	properties = DictField()
	# topics which user usually read
	topics = DictField()
	sentences = ListField()

	def init_level(self, words):
		for i in range(len(words)):
			word = words[i]
			if word.level < self.level:
				self.known_words.append(WordWrapper(word=word.index, ma_score=100, num_search=0, priority=0))
			elif word.level == self.level:
				if len(self.unknown_words) < self.size_unknown_words:
					self.unknown_words.append(WordWrapper(word=word.index, ma_score=0, num_search=0, priority=0))

	def to_dict(self):
		ret = {}
		ret['index'] = self.index
		ret['username'] = self.username
		ret['email'] = self.email
		ret['password'] = self.password
		ret['first_name'] = self.first_name
		ret['last_name'] = self.last_name
		ret['level'] = self.level
		ret['learning_words'] = [wordw.to_dict() for wordw in self.learning_words]
		ret['no_known_words'] = len(self.known_words)
		ret['unknown_words'] = [wordw.to_dict() for wordw in self.unknown_words]
		ret['size_unknown_words'] = self.size_unknown_words
		ret['new_words_per_exam'] = self.new_words_per_exam
		ret['learning_words_per_exam'] = self.learning_words_per_exam
		ret['properties'] = self.properties
		ret['topics'] = self.topics
		ret['sentence']  = [sen for sen in self.sentences]
		return ret





