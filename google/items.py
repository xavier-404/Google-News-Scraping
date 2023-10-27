import scrapy


class SearchItem(scrapy.Item):
    unique_id = scrapy.Field()
    search = scrapy.Field()
    error = scrapy.Field()


class ResultItem(scrapy.Item):
    unique_id = scrapy.Field()
    result = scrapy.Field()
    error = scrapy.Field()
