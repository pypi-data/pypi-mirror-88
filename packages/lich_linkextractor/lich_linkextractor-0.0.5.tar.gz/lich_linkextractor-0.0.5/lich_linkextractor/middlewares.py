# -*- coding: utf-8 -*-

from scrapy import signals

from lich_linkextractor.async_extension import AyncExtractor


class LinkExtractorDownloaderMiddleware:
    def __init__(self, crawler):
        self.async_extension = AyncExtractor.from_crawler(crawler)
        crawler.signals.connect(self.spider_closed, signals.spider_closed)

    def process_response(self, request, response, spider):
        response.request = request
        return self.async_extension.process_response(response)

    def spider_closed(self, spider):
        return self.async_extension.spider_closed()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler)
        return middleware
