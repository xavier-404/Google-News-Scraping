BOT_NAME = 'google'
SPIDER_MODULES = ['google.spiders']
NEWSPIDER_MODULE = 'google.spiders'

# LOG_LEVEL = 'WARNING'
LOG_FILE = 'error.log'

ROBOTSTXT_OBEY = False

HTTP_PROXY = 'http://127.0.0.1:8118'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
# DEFAULT_REQUEST_HEADERS = {}


CONCURRENT_REQUESTS = 8
# DOWNLOAD_DELAY = 2
# CONCURRENT_REQUESTS_PER_DOMAIN = 8
# CONCURRENT_REQUESTS_PER_IP = 8


DOWNLOADER_MIDDLEWARES = {
    # 'google.middlewares.ProxyMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {
    'google.pipelines.GooglePipeline': 300,
}
