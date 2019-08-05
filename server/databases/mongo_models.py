from mongoengine import *

class WordDoc(EmbeddedDocument):
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

	def to_dict(self):
		ret = {}
		ret.update({'index': self.index})
		ret.update({'level': self.level})
		ret.update({'sfi': self.sfi})
		ret.update({'wordlist': self.wordlist})
		ret.update({'oxford_result': self.oxford_result})
		return ret

class DictionaryDoc(Document):
	words = ListField(EmbeddedDocumentField(WordDoc))

	def to_dict(self):
		ret = []
		for word in self.words:
			ret.append(word.to_dict())
		return ret

class WordDocWrapper(EmbeddedDocument):
	word = EmbeddedDocumentField(WordDoc)
	# memorization ability score
	ma_score = IntField(min_value=0, max_value=100)
	# number of user search 
	num_search = IntField(min_value=0)
	# priority of word
	priority = IntField(min_value=0)

	def to_dict(self):
		ret = {}
		ret['word'] = self.word.index
		ret['ma_score'] = self.ma_score
		ret['num_search'] = self.num_search
		ret['priority'] = self.priority
		return ret

class UserDoc(Document):
	#id of user
	index = IntField(min_value=0)
	username = StringField(required=True)
	email = StringField()
	password = StringField(required=True)
	first_name = StringField(max_length=50)
	last_name = StringField(max_length=50)
	#current level of user
	level = IntField(min_value=0, max_value=20)
	#known word list
	known_words = ListField(EmbeddedDocumentField(WordDocWrapper))
	#unknown word list
	unknown_words = ListField(EmbeddedDocumentField(WordDocWrapper))
	size_unknown_words = IntField(min_value=0, default=10)
	new_words_per_exam = IntField(min_value=0, default=6)
	old_words_per_exam = IntField(min_value=0, default=2)
	
	# properties of user, like 'bad-pronunciation',... cai nay de day thoi hien tai ko can lam.
	properties = DictField()
	# topics which user usually read
	topics = DictField()

	def init_level(self, dictionary):
		for i in range(len(dictionary.words)):
			word = dictionary.words[i]
			if word.level < self.level:
				self.known_words.append(WordDocWrapper(word=word, ma_score=100, num_search=0, priority=0))
			elif word.level == self.level:
				if len(self.unknown_words) < self.size_unknown_words:
					self.unknown_words.append(WordDocWrapper(word=word, ma_score=0, num_search=0, priority=0))

	def to_dict(self):
		ret = {}
		ret['index'] = self.index
		ret['username'] = self.username
		ret['email'] = self.email
		ret['password'] = self.password
		ret['first_name'] = self.first_name
		ret['last_name'] = self.last_name
		ret['level'] = self.level
		# ret['known_words'] = [wordw.to_dict() for wordw in self.known_words]
		ret['no_known_words'] = len(self.known_words)
		ret['unknown_words'] = [wordw.to_dict() for wordw in self.unknown_words]
		ret['size_unknown_words'] = self.size_unknown_words
		ret['new_words_per_exam'] = self.new_words_per_exam
		ret['old_words_per_exam'] = self.old_words_per_exam
		ret['properties'] = self.properties
		ret['topics'] = self.topics
		return ret





