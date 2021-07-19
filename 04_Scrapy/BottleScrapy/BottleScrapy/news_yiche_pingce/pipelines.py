# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    collection_name = 'news_yiche_pingce'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if 'Title' not in item:
            raise DropItem('[Dropped] No Title.')
        if 'UniqueCode' not in item:
            raise DropItem('[Dropped] No UniqueCode.')

        e_item = self.db[self.collection_name].find_one({'UniqueCode': item['UniqueCode']}, {'_id': 1})
        if e_item:
            raise DropItem('[Dropped] Item Exists.')

        self.db[self.collection_name].insert_one(dict(item))

        return item
