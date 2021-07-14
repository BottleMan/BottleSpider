# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy.exceptions import IgnoreRequest


class DupRequestMiddleware(object):
    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # print(request.url)
        tid = request.url.strip().split('.')[-2].split('/')[-1]

        redis = spider.redis_cli
        r_tid = redis.hget('news_163_tids', tid)

        if r_tid and tid != '163':
            print('[DupRequestMiddleware] News Already Exists - %s' % tid)
            raise IgnoreRequest()

        return None
