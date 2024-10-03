from .initializer_model import InitializerModel
from deep_translator import GoogleTranslator


class Result(InitializerModel):
	def __init__(self, props=None):
		self.url = None
		self.title = None
		self.title_translated = None
		self.description = None
		self.des_translated = None
		self.thumbnail_url = None
		self.publisher = None
		super(Result, self).__init__(props)

	def _init_properties_custom(self, value, prop, arr):
		standart_properties = []

		if prop in standart_properties:
			self.__setattr__(prop, value)

		elif prop == 'sdata':
			if value != None:
				t_url = value.css("a::attr(href)").extract_first()
				self.url = self._fullURL(t_url)

				title_css_selectors = ['div.mCBkyc', 'div.nDgy9d']
				for selector in title_css_selectors:
					selection = value.css(selector)
					if len(selection) > 0:
						t_title = selection[0].css("*::text").extract()
						self.title = self._filter_text(t_title)
						if self.title:
							# self.title = self.title.replace('...', ' ')
							translated = GoogleTranslator(source='auto',target='ja').translate(text=self.title)
							self.title_translated = translated

				description_css_selectors = ['div.GI74Re']
				for selector in description_css_selectors:
					selection = value.css(selector)
					if len(selection) > 0:
						t_description = selection[0].css("*::text").extract()
						self.description = self._filter_text(t_description)
						if self.description:
							translated = GoogleTranslator(source='auto', target='ja').translate(text=self.description)
							self.des_translated = translated

				publisher_css_selectors = ['div.CEMjEf']
				for selector in publisher_css_selectors:
					selection = value.css(selector)
					if len(selection) > 0:
						t_publisher = selection[0].css("*::text").extract()
						self.publisher = self._filter_text(t_publisher)

				thumbnail_url_css_selectors = ['div.YEMaTe img']
				for selector in thumbnail_url_css_selectors:
					selection = value.css(selector)
					if len(selection) > 0:
						dimg = selection[0].css("::attr(id)").extract_first()
						if dimg:
							self.thumbnail_url = dimg
							