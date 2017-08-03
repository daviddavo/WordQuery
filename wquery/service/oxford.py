#-*- coding:utf-8 -*-
import urllib2
from urllib2 import quote
import json
from aqt.utils import showInfo
from base import WebService, export, register, with_styles

@register("Oxford (en)")
class Oxford(WebService):
	def __init__(self):
		self.word_cache = None
		self.api_cache = None
		super(Oxford, self).__init__()
		
	def _get_from_api(self, lang="en"):
		if self.word != self.word_cache:
			self.word_cache = self.word
			word = self.word
			baseurl = "https://od-api.oxforddictionaries.com/api/v1"
			app_id = "45aecf84"
			app_key = "bb36fd6a1259e5baf8df6110a2f7fc8f"
			headers = {"app_id":app_id, "app_key":app_key}
			
			word_id = quote(word.lower().replace(" ","_"))
			url = baseurl + "/entries/" + lang + "/" + word_id
			url = urllib2.Request(url, headers=headers)
			try:
				response = json.loads(urllib2.urlopen(url).read())
				showInfo("Warning: Showing only 1st definition of 1st lexical category (usualy noun)")
			except urllib2.HTTPError:
				showInfo("Error: No internet")
				response = None
			self.api_cache = response
		else:
			response = self.api_cache
		if response != None:
			return response["results"]

	@export("Lexical Category", 1)
	def _fld_category(self):
		try:
			return self._get_from_api()[0]["lexicalEntries"][0]["lexicalCategory"]
		except TypeError:
			return
		
	@export("Definition", 2)
	def _fld_definition(self):
		try:
			return str(self._get_from_api()[0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0])
		except TypeError:
			return
	
	@export("Example", 3)
	def _fld_example(self):
		try:
			return str(self._get_from_api()[0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"])
		except TypeError:
			return