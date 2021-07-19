# -*- coding: utf-8 -*-
import redis
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings
from BottleScrapy import util
from BottleScrapy.news_jiemian_keji.items import NewsJiemianKejiItem


class EpaperRmrbSpider(CrawlSpider):
    name = 'news_jiemian_keji'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'BottleScrapy.news_jiemian_keji.middlewares.DupRequestMiddleware': 100,
        },
        'ITEM_PIPELINES': {
            'BottleScrapy.news_jiemian_keji.pipelines.MongoPipeline': 101,
        },
    }

    start_urls = [
        'https://m.jiemian.com/lists/65_1.html',
        'https://m.jiemian.com/lists/65_2.html',
        'https://m.jiemian.com/lists/65_3.html',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=['m.jiemian.com'],
                allow=r'https://m\.jiemian\.com/article/.*\.html'
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
        item = NewsJiemianKejiItem(response)

        return item
