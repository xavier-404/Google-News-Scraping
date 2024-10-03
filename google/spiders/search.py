import scrapy
import re
from .. import endpoints
from ..exceptions import ExceptionClass
from ..items import SearchItem, ResultItem
from ..model.search import Search

from scrapy.exceptions import UsageError, CloseSpider
from twisted.python.failure import Failure
from urllib.parse import urlencode


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['www.google.com']
    headers = {
        'referer': endpoints.BASE_URL,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    exit_flag = 0

    def __init__(self, unique_id='12345', keyword_id=None, hl='ja', **kwargs):
        self.unique_id = unique_id
        self.keyword_id = keyword_id
        self.hl = hl
        # The super(SearchSpider, self).__init__(**kwargs) line calls the initialization method of the parent class (scrapy.Spider).
        super(SearchSpider, self).__init__(**kwargs)

    def start_requests(self):
        if hasattr(self, 'keyword'):
            url = endpoints.get_search_link()
            params = {
                'q': self.keyword,
                'hl': self.hl,
                # 'lr': 'lang_ja',  #language example "lang_ja"
                # 'cr': 'countryJP',  #country region example "countryJP"
                'tbm': 'nws',
                'tbs': 'sbd:1',
            }
            if hasattr(self, 'count'):
                params['num'] = str(self.count)
            if hasattr(self, 'pagination'):
                params['start'] = str(self.pagination)
                self.pagination = int(self.pagination)
            else:
                self.pagination = 0

            url = url + '?' + urlencode(params)
            print(url)
            meta = {
                'unique_id': self.unique_id,
                'keyword': self.keyword,
            }
            yield scrapy.Request(url=url, callback=self.parse_search, headers=self.headers, meta=meta, errback=self.errback_httpbin)
        else:
            raise UsageError("Invalid --keyword value, use keyword=VALUE(str)")

    def parse_search(self, response):
        meta = dict(response.meta)
        data = endpoints.get_data_json(response.body)
        item = SearchItem()
        item['unique_id'] = meta['unique_id']
        item['search'] = Search({
            'keyword': meta['keyword'],
            'data': response,
            'pagination': self.pagination
        })
        item['error'] = None
        yield item

        # if self.exit_flag == 0:
        # 	self.pagination = int(item['search'].pagination)
        # 	if self.pagination and self.pagination != 0 and self.pagination < 300:
        # 		url = endpoints.get_search_link()
        # 		params = {
        # 			'q': meta['keyword'],
        # 			'hl': self.hl,
        # 			# 'lr': 'lang_ja',  #language example "lang_ja"
        # 			# 'cr': 'countryJP',  #country region example "countryJP"
        # 			'tbm': 'nws',
        # 			'tbs': 'sbd:1',
        # 			'start': str(self.pagination),
        # 		}
        # 		url = url + '?' + urlencode(params)
        # 		meta = {
        # 			'unique_id': self.unique_id,
        # 			'keyword': meta['keyword'],
        # 		}
        # 		yield scrapy.Request(url=url, callback=self.parse_search, headers=self.headers, meta=meta, dont_filter=True, errback=self.errback_httpbin)

    def errback_httpbin(self, failure):
        item = SearchItem()
        item['unique_id'] = self.unique_id
        item['search'] = None
        item['error'] = ExceptionClass.from_errback(failure)
        yield item

    def convert_date(self, text):
        regex1 = r"([0-9]{4,4})-([0-9]{1,2})-([0-9]{1,2})"
        regex2 = r"([0-9]{4,4})/([0-9]{1,2})/([0-9]{1,2})"
        regex3 = r"([0-9]{1,2})/([0-9]{1,2})/([0-9]{4,4})"

        match = re.search(regex1, text)
        match2 = re.search(regex2, text)
        match3 = re.search(regex3, text)
        if match:
            return match.group(2) + '/' + match.group(3) + '/' + match.group(1)
        elif match2:
            return match2.group(2) + '/' + match2.group(3) + '/' + match2.group(1)
        elif match3:
            return match3.group(1) + '/' + match3.group(2) + '/' + match3.group(3)
        return ''
