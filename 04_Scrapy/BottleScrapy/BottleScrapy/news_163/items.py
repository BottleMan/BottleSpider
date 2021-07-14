# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from BottleScrapy import util


class News163Item(scrapy.Item):
    news_thread = scrapy.Field()
    news_title = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()
    news_url = scrapy.Field()
    news_body = scrapy.Field()
    ctime = scrapy.Field()

    def __init__(self, response, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self['ctime'] = util.get_cur_time()

            self.get_thread(response)
            self.get_url(response)
            self.get_title(response)
            self.get_text(response)
            self.get_time(response)
            self.get_source(response)
        except Exception as e:
            print(repr(e))

    def get_thread(self, response):
        tid = response.url.strip().split('.')[-2].split('/')[-1]
        if tid:
            self['news_thread'] = tid

    def get_title(self, response):
        title = response.xpath('//h1/text()').get()
        if title:
            self['news_title'] = title

    def get_time(self, response):
        get_time = response.xpath('//div[@class="post_info"]/text()').get()
        if get_time:
            get_time = get_time.strip()
            get_time = get_time.split('　来源: ')
            get_time = get_time[0]
            self['news_time'] = get_time

    def get_source(self, response):
        source = response.xpath('//div[@class="post_info"]/text()').get()
        if source:
            source = source.strip()
            source = source.split('　来源: ')
            source = source[1]
            self['news_source'] = source

    def get_url(self, response):
        self['news_url'] = response.url

    def get_text(self, response):
        text = response.xpath('//div[@class="post_body"]//p/text()').getall()
        if text:
            text = ''.join(text)
            self['news_body'] = text
