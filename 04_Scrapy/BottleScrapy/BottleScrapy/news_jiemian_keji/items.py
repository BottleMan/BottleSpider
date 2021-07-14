# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from BottleScrapy import util


class NewsJiemianKejiItem(scrapy.Item):
    Tid = scrapy.Field()
    Title = scrapy.Field()
    PublishDateTime = scrapy.Field()
    Author = scrapy.Field()
    Url = scrapy.Field()
    Content = scrapy.Field()
    Page = scrapy.Field()
    Source = scrapy.Field()
    UniqueCode = scrapy.Field()
    Ctime = scrapy.Field()
    Mtime = scrapy.Field()
    KeyWord = scrapy.Field()
    ConfigName = scrapy.Field()
    ConfigCategory = scrapy.Field()
    config_id = scrapy.Field()
    IsGetInfo = scrapy.Field()

    def __init__(self, response, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_ctime(response)
        self.set_thread(response)
        self.set_url(response)
        self.set_title(response)
        self.set_content(response)
        self.set_time(response)
        self.set_author(response)
        self.set_page(response)
        self.set_papername(response)
        self.set_uniquecode(response)

        self['KeyWord'] = '定向采集'
        self['ConfigName'] = '界面新闻-科技-定向采集'
        self['ConfigCategory'] = '定向采集'
        self['config_id'] = '162624195647972'
        self['IsGetInfo'] = '1'

    def set_ctime(self, response):
        try:
            ctime = util.get_cur_time()
            self['Ctime'] = ctime
            self['Mtime'] = ctime
        except Exception as e:
            print("获取 Ctime 异常 - %s" % repr(e))

    def set_thread(self, response):
        try:
            tid = response.url.strip().split('.')[-2].split('/')[-1]
            if tid:
                self['Tid'] = tid
        except Exception as e:
            print("获取 Tid 异常 - %s" % repr(e))

    def set_url(self, response):
        try:
            self['Url'] = response.url
        except Exception as e:
            print("获取 Url 异常 - %s" % repr(e))

    def set_title(self, response):
        try:
            title = response.xpath('//h1[@class="article-title"]/text()').getall()
            if title:
                title = ''.join(title)
                self['Title'] = title
        except Exception as e:
            print("获取 Title 异常 - %s" % repr(e))

    def set_content(self, response):
        try:
            text = response.xpath('//div[@id="article-content"]/text()').getall()
            if text:
                text = ''.join(text)
                self['Content'] = util.remove_html_tag(text)
        except Exception as e:
            print("获取 Content 异常 - %s" % repr(e))

    def set_time(self, response):
        try:
            date = util.get_field(r'<div class="info" data-time="(.*?)">', response.text)
            self['PublishDateTime'] = date.strip()
        except Exception as e:
            print("获取 PublishDateTime 异常 - %s" % repr(e))

    def set_author(self, response):
        try:
            author = response.xpath('//span[@class="author_name"]/text()').get()
            self['Author'] = author.strip()
        except Exception as e:
            print("获取 Author 异常 - %s" % repr(e))

    def set_page(self, response):
        try:
            self['Page'] = ''
        except Exception as e:
            print("获取 Page 异常 - %s" % repr(e))

    def set_papername(self, response):
        try:
            source = util.get_field(r'<p class="clearfix">[\w\W]*?来源：(.*?)<', response.text)
            self['Source'] = source.strip()
        except Exception as e:
            print("获取 Source 异常 - %s" % repr(e))

    def set_uniquecode(self, response):
        try:
            uniquecode = util.md5_str(response.url)
            self['UniqueCode'] = uniquecode
        except Exception as e:
            print("获取 papername 异常 - %s" % repr(e))
