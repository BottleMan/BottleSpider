# -*- coding: utf-8 -*-
import redis
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from BottleScrapy.news_yiche_pingce.items import NewsYichePingceItem


class EpaperRmrbSpider(CrawlSpider):
    name = 'news_yiche_pingce'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'BottleScrapy.news_yiche_pingce.middlewares.AddHeaderMiddleware': 100,
        },
        'ITEM_PIPELINES': {
            'BottleScrapy.news_yiche_pingce.pipelines.MongoPipeline': 101,
        },
    }

    start_urls = [
        'https://news.m.yiche.com/pingce/1/',
        'https://news.m.yiche.com/pingce/2/',
        'https://news.m.yiche.com/pingce/3/',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=['news.m.yiche.com'],
                allow=r'https://news\.m\.yiche\.com/.*/\d{4}\d{2}\d{2}/.*\.html'
            ),
            callback='parse_item',
            follow=False),
    )

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)

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
        item = NewsYichePingceItem(response)

        return item
