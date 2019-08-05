from __future__ import absolute_import

from server.databases.mongo_models import *

def choose_tasks(user_id):
	words = []
	user = UserDoc.objects().get(index=int(user_id))
	words.extend(choose_old_words(user))
	words.extend(choose_new_words(user))
