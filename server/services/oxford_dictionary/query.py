import requests
import json
OXFORD_APP_ID = "b90dd935"
OXFORD_APP_KEY = "31e115c68c5616004aa4ee2fbf7bddfa"
OXFORD_API_URL = "https://od-api.oxforddictionaries.com:443/api/v2/entries/"

def get_pronunciations(pronunciations):
	ret_pronuc = {}
	for pronunciation in pronunciations:
		if 'audioFile' in pronunciation:
			ret_pronuc['audioFile'] = pronunciation['audioFile']
			try:
				ret_pronuc['dialects'] = pronunciation['dialects'][0]
			except KeyError:
				pass
			try:
				ret_pronuc['phoneticNotation'] = pronunciation['phoneticNotation']
			except KeyError:
				pass
			ret_pronuc['phoneticSpelling'] = pronunciation['phoneticSpelling']
			break
	return ret_pronuc


def get_entries(entries):
	ret_entries = []
	for entry in entries:
		ret_entry = {}
		try:
			ret_entry['definitions'] = entry['entries'][0]['senses'][0]['definitions'][0]
		except KeyError:
			pass
		try:
			ret_entry['examples'] = entry['entries'][0]['senses'][0]['examples'][0]['text']
		except KeyError:
			pass
		try:
			ret_entry['shortDefinitions'] = entry['entries'][0]['senses'][0]['shortDefinitions'][0]
		except KeyError:
			pass
		try:
			ret_entry['subsenses'] = entry['entries'][0]['senses'][0]['subsenses']
		except KeyError:
			pass
		try:
			ret_entry['category'] = entry['lexicalCategory']['text']
		except KeyError:
			pass
		try:
			ret_entry['pronunciations'] = get_pronunciations(entry['pronunciations'])
		except KeyError:
			pass
		try:
			ret_entry['text'] = entry['text']
		except KeyError:
			pass

		ret_entries.append(ret_entry)
	return ret_entries

def query(word):
	language = "en"
	url = OXFORD_API_URL + language + "/" + word.lower()
	response = requests.get(url, headers={"app_id": OXFORD_APP_ID, "app_key": OXFORD_APP_KEY})
	return response.text


def get_word_info(word):
	word_info = {}
	res = json.loads(query(word))

	if 'error' in res:
		return res

	word_info['id'] = res['id']
	word_info['provider'] = res['metadata']['provider']
	word_info['entries'] = get_entries(res['results'][0]['lexicalEntries'])
	return word_info
