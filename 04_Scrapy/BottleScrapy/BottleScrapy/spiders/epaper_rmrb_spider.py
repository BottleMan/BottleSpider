# -*- coding: utf-8 -*-
import redis
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings

from BottleScrapy import util
from BottleScrapy.epaper_rmrb.items import EpaperRmrbItem


class EpaperRmrbSpider(CrawlSpider):
    name = 'epaper_rmrb'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'BottleScrapy.epaper_rmrb.middlewares.DupRequestMiddleware': 100,
        },
        'ITEM_PIPELINES': {
            'BottleScrapy.epaper_rmrb.pipelines.MongoPipeline': 101,
        },
    }

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=['paper.people.com.cn'],
                allow=r'http://paper.people.com.cn/rmrb/html/\d{4}-\d{2}/\d{2}/.*\.htm'
            ),
            callback='parse_item',
            follow=True),
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

        dym = util.get_time_in_delta('%Y-%m')
        dd = util.get_time_in_delta('%d')

        print('cur date: %s-%s' % (dym, dd))

        self.start_urls = [
            'http://paper.people.com.cn/rmrb/html/%s/%s/nbs.D110000renmrb_01.htm' % (dym, dd)
        ]

        self.settings = get_project_settings()
        self.redis_cli = self.get_redis()

    def get_redis(self, db=0):
        redis_pool = redis.ConnectionPool(host=self.settings.get('REDIS_HOST'),
                                          port=self.settings.get('REDIS_PORT'),
                                          password=self.settings.get('REDIS_AUTH'),
                                          db=db,
                                          decode_responses=True)
        redis_conn = redis.Redis(connection_pool=redis_pool)
        return redis_conn

    def parse_item(self, response):
        item = EpaperRmrbItem(response)

        return item
