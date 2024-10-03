import js2py
import json
from .. import endpoints
from .initializer_model import InitializerModel
from .result import Result


class Search(InitializerModel):
	def __init__(self, props=None):
		self.keyword = None
		self.result_list = None
		self.total_results = None
		self.pagination = None
		super(Search, self).__init__(props)

	def _init_properties_custom(self, value, prop, array):

		standart_properties = [
			'keyword',
		]

		if prop in standart_properties:
			self.__setattr__(prop, value)

		if prop == 'data':
			if value != None:

				thumbnail_dict = {}
				script_tags = value.css('script')
				for script in script_tags:
					nonce = script_tags.css('::attr(nonce)').extract_first()
					if nonce:
						stext = script.css('::text').extract_first()
						if "_setImagesSrc(ii,s)" in stext:
							stext = stext.replace('_setImagesSrc(ii,s)', 'return [ii, s]')
							result = js2py.eval_js(stext)
							if len(result[0]) > 0:
								ii = result[0][0]
								thumbnail_dict[ii] = result[1]

				self.result_list = []
				css_selector = [
					'div#search div#rso div.SoaBEf',
					'div#search div#rso div.xuvV6b',
					'div#search div#rso g-card.ftSUBd',
				]
				for selector in css_selector:
					r_list = value.css(selector)
					if len(r_list) > 0:
						for result in r_list:
							tresult = Result({"thumbnail_dict": thumbnail_dict, "sdata": result})
							dimg = tresult.thumbnail_url
							if dimg and dimg in thumbnail_dict:
								tresult.thumbnail_url = thumbnail_dict[dimg]
							self.result_list.append(tresult)
						break
				if self.result_list:
					self.pagination = len(self.result_list)

				t_results = value.css('div#result-stats::text').extract()
				self.total_results = self._filter_results(
					self._filter_text(t_results))

		if prop == 'pagination':
			if self.pagination:    
				self.pagination += value
			else:
				self.pagination = value         
