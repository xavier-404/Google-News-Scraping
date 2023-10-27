import json
import time
import re 
from datetime import datetime
from .. import endpoints

class InitializerModel:

	def __init__(self, props=None):

		# self._is_new = True
		# self._is_loaded = False
		# """init data was empty"""
		# self._is_load_empty = True
		# self._modified = None
		# """Array of initialization data"""
		# self._data = {}

		# self.modified = time.time()
		if len(props) > 0:
			self._init(props)

	def _init(self, props):
		"""
		:param props: props array
		:return: None
		"""
		for key in props.keys():
			try:
				self._init_properties_custom(props[key], key, props)
			except AttributeError:
				# if function does not exist fill help data array
				# self._data[key] = props[key]
				pass

		# self._is_new = False
		# self._is_loaded = True
		# self._is_load_empty = False

	def __repr__(self):
		return json.dumps(self, default=lambda o: o.__dict__)
	

	def _fullURL(self, url):
		if url == None or url == '':
			return None	
		if url.startswith('https://') or url.startswith('http://'):
			return url
		elif url.startswith('//'):
			return 'https:' + url
		else:
			return endpoints.get_base_url() + url
		return url

	def _filter_text(self, text):
		if isinstance(text, list):
			return self._filter_text((' ').join(text))
		else:	
			if text == None:
				return None
			else:
				text = text.replace(u'\\n', u' ')
				text = text.replace(u'<br/>', u' ')
				text = ' '.join(text.split())
			# return ''.join(text).strip()
		return text

	def _filter_results(self, text):
		if text == None:
			return None
		else:
			text = text.replace(u'約', u'')
			text = text.replace(u'件', u'')
			text = text.replace(u',', u'')
			text = ' '.join(text.split())
		return text	