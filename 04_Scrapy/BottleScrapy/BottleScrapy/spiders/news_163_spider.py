# -*- coding: utf-8 -*-
import redis
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.project import get_project_settings

from BottleScrapy.news_163.items import News163Item


class News163Spider(CrawlSpider):
    name = 'news163'
    allowed_domains = [
        'news.163.com',
        'www.163.com'
    ]
    start_urls = ['https://news.163.com/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'BottleScrapy.news_163.pipelines.DuplicateFilterPipline': 100,
            'BottleScrapy.news_163.pipelines.MongoPipeline': 101,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'BottleScrapy.news_163.middlewares.DupRequestMiddleware': 100,
        },
    }

    rules = (
        # Rule(
        #     LinkExtractor(
        #         allow_domains=allowed_domains,
        #     ),
        #     follow=False),
        Rule(
            LinkExtractor(
                allow_domains=allowed_domains,
                allow=r'https://.*\.163\.com/.*/?\.html',
                deny=r'https://.*\.163\.com/.*/?media/.*\.html'
            ),
            callback='parse_item',
            follow=True),
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
        item = News163Item(response)

        return item
