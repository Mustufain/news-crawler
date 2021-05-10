# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

# useful for handling different item types with a single interface
import requests
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from readability import Document
from geograpy import extraction
import html2text
import logging


class NewsTextPipeline:
    """
    Gets text of news article
    """

    def process_item(self, item, spider):
        try:
            adapter = ItemAdapter(item)
            doc = Document(adapter['text'])
            content = Document(doc.content()).summary()
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            news_text = h.handle(content)
            news_text = news_text.replace("\\n", " ").\
                replace("\n", " ").\
                replace("\r", " ").\
                replace("\r\n", " ").\
                replace("**", "").\
                replace("#", "").strip()
            news_text = " ".join(news_text.split())
            adapter['text'] = news_text
        except Exception:
            raise DropItem('Failed to extract news text from: ' + item['url'])
        return item


class NewsPlaceMentionedPipeline:
    """
    Extracts places mentioned in the text of news article
    """

    def process_item(self, item, spider):
        try:
            adapter = ItemAdapter(item)
            extractor = extraction.Extractor(url=adapter['url'])
            extractor.find_geoEntities()
            places = list(set(extractor.places))
            adapter['places_mentioned'] = places
        except Exception:
            raise DropItem('Failed to extract '
                           'places mentioned in: '
                           + item['url'])
        return item


class DropEmptyRequiredFieldsPipeline:
    """
    Drop items if any one of the following fields are missing:
    1. headline
    2. text
    3. author
    4. url
    """
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if (adapter.get('headline') is None or adapter.get('text') is None or
                adapter.get('author') is None or adapter.get('url') is None):
            raise DropItem(f"Missing required fields in {item}")
        else:
            return item


class DuplicatesPipeline:
    """
    Drops items that are already processed
    """
    def __init__(self):
        self.url_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['url'] in self.url_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.url_seen.add(adapter['url'])
        return item


class MongoPipeline:
    """
    Store scraped item in Mongo db
    """

    collection_name = 'news_articles'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.insert(item)
        logging.info('news post url' + item['url'])
        logging.info('news posts added to MongoDB')
        return item

    def insert(self, item):
        collection = self.db[self.collection_name]
        collection.insert_one(ItemAdapter(item).asdict())
