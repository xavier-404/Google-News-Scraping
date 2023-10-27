import urllib.parse
import json
import re
import codecs

import urllib.parse
import json

BASE_URL = 'https://www.google.com/'
SEARCH_LINK = 'https://www.google.com/search'


def get_base_url():
    return BASE_URL


def get_search_link():
    return SEARCH_LINK


def get_data_json(response_body):
    body = codecs.decode(response_body, encoding='utf-8', errors='ignore')
    # with open('source.html', 'w') as outfile:
    # 	outfile.write(body)
    return body


def get_page_json(response_body):
    body = codecs.decode(response_body, encoding='utf-8', errors='ignore')
    try:
        data = json.loads(body)
        # with open('source.html', 'w') as outfile:
        # 	json.dump(data, outfile)
        return data
    except Exception as e:
        pass
    return None
